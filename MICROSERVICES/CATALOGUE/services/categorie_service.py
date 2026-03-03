from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.categorie import Categorie
from ..respositories.categorie_repository import CategorieRepository
from ..schemas.categorie import CategorieCreate, CategorieUpdate


class CategorieService:
	def __init__(self, db: Session):
		self.db = db
		self.repo = CategorieRepository(db)

	def lister_actives(self):
		return self.repo.lister_actives()

	def lister_toutes(self):
		return self.repo.lister_toutes()

	def obtenir(self, identifiant):
		categorie = self.repo.get_by_id(identifiant)
		if not categorie:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Catégorie introuvable")
		return categorie

	def creer(self, payload: CategorieCreate):
		if self.repo.get_by_nom(payload.nom):
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nom déjà utilisé")

		categorie = Categorie(
			nom=payload.nom,
			parent_identifiant=payload.parent_identifiant,
			description=payload.description,
		)
		return self.repo.creer(categorie)

	def maj(self, identifiant, payload: CategorieUpdate):
		categorie = self.obtenir(identifiant)
		donnees = payload.model_dump(exclude_unset=True)
		if "nom" in donnees:
			existante = self.repo.get_by_nom(donnees["nom"])
			if existante and existante.identifiant != identifiant:
				raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nom déjà utilisé")
		return self.repo.maj(categorie, donnees)

	def desactiver(self, identifiant):
		categorie = self.obtenir(identifiant)
		return self.repo.maj(categorie, {"est_actif": False})