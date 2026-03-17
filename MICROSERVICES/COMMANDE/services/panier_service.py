from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.panier import Panier, PanierArticle
from ..respositories.panier_repository import PanierRepository
from ..schemas.panier import PanierArticleCreate, PanierArticleUpdate


class PanierService:
	def __init__(self, db: Session):
		self.db = db
		self.repo = PanierRepository(db)

	def _verifier_variante(self, produit, variante_id):
		if variante_id is None:
			return None

		from MICROSERVICES.CATALOGUE.models.produit import VariantProduit

		variante = self.db.query(VariantProduit).filter(
			VariantProduit.identifiant == variante_id,
			VariantProduit.produit_identifiant == produit.identifiant,
			VariantProduit.est_actif.is_(True),
		).first()
		if not variante:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Variante introuvable pour ce produit",
			)
		return variante

	@staticmethod
	def _stock_disponible(produit, variante):
		if variante is None:
			return produit.stock
		return min(produit.stock, variante.stock)

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

		variante = self._verifier_variante(produit, payload.variante_identifiant)

		# Vérifier le stock
		if self._stock_disponible(produit, variante) < payload.quantite:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f"Stock insuffisant (disponible: {self._stock_disponible(produit, variante)})"
			)

		panier = self.repo.get_ou_creer_panier(utilisateur_id)
		return self.repo.ajouter_article(
			panier.identifiant,
			payload.produit_identifiant,
			payload.quantite,
			payload.variante_identifiant,
		)

	def maj_quantite(self, utilisateur_id, produit_id, payload: PanierArticleUpdate, variante_id=None):
		"""Met à jour la quantité d'un article."""
		panier = self.repo.get_by_utilisateur(utilisateur_id)
		if not panier:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Panier introuvable"
			)

		article = self.repo.get_article(panier.identifiant, produit_id, variante_id)
		if not article:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Article introuvable dans le panier"
			)

		# Vérifier le stock
		from MICROSERVICES.CATALOGUE.models.produit import Produit
		produit = self.db.query(Produit).filter(Produit.identifiant == produit_id).first()
		variante = self._verifier_variante(produit, article.variante_identifiant) if produit else None
		if produit and self._stock_disponible(produit, variante) < payload.quantite:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f"Stock insuffisant (disponible: {self._stock_disponible(produit, variante)})"
			)

		return self.repo.maj_quantite(article, payload.quantite)

	def supprimer_article(self, utilisateur_id, produit_id, variante_id=None):
		"""Supprime un article du panier."""
		panier = self.repo.get_by_utilisateur(utilisateur_id)
		if not panier:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Panier introuvable"
			)

		article = self.repo.get_article(panier.identifiant, produit_id, variante_id)
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
