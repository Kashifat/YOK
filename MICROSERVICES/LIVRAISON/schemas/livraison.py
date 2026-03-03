from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from ..models.livraison import StatutLivraison


class LivraisonCreate(BaseModel):
	commande_identifiant: UUID
	livreur_nom: str | None = Field(default=None, max_length=120)
	livreur_telephone: str | None = Field(default=None, max_length=40)
	commentaire: str | None = None


class LivraisonUpdateRamassage(BaseModel):
	commentaire: str | None = None


class LivraisonUpdateTransit(BaseModel):
	commentaire: str | None = None


class LivraisonUpdateEntrepot(BaseModel):
	commentaire: str | None = None


class LivraisonUpdateLivree(BaseModel):
	preuve_livraison_url: str | None = None
	commentaire: str | None = None


class LivraisonEvenementRead(BaseModel):
	identifiant: UUID
	livraison_identifiant: UUID
	statut_avant: StatutLivraison | None
	statut_apres: StatutLivraison
	acteur_identifiant: UUID | None
	commentaire: str | None
	date_evenement: datetime

	model_config = {"from_attributes": True}


class LivraisonRead(BaseModel):
	identifiant: UUID
	commande_identifiant: UUID
	statut: StatutLivraison
	livreur_nom: str | None
	livreur_telephone: str | None
	preuve_livraison_url: str | None
	commentaire: str | None
	date_creation: datetime
	date_mise_a_jour: datetime
	date_ramassage: datetime | None
	date_verification_entrepot: datetime | None
	date_livraison: datetime | None
	evenements: list[LivraisonEvenementRead] = []

	model_config = {"from_attributes": True}


class ActionRead(BaseModel):
	message: str
