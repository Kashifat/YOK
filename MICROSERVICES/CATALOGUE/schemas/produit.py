from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ProduitBase(BaseModel):
	categorie_identifiant: UUID
	nom: str = Field(min_length=2, max_length=150)
	description: str | None = None
	prix_cfa: int = Field(gt=0)
	stock: int = Field(default=0, ge=0)
	tailles: list[str] = Field(default_factory=list)
	couleurs: list[str] = Field(default_factory=list)
	slug: str | None = Field(default=None, max_length=200)
	mots_cles: list[str] = Field(default_factory=list)
	marque: str | None = Field(default=None, max_length=120)
	origine_pays: str = Field(default="CN", max_length=10)


class ProduitCreate(ProduitBase):
	pass


class ProduitUpdate(BaseModel):
	categorie_identifiant: UUID | None = None
	nom: str | None = Field(default=None, min_length=2, max_length=150)
	description: str | None = None
	prix_cfa: int | None = Field(default=None, gt=0)
	stock: int | None = Field(default=None, ge=0)
	tailles: list[str] | None = None
	couleurs: list[str] | None = None
	slug: str | None = Field(default=None, max_length=200)
	mots_cles: list[str] | None = None
	marque: str | None = Field(default=None, max_length=120)
	origine_pays: str | None = Field(default=None, max_length=10)
	est_actif: bool | None = None


class ProduitRead(ProduitBase):
	identifiant: UUID
	vendeur_identifiant: UUID
	est_actif: bool
	date_creation: datetime

	model_config = {"from_attributes": True}