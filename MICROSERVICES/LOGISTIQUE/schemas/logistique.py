from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from ..models.logistique import StatutConsolidation, StatutReceptionFournisseur


class DossierConsolidationCreate(BaseModel):
	commande_identifiant: UUID


class AssignerAgentPayload(BaseModel):
	agent_identifiant: UUID
	commentaire: str | None = None


class ExpeditionVendeurPayload(BaseModel):
	vendeur_identifiant: UUID
	commande_article_identifiant: UUID | None = None
	tracking_fournisseur: str | None = None
	transporteur_fournisseur: str | None = None
	preuve_expedition_url: str | None = None
	commentaire: str | None = None


class ReceptionAgentPayload(BaseModel):
	preuve_reception_url: str | None = None
	commentaire: str | None = None


class ProblemeReceptionPayload(BaseModel):
	commentaire: str = Field(min_length=3)
	preuve_reception_url: str | None = None


class DemarrerConsolidationPayload(BaseModel):
	commentaire: str | None = None


class PreparerExpeditionPayload(BaseModel):
	poids_total_kg: Decimal | None = None
	longueur_cm: Decimal | None = None
	largeur_cm: Decimal | None = None
	hauteur_cm: Decimal | None = None
	preuve_emballage_url: str | None = None
	commentaire: str | None = None


class ExpeditionInternationalePayload(BaseModel):
	tracking_interne: str | None = None
	transporteur_international: str | None = None
	numero_vol_ou_cargo: str | None = None
	commentaire: str | None = None


class ArriveeAbidjanPayload(BaseModel):
	commentaire: str | None = None


class RemiseLivraisonLocalePayload(BaseModel):
	commentaire: str | None = None


class ConsolidationEvenementRead(BaseModel):
	identifiant: UUID
	dossier_consolidation_identifiant: UUID
	statut_avant: StatutConsolidation | None
	statut_apres: StatutConsolidation
	acteur_identifiant: UUID | None
	commentaire: str | None
	preuve_url: str | None
	date_evenement: datetime

	model_config = {"from_attributes": True}


class ReceptionFournisseurRead(BaseModel):
	identifiant: UUID
	dossier_consolidation_identifiant: UUID
	vendeur_identifiant: UUID
	commande_article_identifiant: UUID | None
	statut: StatutReceptionFournisseur
	tracking_fournisseur: str | None
	transporteur_fournisseur: str | None
	preuve_expedition_url: str | None
	preuve_reception_url: str | None
	commentaire: str | None
	date_expedition_vendeur: datetime | None
	date_reception_agent: datetime | None
	date_creation: datetime
	date_mise_a_jour: datetime

	model_config = {"from_attributes": True}


class DossierConsolidationRead(BaseModel):
	identifiant: UUID
	commande_identifiant: UUID
	agent_identifiant: UUID | None
	statut: StatutConsolidation
	poids_total_kg: Decimal | None
	longueur_cm: Decimal | None
	largeur_cm: Decimal | None
	hauteur_cm: Decimal | None
	nombre_colis_fournisseurs: int
	tous_colis_recus: bool
	tracking_interne: str | None
	transporteur_international: str | None
	numero_vol_ou_cargo: str | None
	preuve_emballage_url: str | None
	commentaire: str | None
	date_depart_chine: datetime | None
	date_arrivee_abidjan: datetime | None
	date_creation: datetime
	date_mise_a_jour: datetime
	receptions: list[ReceptionFournisseurRead] = []
	evenements: list[ConsolidationEvenementRead] = []

	model_config = {"from_attributes": True}


class DossierArisqueRead(BaseModel):
	"""Dossier de consolidation à risque (retards, problèmes, colis manquants)."""
	dossier: DossierConsolidationRead
	nombre_colis_attendu: int
	nombre_colis_recus: int
	nombre_problemes: int
	raisons_risque: list[str]

	model_config = {"from_attributes": True}


class ActionRead(BaseModel):
	message: str
