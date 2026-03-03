from sqlalchemy.orm import Session

from ..models.paiement import Paiement, PaiementEvenement


class PaiementRepository:
	def __init__(self, db: Session):
		self.db = db

	def get_by_id(self, paiement_id):
		return self.db.query(Paiement).filter(Paiement.identifiant == paiement_id).first()

	def get_by_commande(self, commande_id):
		return self.db.query(Paiement).filter(Paiement.commande_identifiant == commande_id).first()

	def get_by_provider_transaction_id(self, transaction_id: str):
		return self.db.query(Paiement).filter(Paiement.provider_transaction_id == transaction_id).first()

	def creer(self, paiement: Paiement):
		self.db.add(paiement)
		self.db.flush()
		self.db.refresh(paiement)
		return paiement

	def maj(self, paiement: Paiement, donnees: dict):
		for cle, valeur in donnees.items():
			setattr(paiement, cle, valeur)
		self.db.flush()
		self.db.refresh(paiement)
		return paiement

	def ajouter_evenement(self, evenement: PaiementEvenement):
		self.db.add(evenement)
		self.db.flush()
		return evenement
