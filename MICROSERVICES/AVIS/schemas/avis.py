from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AvisBase(BaseModel):
	note: int = Field(ge=1, le=5)
	titre: str | None = Field(default=None, max_length=150)
	commentaire: str | None = None


class AvisCreate(AvisBase):
	produit_identifiant: UUID


class AvisUpdate(BaseModel):
	note: int | None = Field(default=None, ge=1, le=5)
	titre: str | None = Field(default=None, max_length=150)
	commentaire: str | None = None


class AvisRead(AvisBase):
	identifiant: UUID
	produit_identifiant: UUID
	client_identifiant: UUID
	date_creation: datetime
	images: list["ImageAvisRead"] = []

	model_config = {"from_attributes": True}


class ImageAvisCreate(BaseModel):
	url_image: str = Field(min_length=4)
	position: int = Field(default=0, ge=0)


class ImageAvisRead(ImageAvisCreate):
	identifiant: UUID
	avis_identifiant: UUID
	date_creation: datetime

	model_config = {"from_attributes": True}
