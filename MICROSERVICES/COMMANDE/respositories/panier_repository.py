from sqlalchemy.orm import Session

from ..models.panier import Panier, PanierArticle


class PanierRepository:
	def __init__(self, db: Session):
		self.db = db

	def get_by_utilisateur(self, utilisateur_id):
		"""Récupère le panier d'un utilisateur (ou None)."""
		return self.db.query(Panier).filter(Panier.utilisateur_identifiant == utilisateur_id).first()

	def creer_panier(self, utilisateur_id):
		"""Crée un nouveau panier pour un utilisateur."""
		panier = Panier(utilisateur_identifiant=utilisateur_id)
		self.db.add(panier)
		self.db.flush()
		return panier

	def get_ou_creer_panier(self, utilisateur_id):
		"""Récupère le panier ou le crée s'il n'existe pas."""
		panier = self.get_by_utilisateur(utilisateur_id)
		if not panier:
			panier = self.creer_panier(utilisateur_id)
		return panier

	def get_article(self, panier_id, produit_id):
		"""Récupère un article du panier."""
		return self.db.query(PanierArticle).filter(
			PanierArticle.panier_identifiant == panier_id,
			PanierArticle.produit_identifiant == produit_id
		).first()

	def ajouter_article(self, panier_id, produit_id, quantite):
		"""Ajoute un article au panier (ou met à jour la quantité)."""
		article = self.get_article(panier_id, produit_id)
		if article:
			article.quantite += quantite
		else:
			article = PanierArticle(
				panier_identifiant=panier_id,
				produit_identifiant=produit_id,
				quantite=quantite
			)
			self.db.add(article)
		self.db.flush()
		return article

	def maj_quantite(self, article: PanierArticle, quantite: int):
		"""Met à jour la quantité d'un article."""
		article.quantite = quantite
		self.db.flush()
		return article

	def supprimer_article(self, article: PanierArticle):
		"""Supprime un article du panier."""
		self.db.delete(article)
		self.db.flush()

	def vider_panier(self, panier: Panier):
		"""Vide tous les articles du panier."""
		self.db.query(PanierArticle).filter(PanierArticle.panier_identifiant == panier.identifiant).delete()
		self.db.flush()
