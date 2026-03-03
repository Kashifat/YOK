from sqlalchemy.orm import Session

from ..models.commande import Commande, CommandeArticle


class CommandeRepository:
	def __init__(self, db: Session):
		self.db = db

	def get_by_id(self, identifiant):
		"""Récupère une commande par ID."""
		return self.db.query(Commande).filter(Commande.identifiant == identifiant).first()

	def lister_par_client(self, client_id):
		"""Liste toutes les commandes d'un client."""
		return self.db.query(Commande).filter(Commande.client_identifiant == client_id).order_by(Commande.date_creation.desc()).all()

	def lister_par_vendeur(self, vendeur_id):
		"""Liste toutes les commandes contenant des produits d'un vendeur."""
		return self.db.query(Commande).join(CommandeArticle).filter(
			CommandeArticle.vendeur_identifiant == vendeur_id
		).order_by(Commande.date_creation.desc()).all()

	def lister_toutes(self, limite: int = 100, offset: int = 0):
		"""Liste toutes les commandes (admin)."""
		return self.db.query(Commande).order_by(Commande.date_creation.desc()).limit(limite).offset(offset).all()

	def creer(self, commande: Commande):
		"""Crée une nouvelle commande."""
		self.db.add(commande)
		self.db.flush()
		return commande

	def ajouter_article(self, article: CommandeArticle):
		"""Ajoute un article à une commande."""
		self.db.add(article)
		self.db.flush()
		return article

	def maj(self, commande: Commande, donnees: dict):
		"""Met à jour une commande."""
		for cle, valeur in donnees.items():
			setattr(commande, cle, valeur)
		self.db.flush()
		return commande

	def get_article_by_id(self, article_id):
		"""Récupère un article de commande par ID."""
		return self.db.query(CommandeArticle).filter(CommandeArticle.identifiant == article_id).first()

	def maj_article_statut(self, article: CommandeArticle, statut):
		"""Met à jour le statut d'un article."""
		article.statut = statut
		self.db.flush()
		return article
