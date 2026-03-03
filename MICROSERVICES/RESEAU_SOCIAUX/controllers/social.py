from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from ..models.social import StatutModerationCommentaire, StatutModerationPost
from ..schemas.social import ActionRead, CommentaireCreate, CommentaireLikeToggleRead, CommentaireModerationUpdate, CommentaireRead, LikeToggleRead, PartageCreate, PartageRead, PostCreate, PostModerationUpdate, PostRead, TriCommentaires
from ..services.autorisation_service import AutorisationService
from ..services.social_service import SocialService


router = APIRouter()
auth_user = AutorisationService([RoleUtilisateur.CLIENT, RoleUtilisateur.VENDEUR, RoleUtilisateur.ADMINISTRATEUR])
auth_admin = AutorisationService([RoleUtilisateur.ADMINISTRATEUR])


@router.post("/posts", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def creer_post(payload: PostCreate, utilisateur=Depends(auth_user), db: Session = Depends(obtenir_session)):
	"""Publier un post social après achat vérifié des produits taggés."""
	service = SocialService(db)
	return service.creer_post(utilisateur.get("sub"), payload)


@router.get("/posts", response_model=list[PostRead])
def lister_feed(limite: int = 20, offset: int = 0, db: Session = Depends(obtenir_session)):
	"""Feed public des posts sociaux."""
	service = SocialService(db)
	return service.lister_feed(limite=limite, offset=offset)


@router.get("/posts/moi", response_model=list[PostRead])
def lister_mes_posts(limite: int = 20, offset: int = 0, utilisateur=Depends(auth_user), db: Session = Depends(obtenir_session)):
	"""Mes posts sociaux."""
	service = SocialService(db)
	return service.lister_mes_posts(utilisateur.get("sub"), limite=limite, offset=offset)


@router.get("/posts/{post_id}", response_model=PostRead)
def obtenir_post(post_id: UUID, db: Session = Depends(obtenir_session)):
	"""Détail d'un post social."""
	service = SocialService(db)
	return service.obtenir_post(post_id)


@router.post("/posts/{post_id}/commentaires", response_model=CommentaireRead, status_code=status.HTTP_201_CREATED)
def commenter_post(post_id: UUID, payload: CommentaireCreate, utilisateur=Depends(auth_user), db: Session = Depends(obtenir_session)):
	"""Commenter un post social."""
	service = SocialService(db)
	return service.commenter(post_id, utilisateur.get("sub"), payload)


@router.get("/posts/{post_id}/commentaires", response_model=list[CommentaireRead])
def lister_commentaires_post(post_id: UUID, tri: TriCommentaires = TriCommentaires.LIKES, limite: int = 100, offset: int = 0, db: Session = Depends(obtenir_session)):
	"""Liste des commentaires d'un post triés par likes (ou récents)."""
	service = SocialService(db)
	return service.lister_commentaires_post(post_id, tri=tri, inclure_non_actifs=False, limite=limite, offset=offset)


@router.post("/commentaires/{commentaire_id}/likes", response_model=CommentaireLikeToggleRead)
def liker_commentaire(commentaire_id: UUID, utilisateur=Depends(auth_user), db: Session = Depends(obtenir_session)):
	"""Like/Unlike d'un commentaire."""
	service = SocialService(db)
	return service.toggle_like_commentaire(commentaire_id, utilisateur.get("sub"))


@router.post("/posts/{post_id}/likes", response_model=LikeToggleRead)
def liker_post(post_id: UUID, utilisateur=Depends(auth_user), db: Session = Depends(obtenir_session)):
	"""Like/Unlike d'un post social."""
	service = SocialService(db)
	return service.toggle_like(post_id, utilisateur.get("sub"))


@router.post("/posts/{post_id}/partages", response_model=PartageRead)
def partager_post(post_id: UUID, payload: PartageCreate, utilisateur=Depends(auth_user), db: Session = Depends(obtenir_session)):
	"""Partager un post social (comptage)."""
	service = SocialService(db)
	return service.partager(post_id, utilisateur.get("sub"), payload)


@router.get("/admin/posts", response_model=list[PostRead])
def admin_lister_posts(
	limite: int = 50,
	offset: int = 0,
	statut: StatutModerationPost | None = None,
	utilisateur=Depends(auth_admin),
	db: Session = Depends(obtenir_session),
):
	"""Admin: voir tous les posts, y compris masqués/supprimés."""
	service = SocialService(db)
	return service.admin_lister_posts(limite=limite, offset=offset, statut=statut)


@router.patch("/admin/posts/{post_id}", response_model=PostRead)
def admin_moderer_post(
	post_id: UUID,
	payload: PostModerationUpdate,
	utilisateur=Depends(auth_admin),
	db: Session = Depends(obtenir_session),
):
	"""Admin: modérer un post (ACTIF/MASQUE/SUPPRIME)."""
	service = SocialService(db)
	return service.admin_moderer_post(post_id, payload.statut)


@router.delete("/admin/posts/{post_id}", response_model=ActionRead)
def admin_supprimer_post(post_id: UUID, utilisateur=Depends(auth_admin), db: Session = Depends(obtenir_session)):
	"""Admin: supprimer définitivement un post."""
	service = SocialService(db)
	return service.admin_supprimer_post(post_id)


@router.delete("/admin/commentaires/{commentaire_id}", response_model=ActionRead)
def admin_supprimer_commentaire(commentaire_id: UUID, utilisateur=Depends(auth_admin), db: Session = Depends(obtenir_session)):
	"""Admin: supprimer n'importe quel commentaire."""
	service = SocialService(db)
	return service.admin_supprimer_commentaire(commentaire_id)


@router.get("/admin/commentaires", response_model=list[CommentaireRead])
def admin_lister_commentaires(
	limite: int = 100,
	offset: int = 0,
	statut: StatutModerationCommentaire | None = None,
	utilisateur=Depends(auth_admin),
	db: Session = Depends(obtenir_session),
):
	"""Admin: voir tous les commentaires, y compris masqués/supprimés."""
	service = SocialService(db)
	return service.admin_lister_commentaires(limite=limite, offset=offset, statut=statut)


@router.patch("/admin/commentaires/{commentaire_id}", response_model=CommentaireRead)
def admin_moderer_commentaire(
	commentaire_id: UUID,
	payload: CommentaireModerationUpdate,
	utilisateur=Depends(auth_admin),
	db: Session = Depends(obtenir_session),
):
	"""Admin: modérer un commentaire (ACTIF/MASQUE/SUPPRIME)."""
	service = SocialService(db)
	return service.admin_moderer_commentaire(commentaire_id, payload.statut)
