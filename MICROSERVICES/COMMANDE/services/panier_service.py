from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.panier import Panier, PanierArticle
from ..respositories.panier_repository import PanierRepository
from ..schemas.panier import PanierArticleCreate, PanierArticleUpdate


class PanierService:
	def __init__(self, db: Session):
		self.db = db
		self.repo = PanierRepository(db)

	def obtenir_panier(self, utilisateur_id):
		"""Récupère ou crée le panier d'un utilisateur."""
		return self.repo.get_ou_creer_panier(utilisateur_id)

	def ajouter_article(self, utilisateur_id, payload: PanierArticleCreate):
		"""Ajoute un article au panier (ou incrémente la quantité)."""
		# Vérifier que le produit existe
		from MICROSERVICES.CATALOGUE.models.produit import Produit
		produit = self.db.query(Produit).filter(
			Produit.identifiant == payload.produit_identifiant,
			Produit.est_actif == True
		).first()
		if not produit:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Produit introuvable"
			)

		# Vérifier le stock
		if produit.stock < payload.quantite:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f"Stock insuffisant (disponible: {produit.stock})"
			)

		panier = self.repo.get_ou_creer_panier(utilisateur_id)
		return self.repo.ajouter_article(panier.identifiant, payload.produit_identifiant, payload.quantite)

	def maj_quantite(self, utilisateur_id, produit_id, payload: PanierArticleUpdate):
		"""Met à jour la quantité d'un article."""
		panier = self.repo.get_by_utilisateur(utilisateur_id)
		if not panier:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Panier introuvable"
			)

		article = self.repo.get_article(panier.identifiant, produit_id)
		if not article:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Article introuvable dans le panier"
			)

		# Vérifier le stock
		from MICROSERVICES.CATALOGUE.models.produit import Produit
		produit = self.db.query(Produit).filter(Produit.identifiant == produit_id).first()
		if produit and produit.stock < payload.quantite:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f"Stock insuffisant (disponible: {produit.stock})"
			)

		return self.repo.maj_quantite(article, payload.quantite)

	def supprimer_article(self, utilisateur_id, produit_id):
		"""Supprime un article du panier."""
		panier = self.repo.get_by_utilisateur(utilisateur_id)
		if not panier:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Panier introuvable"
			)

		article = self.repo.get_article(panier.identifiant, produit_id)
		if not article:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Article introuvable dans le panier"
			)

		self.repo.supprimer_article(article)
		return {"message": "Article supprimé du panier"}

	def vider_panier(self, utilisateur_id):
		"""Vide le panier."""
		panier = self.repo.get_by_utilisateur(utilisateur_id)
		if not panier:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Panier introuvable"
			)

		self.repo.vider_panier(panier)
		return {"message": "Panier vidé"}
