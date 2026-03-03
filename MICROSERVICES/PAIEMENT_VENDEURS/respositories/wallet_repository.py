from sqlalchemy.orm import Session

from ..models.wallet import TransactionWallet, WalletReservationCommande, WalletVendeur


class WalletRepository:
	def __init__(self, db: Session):
		self.db = db

	def get_wallet(self, vendeur_id):
		return self.db.query(WalletVendeur).filter(WalletVendeur.vendeur_identifiant == vendeur_id).first()

	def creer_wallet(self, wallet: WalletVendeur):
		self.db.add(wallet)
		self.db.flush()
		self.db.refresh(wallet)
		return wallet

	def get_reservation(self, vendeur_id, commande_id):
		return (
			self.db.query(WalletReservationCommande)
			.filter(
				WalletReservationCommande.vendeur_identifiant == vendeur_id,
				WalletReservationCommande.commande_identifiant == commande_id,
			)
			.first()
		)

	def lister_reservations_vendeur(self, vendeur_id, limite: int = 100):
		return (
			self.db.query(WalletReservationCommande)
			.filter(WalletReservationCommande.vendeur_identifiant == vendeur_id)
			.order_by(WalletReservationCommande.date_creation.desc())
			.limit(limite)
			.all()
		)

	def lister_reservations_commande(self, commande_id):
		return (
			self.db.query(WalletReservationCommande)
			.filter(WalletReservationCommande.commande_identifiant == commande_id)
			.all()
		)

	def creer_reservation(self, reservation: WalletReservationCommande):
		self.db.add(reservation)
		self.db.flush()
		self.db.refresh(reservation)
		return reservation

	def maj_reservation(self, reservation: WalletReservationCommande, donnees: dict):
		for cle, valeur in donnees.items():
			setattr(reservation, cle, valeur)
		self.db.flush()
		self.db.refresh(reservation)
		return reservation

	def ajouter_transaction(self, transaction: TransactionWallet):
		self.db.add(transaction)
		self.db.flush()
		self.db.refresh(transaction)
		return transaction

	def lister_transactions_vendeur(self, vendeur_id, limite: int = 200):
		return (
			self.db.query(TransactionWallet)
			.filter(TransactionWallet.vendeur_identifiant == vendeur_id)
			.order_by(TransactionWallet.date_creation.desc())
			.limit(limite)
			.all()
		)
