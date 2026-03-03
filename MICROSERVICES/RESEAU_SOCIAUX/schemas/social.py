from datetime import datetime
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, Field
from ..models.social import StatutModerationCommentaire, StatutModerationPost


class PostImageCreate(BaseModel):
	url_image: str = Field(min_length=4)
	position: int = Field(default=0, ge=0)


class PostCreate(BaseModel):
	contenu: str = Field(min_length=2, max_length=3000)
	produit_identifiants: list[UUID] = Field(min_length=1)
	images: list[PostImageCreate] = Field(min_length=1)


class CommentaireCreate(BaseModel):
	contenu: str = Field(min_length=1, max_length=1200)


class PartageCreate(BaseModel):
	plateforme: str | None = Field(default=None, max_length=50)


class PostImageRead(PostImageCreate):
	identifiant: UUID
	post_identifiant: UUID
	date_creation: datetime

	model_config = {"from_attributes": True}


class PostTagProduitRead(BaseModel):
	identifiant: UUID
	post_identifiant: UUID
	produit_identifiant: UUID
	boutique_identifiant: UUID

	model_config = {"from_attributes": True}


class CommentaireRead(BaseModel):
	identifiant: UUID
	post_identifiant: UUID
	auteur_identifiant: UUID
	contenu: str
	statut_moderation: StatutModerationCommentaire
	date_creation: datetime
	nombre_likes: int = 0

	model_config = {"from_attributes": True}


class PostRead(BaseModel):
	identifiant: UUID
	auteur_identifiant: UUID
	contenu: str
	date_creation: datetime
	images: list[PostImageRead]
	tags: list[PostTagProduitRead]
	nombre_commentaires: int
	nombre_likes: int
	nombre_partages: int


class LikeToggleRead(BaseModel):
	est_like: bool
	nombre_likes: int


class CommentaireLikeToggleRead(BaseModel):
	est_like: bool
	nombre_likes_commentaire: int


class PartageRead(BaseModel):
	nombre_partages: int


class PostModerationUpdate(BaseModel):
	statut: StatutModerationPost


class CommentaireModerationUpdate(BaseModel):
	statut: StatutModerationCommentaire


class TriCommentaires(str, Enum):
	LIKES = "likes"
	RECENT = "recent"


class ActionRead(BaseModel):
	message: str
