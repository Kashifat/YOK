from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from ..models.paiement import FournisseurPaiement, StatutPaiementTransaction


class PaiementInitialisationCreate(BaseModel):
	commande_identifiant: UUID
	telephone: str | None = Field(default=None, max_length=40)
	canal: str | None = Field(default="ALL", max_length=30)
	description: str | None = Field(default=None, max_length=255)


class PaiementWebhookPayload(BaseModel):
	payload: dict


class PaiementEvenementRead(BaseModel):
	identifiant: UUID
	paiement_identifiant: UUID
	type_evenement: str
	source: str
	ancien_statut: StatutPaiementTransaction | None
	nouveau_statut: StatutPaiementTransaction
	payload: dict | None
	commentaire: str | None
	date_evenement: datetime

	model_config = {"from_attributes": True}


class PaiementRead(BaseModel):
	identifiant: UUID
	commande_identifiant: UUID
	utilisateur_identifiant: UUID
	montant_cfa: int
	devise: str
	fournisseur: FournisseurPaiement
	statut: StatutPaiementTransaction
	provider_transaction_id: str | None
	provider_payment_url: str | None
	methode: str | None
	description: str | None
	date_confirmation: datetime | None
	date_creation: datetime
	date_mise_a_jour: datetime
	evenements: list[PaiementEvenementRead] = []

	model_config = {"from_attributes": True}


class PaiementInitialisationRead(BaseModel):
	paiement: PaiementRead
	payment_url: str
	provider_transaction_id: str
	mode: str


class PaiementVerificationRead(BaseModel):
	paiement: PaiementRead
	source: str
	message: str


class ActionRead(BaseModel):
	message: str
