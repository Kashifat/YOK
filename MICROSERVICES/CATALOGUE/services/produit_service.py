from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import re
import unicodedata

from ..models.produit import Produit
from ..models.media import ImageProduit, VideoProduit
from ..respositories.produit_repository import ProduitRepository
from ..respositories.media_repository import MediaRepository
from ..respositories.categorie_repository import CategorieRepository
from ..schemas.produit import ProduitCreate, ProduitUpdate
from ..schemas.media import ImageCreate, VideoCreate


class ProduitService:
	def __init__(self, db: Session):
		self.db = db
		self.repo = ProduitRepository(db)
		self.media_repo = MediaRepository(db)
		self.cat_repo = CategorieRepository(db)

	@staticmethod
	def _slugifier(valeur: str) -> str:
		valeur_ascii = unicodedata.normalize("NFKD", valeur).encode("ascii", "ignore").decode("ascii")
		slug = re.sub(r"[^a-zA-Z0-9]+", "-", valeur_ascii.lower()).strip("-")
		return slug or "produit"

	def lister_public(self, categorie_id=None):
		return self.repo.lister_public(categorie_id=categorie_id)

	def obtenir_public(self, identifiant):
		produit = self.repo.get_by_id(identifiant)
		if not produit or not produit.est_actif:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit introuvable")
		return produit

	def lister_vendeur(self, vendeur_id):
		return self.repo.lister_vendeur(vendeur_id)

	def creer(self, vendeur_id, payload: ProduitCreate):
		categorie = self.cat_repo.get_by_id(payload.categorie_identifiant)
		if not categorie or not categorie.est_actif:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Catégorie invalide")

		produit = Produit(
			vendeur_identifiant=vendeur_id,
			categorie_identifiant=payload.categorie_identifiant,
			nom=payload.nom,
			description=payload.description,
			prix_cfa=payload.prix_cfa,
			stock=payload.stock,
			tailles=payload.tailles,
			couleurs=payload.couleurs,
			slug=payload.slug or self._slugifier(payload.nom),
			mots_cles=payload.mots_cles,
			marque=payload.marque,
			origine_pays=payload.origine_pays,
		)
		return self.repo.creer(produit)

	def maj(self, identifiant, vendeur_id, est_admin: bool, payload: ProduitUpdate):
		produit = self.repo.get_by_id(identifiant)
		if not produit:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit introuvable")
		if not est_admin and str(produit.vendeur_identifiant) != str(vendeur_id):
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

		donnees = payload.model_dump(exclude_unset=True)
		if "categorie_identifiant" in donnees:
			categorie = self.cat_repo.get_by_id(donnees["categorie_identifiant"])
			if not categorie or not categorie.est_actif:
				raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Catégorie invalide")
		if "nom" in donnees and "slug" not in donnees and not produit.slug:
			donnees["slug"] = self._slugifier(donnees["nom"])
		if "slug" in donnees and donnees["slug"]:
			donnees["slug"] = self._slugifier(donnees["slug"])

		return self.repo.maj(produit, donnees)

	def desactiver(self, identifiant, vendeur_id, est_admin: bool):
		produit = self.repo.get_by_id(identifiant)
		if not produit:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit introuvable")
		if not est_admin and str(produit.vendeur_identifiant) != str(vendeur_id):
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
		return self.repo.maj(produit, {"est_actif": False})

	def ajouter_image(self, produit_id, vendeur_id, est_admin: bool, payload: ImageCreate):
		produit = self.repo.get_by_id(produit_id)
		if not produit:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit introuvable")
		if not est_admin and str(produit.vendeur_identifiant) != str(vendeur_id):
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

		image = ImageProduit(
			produit_identifiant=produit_id,
			url_image=payload.url_image,
			position=payload.position,
		)
		return self.media_repo.ajouter_image(image)

	def ajouter_video(self, produit_id, vendeur_id, est_admin: bool, payload: VideoCreate):
		produit = self.repo.get_by_id(produit_id)
		if not produit:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit introuvable")
		if not est_admin and str(produit.vendeur_identifiant) != str(vendeur_id):
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

		video = VideoProduit(
			produit_identifiant=produit_id,
			url_video=payload.url_video,
			position=payload.position,
		)
		return self.media_repo.ajouter_video(video)

	def rechercher_public(self, terme: str):
		"""Rechercher des produits actifs par nom ou description"""
		from sqlalchemy import or_
		return self.db.query(Produit).filter(
			Produit.est_actif == True,
			or_(
				Produit.nom.ilike(f"%{terme}%"),
				Produit.description.ilike(f"%{terme}%"),
				Produit.slug.ilike(f"%{terme}%")
			)
		).all()