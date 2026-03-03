from collections import defaultdict

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur
from MICROSERVICES.COMMANDE.models.commande import Commande, CommandeArticle, StatutCommande

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

	def mon_wallet(self, utilisateur_payload: dict):
		if utilisateur_payload.get("role") != RoleUtilisateur.VENDEUR.value:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Réservé aux vendeurs")
		return self.wallet_vendeur(utilisateur_payload.get("sub"))
