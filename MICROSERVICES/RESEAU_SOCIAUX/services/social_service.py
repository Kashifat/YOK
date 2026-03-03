from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from MICROSERVICES.CATALOGUE.models.produit import Produit
from MICROSERVICES.COMMANDE.models.commande import Commande, CommandeArticle, StatutCommande

from ..models.social import StatutModerationCommentaire, StatutModerationPost, ReseauCommentaire, ReseauCommentaireLike, ReseauLike, ReseauPartage, ReseauPost, ReseauPostImage, ReseauPostTagProduit
from ..respositories.social_repository import SocialRepository
from ..schemas.social import CommentaireCreate, PartageCreate, PostCreate, TriCommentaires


class SocialService:
	def __init__(self, db: Session):
		self.db = db
		self.repo = SocialRepository(db)

	def _produit_achete_par_client(self, client_id, produit_id) -> bool:
		achat = (
			self.db.query(CommandeArticle)
			.join(Commande, Commande.identifiant == CommandeArticle.commande_identifiant)
			.filter(
				Commande.client_identifiant == client_id,
				CommandeArticle.produit_identifiant == produit_id,
				Commande.statut.in_(
					[
						StatutCommande.PAYEE,
						StatutCommande.EN_PREPARATION,
						StatutCommande.EXPEDIEE,
						StatutCommande.LIVREE,
						StatutCommande.REMBOURSEE,
					]
				),
			)
			.first()
		)
		return achat is not None

	def _to_post_read(self, post):
		return {
			"identifiant": post.identifiant,
			"auteur_identifiant": post.auteur_identifiant,
			"contenu": post.contenu,
			"date_creation": post.date_creation,
			"images": post.images,
			"tags": post.tags,
			"nombre_commentaires": len(post.commentaires),
			"nombre_likes": len(post.likes),
			"nombre_partages": len(post.partages),
		}

	def creer_post(self, utilisateur_id, payload: PostCreate):
		post = ReseauPost(auteur_identifiant=utilisateur_id, contenu=payload.contenu)
		post = self.repo.creer_post(post)

		for image in payload.images:
			self.repo.ajouter_image(
				ReseauPostImage(
					post_identifiant=post.identifiant,
					url_image=image.url_image,
					position=image.position,
				)
			)

		for produit_id in payload.produit_identifiants:
			produit = self.db.query(Produit).filter(Produit.identifiant == produit_id).first()
			if not produit:
				raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Produit introuvable: {produit_id}")

			if not self._produit_achete_par_client(utilisateur_id, produit_id):
				raise HTTPException(
					status_code=status.HTTP_400_BAD_REQUEST,
					detail=f"Produit non acheté, impossible de publier l'avis social: {produit_id}",
				)

			self.repo.ajouter_tag(
				ReseauPostTagProduit(
					post_identifiant=post.identifiant,
					produit_identifiant=produit.identifiant,
					boutique_identifiant=produit.vendeur_identifiant,
				)
			)

		post = self.repo.get_post(post.identifiant)
		return self._to_post_read(post)

	def lister_feed(self, limite: int = 20, offset: int = 0):
		posts = self.repo.lister_posts_actifs(limite=limite, offset=offset)
		return [self._to_post_read(post) for post in posts]

	def lister_mes_posts(self, utilisateur_id, limite: int = 20, offset: int = 0):
		posts = self.repo.lister_posts_auteur(utilisateur_id, limite=limite, offset=offset)
		return [self._to_post_read(post) for post in posts]

	def obtenir_post(self, post_id):
		post = self.repo.get_post(post_id)
		if not post:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post introuvable")
		return self._to_post_read(post)

	def commenter(self, post_id, utilisateur_id, payload: CommentaireCreate):
		post = self.repo.get_post(post_id)
		if not post:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post introuvable")

		commentaire = ReseauCommentaire(
			post_identifiant=post_id,
			auteur_identifiant=utilisateur_id,
			contenu=payload.contenu,
		)
		commentaire = self.repo.ajouter_commentaire(commentaire)
		return {
			"identifiant": commentaire.identifiant,
			"post_identifiant": commentaire.post_identifiant,
			"auteur_identifiant": commentaire.auteur_identifiant,
			"contenu": commentaire.contenu,
			"statut_moderation": commentaire.statut_moderation,
			"date_creation": commentaire.date_creation,
			"nombre_likes": 0,
		}

	def lister_commentaires_post(self, post_id, tri: TriCommentaires = TriCommentaires.LIKES, inclure_non_actifs: bool = False, limite: int = 100, offset: int = 0):
		post = self.repo.get_post(post_id)
		if not post:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post introuvable")

		commentaires = self.repo.lister_commentaires_post(
			post_id,
			inclure_non_actifs=inclure_non_actifs,
			tri=tri.value,
			limite=limite,
			offset=offset,
		)

		return [
			{
				"identifiant": commentaire.identifiant,
				"post_identifiant": commentaire.post_identifiant,
				"auteur_identifiant": commentaire.auteur_identifiant,
				"contenu": commentaire.contenu,
				"statut_moderation": commentaire.statut_moderation,
				"date_creation": commentaire.date_creation,
				"nombre_likes": len(commentaire.likes),
			}
			for commentaire in commentaires
		]

	def toggle_like(self, post_id, utilisateur_id):
		post = self.repo.get_post(post_id)
		if not post:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post introuvable")

		existant = self.repo.get_like(post_id, utilisateur_id)
		if existant:
			self.repo.supprimer_like(existant)
			est_like = False
		else:
			self.repo.ajouter_like(ReseauLike(post_identifiant=post_id, utilisateur_identifiant=utilisateur_id))
			est_like = True

		return {"est_like": est_like, "nombre_likes": self.repo.compter_likes(post_id)}

	def partager(self, post_id, utilisateur_id, payload: PartageCreate):
		post = self.repo.get_post(post_id)
		if not post:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post introuvable")

		self.repo.ajouter_partage(
			ReseauPartage(
				post_identifiant=post_id,
				utilisateur_identifiant=utilisateur_id,
				plateforme=payload.plateforme,
			)
		)
		return {"nombre_partages": self.repo.compter_partages(post_id)}

	def toggle_like_commentaire(self, commentaire_id, utilisateur_id):
		commentaire = self.repo.get_commentaire(commentaire_id)
		if not commentaire:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commentaire introuvable")

		existant = self.repo.get_like_commentaire(commentaire_id, utilisateur_id)
		if existant:
			self.repo.supprimer_like_commentaire(existant)
			est_like = False
		else:
			self.repo.ajouter_like_commentaire(
				ReseauCommentaireLike(
					commentaire_identifiant=commentaire_id,
					utilisateur_identifiant=utilisateur_id,
				)
			)
			est_like = True

		return {
			"est_like": est_like,
			"nombre_likes_commentaire": self.repo.compter_likes_commentaire(commentaire_id),
		}

	# ========== ADMIN (tout droit) ==========
	def admin_lister_posts(self, limite: int = 50, offset: int = 0, statut: StatutModerationPost | None = None):
		posts = self.repo.lister_posts_tous(limite=limite, offset=offset, statut=statut)
		return [self._to_post_read(post) for post in posts]

	def admin_moderer_post(self, post_id, nouveau_statut: StatutModerationPost):
		post = self.repo.get_post(post_id)
		if not post:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post introuvable")
		post = self.repo.maj_post(post, {"statut_moderation": nouveau_statut})
		return self._to_post_read(post)

	def admin_supprimer_post(self, post_id):
		post = self.repo.get_post(post_id)
		if not post:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post introuvable")
		self.repo.supprimer_post(post)
		return {"message": "Post supprimé"}

	def admin_supprimer_commentaire(self, commentaire_id):
		commentaire = self.repo.get_commentaire(commentaire_id)
		if not commentaire:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commentaire introuvable")
		self.repo.supprimer_commentaire(commentaire)
		return {"message": "Commentaire supprimé"}

	def admin_lister_commentaires(self, limite: int = 100, offset: int = 0, statut: StatutModerationCommentaire | None = None):
		commentaires = self.repo.lister_commentaires_tous(limite=limite, offset=offset, statut=statut)
		return [
			{
				"identifiant": commentaire.identifiant,
				"post_identifiant": commentaire.post_identifiant,
				"auteur_identifiant": commentaire.auteur_identifiant,
				"contenu": commentaire.contenu,
				"statut_moderation": commentaire.statut_moderation,
				"date_creation": commentaire.date_creation,
				"nombre_likes": len(commentaire.likes),
			}
			for commentaire in commentaires
		]

	def admin_moderer_commentaire(self, commentaire_id, nouveau_statut: StatutModerationCommentaire):
		commentaire = self.repo.get_commentaire(commentaire_id)
		if not commentaire:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commentaire introuvable")
		commentaire = self.repo.maj_commentaire(commentaire, {"statut_moderation": nouveau_statut})
		return {
			"identifiant": commentaire.identifiant,
			"post_identifiant": commentaire.post_identifiant,
			"auteur_identifiant": commentaire.auteur_identifiant,
			"contenu": commentaire.contenu,
			"statut_moderation": commentaire.statut_moderation,
			"date_creation": commentaire.date_creation,
			"nombre_likes": len(commentaire.likes),
		}
