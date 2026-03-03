from sqlalchemy.orm import Session

from ..models.categorie import Categorie


class CategorieRepository:
	def __init__(self, db: Session):
		self.db = db

	def get_by_id(self, identifiant):
		return self.db.query(Categorie).filter(Categorie.identifiant == identifiant).first()

	def get_by_nom(self, nom: str):
		return self.db.query(Categorie).filter(Categorie.nom == nom).first()

	def lister_actives(self):
		return self.db.query(Categorie).filter(Categorie.est_actif.is_(True)).all()

	def lister_toutes(self):
		return self.db.query(Categorie).all()

	def creer(self, categorie: Categorie):
		self.db.add(categorie)
		self.db.flush()
		return categorie

	def maj(self, categorie: Categorie, donnees: dict):
		for cle, valeur in donnees.items():
			setattr(categorie, cle, valeur)
		self.db.flush()
		return categorie