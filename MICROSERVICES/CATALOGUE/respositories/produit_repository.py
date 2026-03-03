from sqlalchemy.orm import Session

from ..models.produit import Produit


class ProduitRepository:
	def __init__(self, db: Session):
		self.db = db

	def get_by_id(self, identifiant):
		return self.db.query(Produit).filter(Produit.identifiant == identifiant).first()

	def lister_public(self, categorie_id=None):
		requete = self.db.query(Produit).filter(Produit.est_actif.is_(True))
		if categorie_id:
			requete = requete.filter(Produit.categorie_identifiant == categorie_id)
		return requete.all()

	def lister_vendeur(self, vendeur_id):
		return self.db.query(Produit).filter(Produit.vendeur_identifiant == vendeur_id).all()

	def creer(self, produit: Produit):
		self.db.add(produit)
		self.db.flush()
		return produit

	def maj(self, produit: Produit, donnees: dict):
		for cle, valeur in donnees.items():
			setattr(produit, cle, valeur)
		self.db.flush()
		return produit

	def lister_tous(self):
		"""Lister tous les produits (pour admin)"""
		return self.db.query(Produit).all()