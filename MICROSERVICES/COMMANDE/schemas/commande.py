from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from ..models.commande import StatutCommande


# ========== COMMANDE ==========

class CommandeCreate(BaseModel):
	adresse_identifiant: UUID
	remarques: str | None = None


class CommandeUpdate(BaseModel):
	statut: StatutCommande | None = None
	remarques: str | None = None


class CommandeArticleRead(BaseModel):
	identifiant: UUID
	commande_identifiant: UUID
	produit_identifiant: UUID
	vendeur_identifiant: UUID
	prix_unitaire_cfa: int
	quantite: int
	total_ligne_cfa: int
	statut: StatutCommande
	date_creation: datetime

	model_config = {"from_attributes": True}


class CommandeRead(BaseModel):
	identifiant: UUID
	client_identifiant: UUID
	adresse_identifiant: UUID
	statut: StatutCommande
	total_cfa: int
	remarques: str | None
	date_creation: datetime
	articles: list[CommandeArticleRead] = []

	model_config = {"from_attributes": True}


class CommandeCreationRead(CommandeRead):
	paiement_identifiant: UUID | None = None
	payment_url: str | None = None
	provider_transaction_id: str | None = None
	payment_mode: str | None = None
	payment_message: str | None = None


class CommandeArticleUpdateStatut(BaseModel):
	statut: StatutCommande
