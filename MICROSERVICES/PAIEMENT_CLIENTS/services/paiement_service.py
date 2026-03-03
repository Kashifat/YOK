from datetime import datetime
from uuid import UUID, uuid4
import logging

import httpx
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur, Utilisateur
from MICROSERVICES.COMMANDE.models.commande import Commande, CommandeArticle, StatutCommande
from MICROSERVICES.FACTURE.models.facture import Facture, FacturePaiementSuivi, StatutPaiementFacture

from ..config import settings
from ..models.paiement import FournisseurPaiement, Paiement, PaiementEvenement, StatutPaiementTransaction
from ..respositories.paiement_repository import PaiementRepository
from ..schemas.paiement import PaiementInitialisationCreate


class PaiementService:
	def __init__(self, db: Session):
		self.db = db
		self.repo = PaiementRepository(db)
		self.logger = logging.getLogger(__name__)

	def _map_statut_provider(self, statut_brut: str | None) -> StatutPaiementTransaction:
		if not statut_brut:
			return StatutPaiementTransaction.EN_COURS

		valeur = str(statut_brut).strip().upper()
		if valeur in {"ACCEPTED", "SUCCESS", "PAID", "SUCCES", "00", "PAYEE"}:
			return StatutPaiementTransaction.PAYEE
		if valeur in {"REFUSED", "FAILED", "ECHEC", "ERROR", "KO", "CANCELED", "ANNULEE"}:
			return StatutPaiementTransaction.ECHOUE
		return StatutPaiementTransaction.EN_COURS

	def _ajouter_evenement(
		self,
		paiement_id,
		type_evenement: str,
		source: str,
		ancien_statut: StatutPaiementTransaction | None,
		nouveau_statut: StatutPaiementTransaction,
		payload: dict | None,
		commentaire: str | None = None,
	):
		evenement = PaiementEvenement(
			paiement_identifiant=paiement_id,
			type_evenement=type_evenement,
			source=source,
			ancien_statut=ancien_statut,
			nouveau_statut=nouveau_statut,
			payload=payload,
			commentaire=commentaire,
		)
		self.repo.ajouter_evenement(evenement)

	def _synchroniser_commande_facture(self, paiement: Paiement):
		commande = self.db.query(Commande).filter(Commande.identifiant == paiement.commande_identifiant).first()
		if not commande:
			return

		if paiement.statut == StatutPaiementTransaction.PAYEE:
			commande.statut = StatutCommande.PAYEE
			for article in commande.articles:
				article.statut = StatutCommande.PAYEE
		elif paiement.statut in {StatutPaiementTransaction.ECHOUE, StatutPaiementTransaction.ANNULEE}:
			commande.statut = StatutCommande.EN_ATTENTE_PAIEMENT
			for article in commande.articles:
				article.statut = StatutCommande.EN_ATTENTE_PAIEMENT
		self.db.flush()

		if commande.statut == StatutCommande.PAYEE:
			try:
				from MICROSERVICES.PAIEMENT_VENDEURS.services.wallet_service import WalletService
				wallet_service = WalletService(self.db)
				wallet_service.traiter_evenement_commande(
					commande.identifiant,
					StatutCommande.PAYEE,
					source="PAIEMENT_CLIENTS_WEBHOOK",
				)
			except Exception as exc:
				self.logger.warning("Synchronisation wallet vendeurs échouée pour commande %s: %s", commande.identifiant, exc)

		facture = self.db.query(Facture).filter(Facture.commande_identifiant == paiement.commande_identifiant).first()
		if not facture:
			return

		ancien_statut = facture.statut_paiement
		if paiement.statut == StatutPaiementTransaction.PAYEE:
			nouveau_statut = StatutPaiementFacture.PAYEE
			facture.date_paiement = facture.date_paiement or datetime.utcnow()
		elif paiement.statut in {StatutPaiementTransaction.ECHOUE, StatutPaiementTransaction.ANNULEE}:
			nouveau_statut = StatutPaiementFacture.ECHOUE
		else:
			nouveau_statut = StatutPaiementFacture.EN_ATTENTE

		if ancien_statut != nouveau_statut:
			facture.statut_paiement = nouveau_statut
			facture.mode_paiement = FournisseurPaiement.CINETPAY.value
			facture.reference_paiement = paiement.provider_transaction_id
			self.db.flush()

			suivi = FacturePaiementSuivi(
				facture_identifiant=facture.identifiant,
				ancien_statut=ancien_statut,
				nouveau_statut=nouveau_statut,
				commentaire=f"Synchronisation depuis PAIEMENT ({paiement.statut.value})",
				acteur_identifiant=paiement.utilisateur_identifiant,
			)
			self.db.add(suivi)
			self.db.flush()

	def _verifier_acces(self, paiement: Paiement, utilisateur_payload: dict):
		role = utilisateur_payload.get("role")
		if role == RoleUtilisateur.ADMINISTRATEUR.value:
			return

		if str(paiement.utilisateur_identifiant) != str(utilisateur_payload.get("sub")):
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

	def obtenir(self, paiement_id: UUID, utilisateur_payload: dict):
		paiement = self.repo.get_by_id(paiement_id)
		if not paiement:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paiement introuvable")
		self._verifier_acces(paiement, utilisateur_payload)
		return paiement

	def obtenir_par_commande(self, commande_id: UUID, utilisateur_payload: dict):
		paiement = self.repo.get_by_commande(commande_id)
		if not paiement:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paiement introuvable pour cette commande")
		self._verifier_acces(paiement, utilisateur_payload)
		return paiement

	def obtenir_par_transaction(self, provider_transaction_id: str, utilisateur_payload: dict):
		paiement = self.repo.get_by_provider_transaction_id(provider_transaction_id)
		if not paiement:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paiement introuvable pour cette transaction")
		self._verifier_acces(paiement, utilisateur_payload)
		return paiement

	def _initialiser_cinetpay(self, paiement: Paiement, commande: Commande, utilisateur: Utilisateur, payload: PaiementInitialisationCreate):
		transaction_id = f"YOK-{uuid4().hex[:18].upper()}"

		if not settings.cinetpay_api_key or not settings.cinetpay_site_id:
			payment_url = f"https://checkout.cinetpay.com/mock/{transaction_id}"
			donnees = {
				"provider_transaction_id": transaction_id,
				"provider_payment_url": payment_url,
				"statut": StatutPaiementTransaction.EN_COURS,
			}
			paiement = self.repo.maj(paiement, donnees)
			self._ajouter_evenement(
				paiement.identifiant,
				"INITIALISATION",
				"SYSTEM",
				StatutPaiementTransaction.EN_ATTENTE,
				paiement.statut,
				{"mode": "SIMULATION", "transaction_id": transaction_id},
				"CinetPay non configuré: mode simulation activé",
			)
			return paiement, "SIMULATION"

		request_payload = {
			"apikey": settings.cinetpay_api_key,
			"site_id": settings.cinetpay_site_id,
			"transaction_id": transaction_id,
			"amount": commande.total_cfa,
			"currency": "XOF",
			"description": payload.description or f"Paiement commande {commande.identifiant}",
			"notify_url": settings.cinetpay_notify_url,
			"return_url": settings.cinetpay_return_url,
			"channels": (payload.canal or "ALL").upper(),
			"customer_name": utilisateur.nom_complet,
			"customer_email": utilisateur.courriel,
			"customer_phone_number": payload.telephone or utilisateur.telephone,
		}

		try:
			with httpx.Client(timeout=15.0) as client:
				reponse = client.post(settings.cinetpay_api_url, json=request_payload)
			reponse.raise_for_status()
			reponse_json = reponse.json()
		except Exception as exc:
			raise HTTPException(
				status_code=status.HTTP_502_BAD_GATEWAY,
				detail=f"Erreur initialisation CinetPay: {exc}",
			) from exc

		donnees_provider = reponse_json.get("data") or {}
		payment_url = donnees_provider.get("payment_url") or donnees_provider.get("payment_link")
		if not payment_url:
			raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Réponse CinetPay invalide: payment_url absent")

		paiement = self.repo.maj(
			paiement,
			{
				"provider_transaction_id": donnees_provider.get("transaction_id") or transaction_id,
				"provider_payment_url": payment_url,
				"payload_initialisation": reponse_json,
				"statut": StatutPaiementTransaction.EN_COURS,
			},
		)
		self._ajouter_evenement(
			paiement.identifiant,
			"INITIALISATION",
			"CINETPAY_API",
			StatutPaiementTransaction.EN_ATTENTE,
			paiement.statut,
			reponse_json,
			"Paiement initialisé chez CinetPay",
		)
		return paiement, "CINETPAY"

	def initialiser(self, utilisateur_payload: dict, payload: PaiementInitialisationCreate):
		commande = self.db.query(Commande).filter(Commande.identifiant == payload.commande_identifiant).first()
		if not commande:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande introuvable")

		role = utilisateur_payload.get("role")
		if role != RoleUtilisateur.ADMINISTRATEUR.value and str(commande.client_identifiant) != str(utilisateur_payload.get("sub")):
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

		if commande.statut not in {StatutCommande.EN_ATTENTE_PAIEMENT, StatutCommande.PAYEE}:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Commande non payable dans son statut actuel")

		existant = self.repo.get_by_commande(commande.identifiant)
		if existant and existant.statut == StatutPaiementTransaction.PAYEE:
			return {
				"paiement": existant,
				"payment_url": existant.provider_payment_url or "",
				"provider_transaction_id": existant.provider_transaction_id or "",
				"mode": "EXISTANT",
			}

		if existant:
			paiement = existant
			ancien = paiement.statut
			paiement = self.repo.maj(
				paiement,
				{
					"statut": StatutPaiementTransaction.EN_ATTENTE,
					"methode": payload.canal,
					"description": payload.description,
				},
			)
			self._ajouter_evenement(
				paiement.identifiant,
				"REINITIALISATION",
				"API",
				ancien,
				paiement.statut,
				{"commande_id": str(commande.identifiant)},
			)
		else:
			paiement = Paiement(
				commande_identifiant=commande.identifiant,
				utilisateur_identifiant=commande.client_identifiant,
				montant_cfa=commande.total_cfa,
				fournisseur=FournisseurPaiement.CINETPAY,
				statut=StatutPaiementTransaction.EN_ATTENTE,
				methode=payload.canal,
				description=payload.description,
			)
			paiement = self.repo.creer(paiement)

		utilisateur = self.db.query(Utilisateur).filter(Utilisateur.identifiant == commande.client_identifiant).first()
		if not utilisateur:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")

		paiement, mode = self._initialiser_cinetpay(paiement, commande, utilisateur, payload)
		self.db.refresh(paiement)
		return {
			"paiement": paiement,
			"payment_url": paiement.provider_payment_url,
			"provider_transaction_id": paiement.provider_transaction_id,
			"mode": mode,
		}

	def traiter_webhook(self, payload: dict, signature_header: str | None = None):
		if settings.cinetpay_webhook_secret and signature_header != settings.cinetpay_webhook_secret:
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Signature webhook invalide")

		transaction_id = (
			payload.get("transaction_id")
			or payload.get("cpm_trans_id")
			or payload.get("provider_transaction_id")
		)
		if not transaction_id:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="transaction_id manquant")

		paiement = self.repo.get_by_provider_transaction_id(transaction_id)
		if not paiement:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paiement introuvable")

		ancien_statut = paiement.statut
		nouveau_statut = self._map_statut_provider(
			payload.get("status") or payload.get("cpm_result") or payload.get("payment_status")
		)

		donnees = {
			"statut": nouveau_statut,
			"payload_webhook": payload,
		}
		if nouveau_statut == StatutPaiementTransaction.PAYEE and not paiement.date_confirmation:
			donnees["date_confirmation"] = datetime.utcnow()

		paiement = self.repo.maj(paiement, donnees)
		self._ajouter_evenement(
			paiement.identifiant,
			"WEBHOOK",
			"CINETPAY_WEBHOOK",
			ancien_statut,
			nouveau_statut,
			payload,
		)
		self._synchroniser_commande_facture(paiement)
		self.db.refresh(paiement)
		return {
			"paiement": paiement,
			"source": "WEBHOOK",
			"message": "Webhook traité",
		}

	def verifier(self, paiement_id: UUID, utilisateur_payload: dict):
		paiement = self.obtenir(paiement_id, utilisateur_payload)
		if not paiement.provider_transaction_id:
			return {
				"paiement": paiement,
				"source": "LOCAL",
				"message": "Paiement sans transaction provider à vérifier",
			}

		if not settings.cinetpay_api_key or not settings.cinetpay_site_id:
			return {
				"paiement": paiement,
				"source": "SIMULATION",
				"message": "CinetPay non configuré, vérification distante ignorée",
			}

		request_payload = {
			"apikey": settings.cinetpay_api_key,
			"site_id": settings.cinetpay_site_id,
			"transaction_id": paiement.provider_transaction_id,
		}

		try:
			with httpx.Client(timeout=15.0) as client:
				reponse = client.post(settings.cinetpay_check_url, json=request_payload)
			reponse.raise_for_status()
			reponse_json = reponse.json()
		except Exception as exc:
			raise HTTPException(
				status_code=status.HTTP_502_BAD_GATEWAY,
				detail=f"Erreur vérification CinetPay: {exc}",
			) from exc

		donnees_provider = reponse_json.get("data") or {}
		nouveau_statut = self._map_statut_provider(
			donnees_provider.get("status") or reponse_json.get("status") or reponse_json.get("code")
		)
		ancien_statut = paiement.statut
		donnees = {"statut": nouveau_statut}
		if nouveau_statut == StatutPaiementTransaction.PAYEE and not paiement.date_confirmation:
			donnees["date_confirmation"] = datetime.utcnow()
		paiement = self.repo.maj(paiement, donnees)
		self._ajouter_evenement(
			paiement.identifiant,
			"VERIFICATION",
			"CINETPAY_API",
			ancien_statut,
			nouveau_statut,
			reponse_json,
		)
		self._synchroniser_commande_facture(paiement)
		self.db.refresh(paiement)
		return {
			"paiement": paiement,
			"source": "CINETPAY_API",
			"message": "Vérification effectuée",
		}

	def retour_frontend(self, provider_transaction_id: str, utilisateur_payload: dict):
		paiement = self.obtenir_par_transaction(provider_transaction_id, utilisateur_payload)

		if paiement.statut in {StatutPaiementTransaction.PAYEE, StatutPaiementTransaction.ECHOUE, StatutPaiementTransaction.ANNULEE}:
			return {
				"paiement": paiement,
				"source": "RETOUR_FRONTEND",
				"message": "Statut final déjà connu",
			}

		try:
			return self.verifier(paiement.identifiant, utilisateur_payload)
		except HTTPException:
			self.db.refresh(paiement)
			return {
				"paiement": paiement,
				"source": "RETOUR_FRONTEND_LOCAL",
				"message": "Retour reçu, en attente de confirmation webhook",
			}

	def traiter_webhook_brut(self, payload_brut: dict, signature_header: str | None = None):
		payload = payload_brut.get("payload") if isinstance(payload_brut.get("payload"), dict) else payload_brut
		return self.traiter_webhook(payload, signature_header=signature_header)
