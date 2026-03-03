from sqlalchemy.orm import Session

from ..models.livraison import Livraison, LivraisonEvenement


class LivraisonRepository:
	def __init__(self, db: Session):
		self.db = db

	def get_by_id(self, livraison_id):
		return self.db.query(Livraison).filter(Livraison.identifiant == livraison_id).first()

	def get_by_commande(self, commande_id):
		return self.db.query(Livraison).filter(Livraison.commande_identifiant == commande_id).first()

	def creer(self, livraison: Livraison):
		self.db.add(livraison)
		self.db.flush()
		self.db.refresh(livraison)
		return livraison

	def maj(self, livraison: Livraison, donnees: dict):
		for cle, valeur in donnees.items():
			setattr(livraison, cle, valeur)
		self.db.flush()
		self.db.refresh(livraison)
		return livraison

	def ajouter_evenement(self, evenement: LivraisonEvenement):
		self.db.add(evenement)
		self.db.flush()
		self.db.refresh(evenement)
		return evenement
