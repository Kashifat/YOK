from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from ..models.commande import StatutCommande


# ========== PANIER ==========

class PanierArticleBase(BaseModel):
	produit_identifiant: UUID
	quantite: int = Field(gt=0)


class PanierArticleCreate(PanierArticleBase):
	pass


class PanierArticleUpdate(BaseModel):
	quantite: int = Field(gt=0)


class PanierArticleRead(PanierArticleBase):
	identifiant: UUID
	panier_identifiant: UUID
	date_creation: datetime

	model_config = {"from_attributes": True}


class PanierRead(BaseModel):
	identifiant: UUID
	utilisateur_identifiant: UUID
	date_mise_a_jour: datetime
	articles: list[PanierArticleRead] = []

	model_config = {"from_attributes": True}
