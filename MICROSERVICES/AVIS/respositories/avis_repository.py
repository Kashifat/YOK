from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models.avis import Avis


class AvisRepository:
	def __init__(self, db: Session):
		self.db = db

	def get_by_id(self, identifiant):
		return self.db.query(Avis).filter(Avis.identifiant == identifiant).first()

	def lister_par_produit(self, produit_id):
		"""Liste tous les avis d'un produit."""
		return self.db.query(Avis).filter(Avis.produit_identifiant == produit_id).all()

	def lister_par_client(self, client_id):
		"""Liste tous les avis d'un client."""
		return self.db.query(Avis).filter(Avis.client_identifiant == client_id).all()

	def get_avis_client_produit(self, client_id, produit_id):
		"""Vérifie si un client a déjà laissé un avis pour un produit."""
		return self.db.query(Avis).filter(
			and_(
				Avis.client_identifiant == client_id,
				Avis.produit_identifiant == produit_id
			)
		).first()

	def creer(self, avis: Avis):
		self.db.add(avis)
		self.db.flush()
		return avis

	def maj(self, avis: Avis, donnees: dict):
		for cle, valeur in donnees.items():
			setattr(avis, cle, valeur)
		self.db.flush()
		return avis

	def supprimer(self, avis: Avis):
		self.db.delete(avis)
		self.db.flush()
