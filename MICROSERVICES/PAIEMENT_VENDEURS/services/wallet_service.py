from collections import defaultdict

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur
from MICROSERVICES.COMMANDE.models.commande import Commande, CommandeArticle, StatutCommande
from MICROSERVICES.CATALOGUE.models.produit import Produit

from ..config import settings
from ..models.wallet import StatutReservationWallet, TransactionWallet, TypeTransactionWallet, WalletReservationCommande, WalletVendeur
from ..respositories.wallet_repository import WalletRepository
from ..schemas.wallet import EvenementCommandeCreate


class WalletService:
	def __init__(self, db: Session):
		self.db = db
		self.repo = WalletRepository(db)

	def _get_or_create_wallet(self, vendeur_id):
		wallet = self.repo.get_wallet(vendeur_id)
		if wallet:
			return wallet
		wallet = WalletVendeur(vendeur_identifiant=vendeur_id, solde_disponible_cfa=0, solde_en_attente_cfa=0)
		return self.repo.creer_wallet(wallet)

	def _add_transaction(self, vendeur_id, commande_id, tx_type: TypeTransactionWallet, montant: int, commentaire: str | None = None):
		if montant < 0:
			raise ValueError("montant transaction négatif interdit")
		transaction = TransactionWallet(
			vendeur_identifiant=vendeur_id,
			commande_identifiant=commande_id,
			type=tx_type,
			montant_cfa=montant,
			commentaire=commentaire,
		)
		self.repo.ajouter_transaction(transaction)

	def _notifier_vendeur_wallet(self, vendeur_id, commande_id, titre: str, message: str):
		try:
			from MICROSERVICES.NOTIFICATION.models.notification import Notification, TypeNotification

			notification = Notification(
				utilisateur_identifiant=vendeur_id,
				type=TypeNotification.PAIEMENT_VENDEUR_RECU,
				titre=titre,
				message=message,
				lien=f"/vendeur/wallet?commande={commande_id}",
			)
			self.db.add(notification)
		except Exception:
			# La notification ne doit jamais bloquer la logique financière.
			pass

	def _montant_verse_pour_commande(self, vendeur_id, commande_id) -> int:
		transactions = self.repo.lister_transactions_vendeur(vendeur_id, limite=1000)
		return sum(
			int(tx.montant_cfa)
			for tx in transactions
			if str(tx.commande_identifiant) == str(commande_id)
			and tx.type == TypeTransactionWallet.PAIEMENT_EFFECTUE
			and int(tx.montant_cfa) > 0
		)

	def _date_dernier_type_tx(self, vendeur_id, commande_id, tx_type: TypeTransactionWallet):
		transactions = self.repo.lister_transactions_vendeur(vendeur_id, limite=1000)
		candidates = [
			tx.date_creation
			for tx in transactions
			if str(tx.commande_identifiant) == str(commande_id) and tx.type == tx_type
		]
		return max(candidates) if candidates else None

	def _statut_financier_vendeur(self, reservation, montant_verse: int) -> str:
		if montant_verse >= int(reservation.montant_total_net_cfa):
			return "VERSE"
		if reservation.statut in {StatutReservationWallet.PARTIELLEMENT_LIBEREE, StatutReservationWallet.LIBEREE}:
			return "CONFIRME"
		if reservation.statut == StatutReservationWallet.ANNULEE:
			return "ANNULE"
		return "EN_ATTENTE"

	def _credit_en_attente_si_absent(self, commande: Commande):
		groupes = defaultdict(int)
		for article in commande.articles:
			groupes[article.vendeur_identifiant] += int(article.total_ligne_cfa)

		for vendeur_id, brut_vendeur in groupes.items():
			reservation = self.repo.get_reservation(vendeur_id, commande.identifiant)
			if reservation:
				continue

			net_vendeur = max(0, round(brut_vendeur * (1.0 - settings.commission_percent)))
			wallet = self._get_or_create_wallet(vendeur_id)
			wallet.solde_en_attente_cfa = int(wallet.solde_en_attente_cfa) + net_vendeur

			reservation = WalletReservationCommande(
				vendeur_identifiant=vendeur_id,
				commande_identifiant=commande.identifiant,
				montant_total_net_cfa=net_vendeur,
				montant_en_attente_restant_cfa=net_vendeur,
				montant_avance_debloque_cfa=0,
				montant_solde_debloque_cfa=0,
				statut=StatutReservationWallet.EN_ATTENTE,
			)
			self.repo.creer_reservation(reservation)
			self._add_transaction(
				vendeur_id,
				commande.identifiant,
				TypeTransactionWallet.CREDIT_ATTENTE,
				net_vendeur,
				commentaire="Commande payée: crédit en attente",
			)
		self.db.flush()

	def _liberer_avance_expediee(self, commande_id):
		reservations = self.repo.lister_reservations_commande(commande_id)
		for reservation in reservations:
			if reservation.montant_avance_debloque_cfa > 0 or reservation.statut == StatutReservationWallet.ANNULEE:
				continue

			avance = round(int(reservation.montant_total_net_cfa) * settings.avance_percent_expediee)
			avance = max(0, min(avance, int(reservation.montant_en_attente_restant_cfa)))
			if avance == 0:
				continue

			wallet = self._get_or_create_wallet(reservation.vendeur_identifiant)
			wallet.solde_en_attente_cfa = max(0, int(wallet.solde_en_attente_cfa) - avance)
			wallet.solde_disponible_cfa = int(wallet.solde_disponible_cfa) + avance

			restant = int(reservation.montant_en_attente_restant_cfa) - avance
			statut = StatutReservationWallet.PARTIELLEMENT_LIBEREE if restant > 0 else StatutReservationWallet.LIBEREE
			self.repo.maj_reservation(
				reservation,
				{
					"montant_avance_debloque_cfa": avance,
					"montant_en_attente_restant_cfa": restant,
					"statut": statut,
				},
			)

			self._add_transaction(
				reservation.vendeur_identifiant,
				reservation.commande_identifiant,
				TypeTransactionWallet.DEBIT_ATTENTE,
				avance,
				commentaire="Commande expédiée: déblocage avance",
			)
			self._add_transaction(
				reservation.vendeur_identifiant,
				reservation.commande_identifiant,
				TypeTransactionWallet.CREDIT_DISPONIBLE,
				avance,
				commentaire="Commande expédiée: avance disponible",
			)
			self._notifier_vendeur_wallet(
				reservation.vendeur_identifiant,
				reservation.commande_identifiant,
				"Avance vendeur débloquée",
				f"Une avance de {avance} FCFA est disponible suite à l'expédition logistique.",
			)
		self.db.flush()

	def _liberer_solde_livree(self, commande_id):
		reservations = self.repo.lister_reservations_commande(commande_id)
		for reservation in reservations:
			if reservation.statut == StatutReservationWallet.ANNULEE:
				continue

			restant = int(reservation.montant_en_attente_restant_cfa)
			if restant <= 0:
				if reservation.statut != StatutReservationWallet.LIBEREE:
					self.repo.maj_reservation(reservation, {"statut": StatutReservationWallet.LIBEREE})
				continue

			wallet = self._get_or_create_wallet(reservation.vendeur_identifiant)
			wallet.solde_en_attente_cfa = max(0, int(wallet.solde_en_attente_cfa) - restant)
			wallet.solde_disponible_cfa = int(wallet.solde_disponible_cfa) + restant

			self.repo.maj_reservation(
				reservation,
				{
					"montant_solde_debloque_cfa": int(reservation.montant_solde_debloque_cfa) + restant,
					"montant_en_attente_restant_cfa": 0,
					"statut": StatutReservationWallet.LIBEREE,
				},
			)

			self._add_transaction(
				reservation.vendeur_identifiant,
				reservation.commande_identifiant,
				TypeTransactionWallet.DEBIT_ATTENTE,
				restant,
				commentaire="Commande livrée: solde débloqué",
			)
			self._add_transaction(
				reservation.vendeur_identifiant,
				reservation.commande_identifiant,
				TypeTransactionWallet.CREDIT_DISPONIBLE,
				restant,
				commentaire="Commande livrée: solde disponible",
			)
			self._notifier_vendeur_wallet(
				reservation.vendeur_identifiant,
				reservation.commande_identifiant,
				"Solde vendeur débloqué",
				f"Le solde final de {restant} FCFA est disponible après la livraison client.",
			)
		self.db.flush()

	def _annuler_attente(self, commande_id, statut: StatutCommande):
		reservations = self.repo.lister_reservations_commande(commande_id)
		for reservation in reservations:
			if reservation.statut == StatutReservationWallet.ANNULEE:
				continue

			restant = int(reservation.montant_en_attente_restant_cfa)
			if restant > 0:
				wallet = self._get_or_create_wallet(reservation.vendeur_identifiant)
				wallet.solde_en_attente_cfa = max(0, int(wallet.solde_en_attente_cfa) - restant)
				self._add_transaction(
					reservation.vendeur_identifiant,
					reservation.commande_identifiant,
					TypeTransactionWallet.DEBIT_ATTENTE,
					restant,
					commentaire=f"{statut.value}: annulation solde en attente",
				)

			statut_reservation = StatutReservationWallet.ANNULEE
			if int(reservation.montant_avance_debloque_cfa) > 0:
				self._add_transaction(
					reservation.vendeur_identifiant,
					reservation.commande_identifiant,
					TypeTransactionWallet.PAIEMENT_EFFECTUE,
					0,
					commentaire=f"{statut.value}: avance déjà débloquée, litige/politique requise",
				)

			self.repo.maj_reservation(
				reservation,
				{
					"montant_en_attente_restant_cfa": 0,
					"statut": statut_reservation,
				},
			)
		self.db.flush()

	def traiter_evenement_commande(self, commande_id, nouveau_statut: StatutCommande, source: str | None = None):
		commande = self.db.query(Commande).filter(Commande.identifiant == commande_id).first()
		if not commande:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande introuvable pour wallet vendeur")

		if nouveau_statut == StatutCommande.PAYEE:
			self._credit_en_attente_si_absent(commande)
		elif nouveau_statut == StatutCommande.EXPEDIEE:
			self._liberer_avance_expediee(commande.identifiant)
		elif nouveau_statut == StatutCommande.LIVREE:
			self._liberer_solde_livree(commande.identifiant)
		elif nouveau_statut in {StatutCommande.ANNULEE, StatutCommande.REMBOURSEE}:
			self._annuler_attente(commande.identifiant, nouveau_statut)

		return {
			"message": f"Wallet vendeurs synchronisé pour commande {commande.identifiant} ({nouveau_statut.value})"
		}

	def wallet_vendeur(self, vendeur_id):
		wallet = self._get_or_create_wallet(vendeur_id)
		reservations = self.repo.lister_reservations_vendeur(vendeur_id)
		transactions = self.repo.lister_transactions_vendeur(vendeur_id)
		return {
			"wallet": wallet,
			"reservations": reservations,
			"transactions": transactions,
		}

	def _liberer_avance_expedition_vendeur(self, commande_id, reception_id=None):
		"""
		Libère l'avance (20%) lorsque le vendeur signale l'expédition avec un tracking valide.
		Appelé après EXPEDIE_PAR_VENDEUR dans logistique_service.
		"""
		reservations = self.repo.lister_reservations_commande(commande_id)
		for reservation in reservations:
			if reservation.montant_avance_debloque_cfa > 0 or reservation.statut == StatutReservationWallet.ANNULEE:
				continue

			avance = round(int(reservation.montant_total_net_cfa) * settings.avance_percent_expedition_vendeur)
			avance = max(0, min(avance, int(reservation.montant_en_attente_restant_cfa)))
			if avance == 0:
				continue

			wallet = self._get_or_create_wallet(reservation.vendeur_identifiant)
			wallet.solde_en_attente_cfa = max(0, int(wallet.solde_en_attente_cfa) - avance)
			wallet.solde_disponible_cfa = int(wallet.solde_disponible_cfa) + avance

			restant = int(reservation.montant_en_attente_restant_cfa) - avance
			statut = StatutReservationWallet.PARTIELLEMENT_LIBEREE if restant > 0 else StatutReservationWallet.LIBEREE
			self.repo.maj_reservation(
				reservation,
				{
					"montant_avance_debloque_cfa": avance,
					"montant_en_attente_restant_cfa": restant,
					"statut": statut,
				},
			)

			self._add_transaction(
				reservation.vendeur_identifiant,
				reservation.commande_identifiant,
				TypeTransactionWallet.DEBIT_ATTENTE,
				avance,
				commentaire=f"Expédition vendeur: déblocage avance {int(settings.avance_percent_expedition_vendeur*100)}%",
			)
			self._add_transaction(
				reservation.vendeur_identifiant,
				reservation.commande_identifiant,
				TypeTransactionWallet.CREDIT_DISPONIBLE,
				avance,
				commentaire=f"Avance {int(settings.avance_percent_expedition_vendeur*100)}% disponible après tracking",
			)
			self._notifier_vendeur_wallet(
				reservation.vendeur_identifiant,
				reservation.commande_identifiant,
				"Avance débloquée",
				f"Avance de {avance} FCFA ({int(settings.avance_percent_expedition_vendeur*100)}%) débloquée suite à l'expédition validée.",
			)
		self.db.flush()

	def _liberer_solde_verification_agent(self, commande_id):
		"""
		Libère le solde (70%) lorsque l'agent logistique confirme la réception et vérifie le produit.
		Appelé après RECU_PAR_AGENT dans logistique_service.
		"""
		reservations = self.repo.lister_reservations_commande(commande_id)
		for reservation in reservations:
			if reservation.statut == StatutReservationWallet.ANNULEE:
				continue

			restant = int(reservation.montant_en_attente_restant_cfa)
			if restant <= 0:
				if reservation.statut != StatutReservationWallet.LIBEREE:
					self.repo.maj_reservation(reservation, {"statut": StatutReservationWallet.LIBEREE})
				continue

			wallet = self._get_or_create_wallet(reservation.vendeur_identifiant)
			wallet.solde_en_attente_cfa = max(0, int(wallet.solde_en_attente_cfa) - restant)
			wallet.solde_disponible_cfa = int(wallet.solde_disponible_cfa) + restant

			self.repo.maj_reservation(
				reservation,
				{
					"montant_solde_debloque_cfa": int(reservation.montant_solde_debloque_cfa) + restant,
					"montant_en_attente_restant_cfa": 0,
					"statut": StatutReservationWallet.LIBEREE,
				},
			)

			self._add_transaction(
				reservation.vendeur_identifiant,
				reservation.commande_identifiant,
				TypeTransactionWallet.DEBIT_ATTENTE,
				restant,
				commentaire=f"Vérification agent: déblocage solde {int(settings.solde_percent_verification_agent*100)}%",
			)
			self._add_transaction(
				reservation.vendeur_identifiant,
				reservation.commande_identifiant,
				TypeTransactionWallet.CREDIT_DISPONIBLE,
				restant,
				commentaire=f"Solde {int(settings.solde_percent_verification_agent*100)}% disponible après vérification",
			)
			self._notifier_vendeur_wallet(
				reservation.vendeur_identifiant,
				reservation.commande_identifiant,
				"Solde débloqué",
				f"Solde final de {restant} FCFA ({int(settings.solde_percent_verification_agent*100)}%) débloqué après vérification agent.",
			)
		self.db.flush()

	def traiter_evenement_logistique(self, commande_id, action: str, reception_id=None):
		"""
		Traite les événements logistiques pour libération progressive du paiement vendeur.
		
		Actions supportées:
		- EXPEDITION_VENDEUR: libère avance_percent_expedition_vendeur (20%) après tracking valide
		- VERIFICATION_AGENT: libère solde_percent_verification_agent (80%) après vérification
		"""
		if action == "EXPEDITION_VENDEUR":
			self._liberer_avance_expedition_vendeur(commande_id, reception_id)
			return {"message": f"Avance {int(settings.avance_percent_expedition_vendeur*100)}% libérée pour commande {commande_id}"}
		elif action == "VERIFICATION_AGENT":
			self._liberer_solde_verification_agent(commande_id)
			return {"message": f"Solde {int(settings.solde_percent_verification_agent*100)}% libéré pour commande {commande_id}"}
		else:
			raise ValueError(f"Action logistique inconnue: {action}")

	def mon_wallet(self, utilisateur_payload: dict):
		if utilisateur_payload.get("role") != RoleUtilisateur.VENDEUR.value:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Réservé aux vendeurs")
		dashboard = self.dashboard_financier_vendeur(utilisateur_payload)
		transactions = self.transactions_financieres_vendeur(utilisateur_payload, limite=50)
		return {
			"mes_revenus_cfa": int(dashboard["total_ventes_cfa"]),
			"montant_en_attente_cfa": int(dashboard["montant_en_attente_cfa"]),
			"montant_confirme_cfa": int(dashboard["montant_confirme_cfa"]),
			"montant_verse_cfa": int(dashboard["montant_verse_cfa"]),
			"historique_transactions": transactions["transactions"],
		}

	def dashboard_financier_vendeur(self, utilisateur_payload: dict):
		if utilisateur_payload.get("role") not in {RoleUtilisateur.VENDEUR.value, RoleUtilisateur.ADMINISTRATEUR.value}:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Réservé aux vendeurs")

		vendeur_id = utilisateur_payload.get("sub")
		reservations = self.repo.lister_reservations_vendeur(vendeur_id, limite=1000)

		total_ventes = sum(int(r.montant_total_net_cfa) for r in reservations)
		montant_en_attente = 0
		montant_confirme = 0
		montant_verse = 0

		for reservation in reservations:
			verse = self._montant_verse_pour_commande(vendeur_id, reservation.commande_identifiant)
			verse = min(verse, int(reservation.montant_total_net_cfa))
			montant_verse += verse

			restant_non_verse = max(0, int(reservation.montant_total_net_cfa) - verse)
			if reservation.statut in {StatutReservationWallet.PARTIELLEMENT_LIBEREE, StatutReservationWallet.LIBEREE}:
				montant_confirme += restant_non_verse
			elif reservation.statut == StatutReservationWallet.EN_ATTENTE:
				montant_en_attente += restant_non_verse

		return {
			"total_ventes_cfa": total_ventes,
			"montant_en_attente_cfa": montant_en_attente,
			"montant_confirme_cfa": montant_confirme,
			"montant_verse_cfa": montant_verse,
		}

	def transactions_financieres_vendeur(self, utilisateur_payload: dict, statut: str | None = None, limite: int = 100):
		if utilisateur_payload.get("role") not in {RoleUtilisateur.VENDEUR.value, RoleUtilisateur.ADMINISTRATEUR.value}:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Réservé aux vendeurs")

		vendeur_id = utilisateur_payload.get("sub")
		reservations = self.repo.lister_reservations_vendeur(vendeur_id, limite=1000)
		items = []

		for reservation in reservations:
			commande = self.db.query(Commande).filter(Commande.identifiant == reservation.commande_identifiant).first()
			if not commande:
				continue

			articles = (
				self.db.query(CommandeArticle)
				.filter(
					CommandeArticle.commande_identifiant == commande.identifiant,
					CommandeArticle.vendeur_identifiant == vendeur_id,
				)
				.all()
			)
			if not articles:
				continue

			montant_verse_commande = self._montant_verse_pour_commande(vendeur_id, commande.identifiant)
			statut_financier = self._statut_financier_vendeur(reservation, montant_verse_commande)
			if statut and statut_financier != statut.upper():
				continue

			date_confirmation = self._date_dernier_type_tx(vendeur_id, commande.identifiant, TypeTransactionWallet.CREDIT_DISPONIBLE)
			date_versement = self._date_dernier_type_tx(vendeur_id, commande.identifiant, TypeTransactionWallet.PAIEMENT_EFFECTUE)

			for article in articles:
				produit = self.db.query(Produit).filter(Produit.identifiant == article.produit_identifiant).first()
				produit_nom = produit.nom if produit else "Produit"
				montant_vendeur = max(0, round(int(article.total_ligne_cfa) * (1.0 - settings.commission_percent)))

				items.append(
					{
						"commande_identifiant": commande.identifiant,
						"article_identifiant": article.identifiant,
						"produit_identifiant": article.produit_identifiant,
						"produit_nom": produit_nom,
						"quantite": int(article.quantite),
						"montant_vendeur_cfa": int(montant_vendeur),
						"statut_financier": statut_financier,
						"date_commande": commande.date_creation,
						"date_confirmation": date_confirmation,
						"date_versement": date_versement,
					}
				)

		items = sorted(items, key=lambda x: x["date_commande"], reverse=True)[:limite]
		return {"transactions": items, "total": len(items)}

	def enregistrer_versement_admin(self, payload):
		commande = self.db.query(Commande).filter(Commande.identifiant == payload.commande_identifiant).first()
		if not commande:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande introuvable")

		reservations = self.repo.lister_reservations_commande(commande.identifiant)
		if not reservations:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune réservation vendeur pour cette commande")

		reservation = None
		if payload.vendeur_identifiant:
			for r in reservations:
				if str(r.vendeur_identifiant) == str(payload.vendeur_identifiant):
					reservation = r
					break
			if reservation is None:
				raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Réservation vendeur introuvable pour cette commande")
		elif len(reservations) == 1:
			reservation = reservations[0]
		else:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Commande multi-vendeurs: vendeur_identifiant est obligatoire pour enregistrer un versement",
			)
		if payload.montant_cfa <= 0:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Montant de versement invalide")

		montant_verse = self._montant_verse_pour_commande(reservation.vendeur_identifiant, commande.identifiant)
		restant = max(0, int(reservation.montant_total_net_cfa) - montant_verse)
		montant = min(int(payload.montant_cfa), restant)
		if montant <= 0:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Commande déjà totalement versée")

		commentaire = "Versement vendeur validé"
		if payload.reference_versement:
			commentaire = f"Versement vendeur validé - ref: {payload.reference_versement}"

		self._add_transaction(
			reservation.vendeur_identifiant,
			commande.identifiant,
			TypeTransactionWallet.PAIEMENT_EFFECTUE,
			montant,
			commentaire=commentaire,
		)
		self.db.flush()

		return {
			"message": "Versement enregistré",
			"vendeur_identifiant": reservation.vendeur_identifiant,
			"commande_identifiant": commande.identifiant,
			"montant_cfa": montant,
		}
