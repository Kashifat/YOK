from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from ..models.social import (
	ReseauCommentaire,
	ReseauCommentaireLike,
	ReseauLike,
	ReseauPartage,
	ReseauPost,
	ReseauPostImage,
	ReseauPostTagProduit,
	StatutModerationCommentaire,
	StatutModerationPost,
)


class SocialRepository:
	def __init__(self, db: Session):
		self.db = db

	def creer_post(self, post: ReseauPost):
		self.db.add(post)
		self.db.flush()
		self.db.refresh(post)
		return post

	def ajouter_image(self, image: ReseauPostImage):
		self.db.add(image)
		self.db.flush()
		return image

	def ajouter_tag(self, tag: ReseauPostTagProduit):
		self.db.add(tag)
		self.db.flush()
		return tag

	def get_post(self, post_id):
		return self.db.query(ReseauPost).filter(ReseauPost.identifiant == post_id).first()

	def lister_posts_actifs(self, limite: int = 20, offset: int = 0):
		return (
			self.db.query(ReseauPost)
			.filter(ReseauPost.statut_moderation == StatutModerationPost.ACTIF)
			.order_by(ReseauPost.date_creation.desc())
			.limit(limite)
			.offset(offset)
			.all()
		)

	def lister_posts_auteur(self, auteur_id, limite: int = 20, offset: int = 0):
		return (
			self.db.query(ReseauPost)
			.filter(ReseauPost.auteur_identifiant == auteur_id)
			.order_by(ReseauPost.date_creation.desc())
			.limit(limite)
			.offset(offset)
			.all()
		)

	def lister_posts_tous(self, limite: int = 50, offset: int = 0, statut: StatutModerationPost | None = None):
		requete = self.db.query(ReseauPost)
		if statut is not None:
			requete = requete.filter(ReseauPost.statut_moderation == statut)
		return requete.order_by(ReseauPost.date_creation.desc()).limit(limite).offset(offset).all()

	def maj_post(self, post: ReseauPost, donnees: dict):
		for cle, valeur in donnees.items():
			setattr(post, cle, valeur)
		self.db.flush()
		self.db.refresh(post)
		return post

	def supprimer_post(self, post: ReseauPost):
		self.db.delete(post)
		self.db.flush()

	def ajouter_commentaire(self, commentaire: ReseauCommentaire):
		self.db.add(commentaire)
		self.db.flush()
		self.db.refresh(commentaire)
		return commentaire

	def get_commentaire(self, commentaire_id):
		return self.db.query(ReseauCommentaire).filter(ReseauCommentaire.identifiant == commentaire_id).first()

	def lister_commentaires_post(self, post_id, inclure_non_actifs: bool = False, tri: str = "likes", limite: int = 100, offset: int = 0):
		requete = self.db.query(ReseauCommentaire)
		if not inclure_non_actifs:
			requete = requete.filter(ReseauCommentaire.statut_moderation == StatutModerationCommentaire.ACTIF)
		requete = requete.filter(ReseauCommentaire.post_identifiant == post_id)

		if tri == "likes":
			requete = (
				requete.outerjoin(
					ReseauCommentaireLike,
					ReseauCommentaireLike.commentaire_identifiant == ReseauCommentaire.identifiant,
				)
				.group_by(ReseauCommentaire.identifiant)
				.order_by(desc(func.count(ReseauCommentaireLike.identifiant)), desc(ReseauCommentaire.date_creation))
			)
		else:
			requete = requete.order_by(desc(ReseauCommentaire.date_creation))

		return requete.limit(limite).offset(offset).all()

	def lister_commentaires_tous(self, limite: int = 100, offset: int = 0, statut: StatutModerationCommentaire | None = None):
		requete = self.db.query(ReseauCommentaire)
		if statut is not None:
			requete = requete.filter(ReseauCommentaire.statut_moderation == statut)
		return requete.order_by(desc(ReseauCommentaire.date_creation)).limit(limite).offset(offset).all()

	def maj_commentaire(self, commentaire: ReseauCommentaire, donnees: dict):
		for cle, valeur in donnees.items():
			setattr(commentaire, cle, valeur)
		self.db.flush()
		self.db.refresh(commentaire)
		return commentaire

	def supprimer_commentaire(self, commentaire: ReseauCommentaire):
		self.db.delete(commentaire)
		self.db.flush()

	def get_like_commentaire(self, commentaire_id, utilisateur_id):
		return (
			self.db.query(ReseauCommentaireLike)
			.filter(
				ReseauCommentaireLike.commentaire_identifiant == commentaire_id,
				ReseauCommentaireLike.utilisateur_identifiant == utilisateur_id,
			)
			.first()
		)

	def ajouter_like_commentaire(self, like_commentaire: ReseauCommentaireLike):
		self.db.add(like_commentaire)
		self.db.flush()
		return like_commentaire

	def supprimer_like_commentaire(self, like_commentaire: ReseauCommentaireLike):
		self.db.delete(like_commentaire)
		self.db.flush()

	def compter_likes_commentaire(self, commentaire_id):
		return self.db.query(ReseauCommentaireLike).filter(ReseauCommentaireLike.commentaire_identifiant == commentaire_id).count()

	def get_like(self, post_id, utilisateur_id):
		return (
			self.db.query(ReseauLike)
			.filter(
				ReseauLike.post_identifiant == post_id,
				ReseauLike.utilisateur_identifiant == utilisateur_id,
			)
			.first()
		)

	def ajouter_like(self, like: ReseauLike):
		self.db.add(like)
		self.db.flush()
		return like

	def supprimer_like(self, like: ReseauLike):
		self.db.delete(like)
		self.db.flush()

	def compter_likes(self, post_id):
		return self.db.query(ReseauLike).filter(ReseauLike.post_identifiant == post_id).count()

	def ajouter_partage(self, partage: ReseauPartage):
		self.db.add(partage)
		self.db.flush()
		return partage

	def compter_partages(self, post_id):
		return self.db.query(ReseauPartage).filter(ReseauPartage.post_identifiant == post_id).count()
