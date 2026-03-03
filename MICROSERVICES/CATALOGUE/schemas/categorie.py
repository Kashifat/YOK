from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CategorieBase(BaseModel):
	nom: str = Field(min_length=2, max_length=120)
	parent_identifiant: UUID | None = None
	description: str | None = None


class CategorieCreate(CategorieBase):
	pass


class CategorieUpdate(BaseModel):
	nom: str | None = Field(default=None, min_length=2, max_length=120)
	parent_identifiant: UUID | None = None
	description: str | None = None
	est_actif: bool | None = None


class CategorieRead(CategorieBase):
	identifiant: UUID
	est_actif: bool
	date_creation: datetime

	model_config = {"from_attributes": True}