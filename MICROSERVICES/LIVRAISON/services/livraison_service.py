from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from MICROSERVICES.COMMANDE.models.commande import Commande, StatutCommande
from MICROSERVICES.LOGISTIQUE.models.logistique import DossierConsolidation, StatutConsolidation
from MICROSERVICES.COMMANDE.schemas.commande import CommandeUpdate
from MICROSERVICES.COMMANDE.services.commande_service import CommandeService

from ..models.livraison import Livraison, LivraisonEvenement, StatutLivraison
from ..respositories.livraison_repository import LivraisonRepository
from ..schemas.livraison import LivraisonCreate, LivraisonUpdateEntrepot, LivraisonUpdateLivree, LivraisonUpdateRamassage, LivraisonUpdateTransit


class LivraisonService:
	def __init__(self, db: Session):
		self.db = db
		self.repo = LivraisonRepository(db)
		self.commande_service = CommandeService(db)

	def _ajouter_evenement(self, livraison: Livraison, statut_avant: StatutLivraison | None, statut_apres: StatutLivraison, acteur_identifiant=None, commentaire: str | None = None):
		evenement = LivraisonEvenement(
			livraison_identifiant=livraison.identifiant,
			statut_avant=statut_avant,
			statut_apres=statut_apres,
			acteur_identifiant=acteur_identifiant,
			commentaire=commentaire,
		)
		self.repo.ajouter_evenement(evenement)

	def creer(self, payload: LivraisonCreate, acteur_payload: dict):
		commande = self.db.query(Commande).filter(Commande.identifiant == payload.commande_identifiant).first()
		if not commande:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande introuvable")

		dossier_id = payload.dossier_consolidation_identifiant
		if dossier_id:
			dossier = self.db.query(DossierConsolidation).filter(DossierConsolidation.identifiant == dossier_id).first()
			if not dossier:
				raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dossier de consolidation introuvable")
			if str(dossier.commande_identifiant) != str(payload.commande_identifiant):
				raise HTTPException(
					status_code=status.HTTP_400_BAD_REQUEST,
					detail="Le dossier de consolidation ne correspond pas à la commande",
				)
			if dossier.statut not in {StatutConsolidation.ARRIVE_ABIDJAN, StatutConsolidation.REMIS_LIVRAISON_LOCALE}:
				raise HTTPException(
					status_code=status.HTTP_400_BAD_REQUEST,
					detail="La livraison locale ne peut commencer qu'après ARRIVE_ABIDJAN",
				)

		existante = self.repo.get_by_commande(payload.commande_identifiant)
		if existante:
			return existante

		livraison = Livraison(
			commande_identifiant=payload.commande_identifiant,
			dossier_consolidation_identifiant=payload.dossier_consolidation_identifiant,
			statut=StatutLivraison.ASSIGNEE if payload.livreur_nom else StatutLivraison.CREEE,
			livreur_nom=payload.livreur_nom,
			livreur_telephone=payload.livreur_telephone,
			commentaire=payload.commentaire,
		)
		livraison = self.repo.creer(livraison)

		self._ajouter_evenement(
			livraison,
			None,
			livraison.statut,
			acteur_identifiant=acteur_payload.get("sub"),
			commentaire="Livraison créée",
		)
		self.db.refresh(livraison)
		return livraison

	def obtenir(self, livraison_id):
		livraison = self.repo.get_by_id(livraison_id)
		if not livraison:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livraison introuvable")
		return livraison

	def _mettre_a_jour_commande(self, commande_id, statut: StatutCommande):
		self.commande_service.maj_commande(commande_id, CommandeUpdate(statut=statut))

	def signaler_expedition_vendeur(self, livraison_id, payload: LivraisonUpdateRamassage, acteur_payload: dict):
		livraison = self.obtenir(livraison_id)
		if livraison.statut == StatutLivraison.EN_TRANSIT:
			return livraison
		if livraison.statut not in {StatutLivraison.CREEE, StatutLivraison.ASSIGNEE}:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transition invalide vers EN_TRANSIT (expédition vendeur)")

		ancien = livraison.statut
		livraison = self.repo.maj(
			livraison,
			{
				"statut": StatutLivraison.EN_TRANSIT,
				"date_ramassage": datetime.utcnow(),
				"commentaire": payload.commentaire or livraison.commentaire,
			},
		)
		self._ajouter_evenement(
			livraison,
			ancien,
			StatutLivraison.EN_TRANSIT,
			acteur_identifiant=acteur_payload.get("sub"),
			commentaire=payload.commentaire or "Vendeur: colis expédié vers Abidjan",
		)
		self._mettre_a_jour_commande(livraison.commande_identifiant, StatutCommande.EXPEDIEE)
		self.db.refresh(livraison)
		return livraison

	def signaler_en_transit(self, livraison_id, payload: LivraisonUpdateTransit, acteur_payload: dict):
		livraison = self.obtenir(livraison_id)
		if livraison.statut == StatutLivraison.EN_TRANSIT:
			return livraison
		if livraison.statut not in {StatutLivraison.CREEE, StatutLivraison.ASSIGNEE, StatutLivraison.EN_TRANSIT}:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transition invalide vers EN_TRANSIT")

		ancien = livraison.statut
		livraison = self.repo.maj(
			livraison,
			{
				"statut": StatutLivraison.EN_TRANSIT,
				"commentaire": payload.commentaire or livraison.commentaire,
			},
		)
		self._ajouter_evenement(
			livraison,
			ancien,
			StatutLivraison.EN_TRANSIT,
			acteur_identifiant=acteur_payload.get("sub"),
			commentaire=payload.commentaire or "Colis en transit",
		)
		self.db.refresh(livraison)
		return livraison

	def verifier_entrepot_abidjan(self, livraison_id, payload: LivraisonUpdateEntrepot, acteur_payload: dict):
		livraison = self.obtenir(livraison_id)
		if livraison.statut == StatutLivraison.ARRIVEE_ENTREPOT_ABIDJAN:
			return livraison
		if livraison.statut != StatutLivraison.EN_TRANSIT:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transition invalide vers ARRIVEE_ENTREPOT_ABIDJAN")

		ancien = livraison.statut
		livraison = self.repo.maj(
			livraison,
			{
				"statut": StatutLivraison.ARRIVEE_ENTREPOT_ABIDJAN,
				"date_verification_entrepot": datetime.utcnow(),
				"commentaire": payload.commentaire or livraison.commentaire,
			},
		)
		self._ajouter_evenement(
			livraison,
			ancien,
			StatutLivraison.ARRIVEE_ENTREPOT_ABIDJAN,
			acteur_identifiant=acteur_payload.get("sub"),
			commentaire=payload.commentaire or "Entrepôt Abidjan: vérifications terminées",
		)
		self.db.refresh(livraison)
		return livraison

	def signaler_livree_client(self, livraison_id, payload: LivraisonUpdateLivree, acteur_payload: dict):
		livraison = self.obtenir(livraison_id)
		if livraison.statut == StatutLivraison.LIVREE_CLIENT:
			return livraison
		if livraison.statut != StatutLivraison.ARRIVEE_ENTREPOT_ABIDJAN:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transition invalide vers LIVREE_CLIENT")
		if not payload.preuve_livraison_url:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Preuve de livraison obligatoire")

		ancien = livraison.statut
		livraison = self.repo.maj(
			livraison,
			{
				"statut": StatutLivraison.LIVREE_CLIENT,
				"date_livraison": datetime.utcnow(),
				"preuve_livraison_url": payload.preuve_livraison_url,
				"commentaire": payload.commentaire or livraison.commentaire,
			},
		)
		self._ajouter_evenement(
			livraison,
			ancien,
			StatutLivraison.LIVREE_CLIENT,
			acteur_identifiant=acteur_payload.get("sub"),
			commentaire=payload.commentaire or "Livraison client confirmée",
		)
		self._mettre_a_jour_commande(livraison.commande_identifiant, StatutCommande.LIVREE)
		self.db.refresh(livraison)
		return livraison
