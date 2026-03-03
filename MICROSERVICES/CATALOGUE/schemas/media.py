from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ImageCreate(BaseModel):
	url_image: str = Field(min_length=4)
	couleur: str | None = None
	position: int = Field(default=0, ge=0)


class ImageRead(ImageCreate):
	identifiant: UUID
	produit_identifiant: UUID
	date_creation: datetime

	model_config = {"from_attributes": True}


class VideoCreate(BaseModel):
	url_video: str = Field(min_length=4)
	position: int = Field(default=0, ge=0)


class VideoRead(VideoCreate):
	identifiant: UUID
	produit_identifiant: UUID
	date_creation: datetime

	model_config = {"from_attributes": True}