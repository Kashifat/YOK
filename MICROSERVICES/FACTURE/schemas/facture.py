from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from ..models.facture import StatutPaiementFacture
from MICROSERVICES.COMMANDE.models.commande import StatutCommande


class FacturePaiementSuiviRead(BaseModel):
	identifiant: UUID
	facture_identifiant: UUID
	ancien_statut: StatutPaiementFacture | None
	nouveau_statut: StatutPaiementFacture
	commentaire: str | None
	acteur_identifiant: UUID | None
	date_evenement: datetime

	model_config = {"from_attributes": True}


class FactureRead(BaseModel):
	identifiant: UUID
	numero_facture: str
	commande_identifiant: UUID
	client_identifiant: UUID
	montant_total_cfa: int
	statut_paiement: StatutPaiementFacture
	mode_paiement: str | None
	reference_paiement: str | None
	date_emission: datetime
	date_paiement: datetime | None
	notes: str | None
	suivis: list[FacturePaiementSuiviRead] = []

	model_config = {"from_attributes": True}


class FacturePaiementUpdate(BaseModel):
	nouveau_statut: StatutPaiementFacture
	mode_paiement: str | None = Field(default=None, max_length=80)
	reference_paiement: str | None = Field(default=None, max_length=120)
	commentaire: str | None = None
	notes: str | None = None


class FactureDownloadMeta(BaseModel):
	facture_id: UUID
	nom_fichier: str
	media_type: str = "text/html"


class CommandeUtilisateurRead(BaseModel):
	identifiant: UUID
	client_identifiant: UUID
	adresse_identifiant: UUID
	statut: StatutCommande
	total_cfa: int
	date_creation: datetime

	model_config = {"from_attributes": True}


class HistoriqueUtilisateurAdminRead(BaseModel):
	utilisateur_identifiant: UUID
	nombre_commandes: int
	nombre_factures: int
	commandes: list[CommandeUtilisateurRead]
	factures: list[FactureRead]
