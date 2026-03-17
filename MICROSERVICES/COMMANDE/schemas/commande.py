from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from ..models.commande import StatutCommande


# ========== COMMANDE ==========

class CommandeCreate(BaseModel):
	adresse_identifiant: UUID
	code_promo_identifiant: UUID | None = None
	frais_livraison_cfa: int = Field(default=0, ge=0)
	montant_remise_cfa: int = Field(default=0, ge=0)
	remarques: str | None = None


class CommandeUpdate(BaseModel):
	statut: StatutCommande | None = None
	code_promo_identifiant: UUID | None = None
	frais_livraison_cfa: int | None = Field(default=None, ge=0)
	montant_remise_cfa: int | None = Field(default=None, ge=0)
	remarques: str | None = None


class CommandeArticleRead(BaseModel):
	identifiant: UUID
	commande_identifiant: UUID
	produit_identifiant: UUID
	vendeur_identifiant: UUID
	variante_identifiant: UUID | None = None
	prix_unitaire_cfa: int
	quantite: int
	taille_selectionnee: str | None = None
	couleur_selectionnee: str | None = None
	total_ligne_cfa: int
	statut: StatutCommande
	date_creation: datetime

	model_config = {"from_attributes": True}


class CommandeRead(BaseModel):
	identifiant: UUID
	client_identifiant: UUID
	adresse_identifiant: UUID
	code_promo_identifiant: UUID | None = None
	statut: StatutCommande
	total_cfa: int
	frais_livraison_cfa: int
	montant_remise_cfa: int
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


class CommandeStatutUXRead(BaseModel):
	commande_identifiant: UUID
	statut_ux: str
	statut_commande: StatutCommande
	statut_consolidation: str | None = None
	statut_livraison: str | None = None
	message: str


class ExpeditionAFaireRead(BaseModel):
	"""Vue opérationnelle: article à expédier pour vendeur."""
	article_identifiant: UUID
	commande_identifiant: UUID
	dossier_consolidation_identifiant: UUID
	produit_nom: str
	taille_selectionnee: str | None = None
	couleur_selectionnee: str | None = None
	quantite: int
	prix_unitaire_cfa: int
	total_ligne_cfa: int
	statut_reception: str  # EN_ATTENTE_EXPEDITION_VENDEUR, EXPEDIE_PAR_VENDEUR, etc.
	date_commande: datetime
	est_expedie: bool  # True si EXPEDIE_PAR_VENDEUR
	tracking: str | None = None  # Si déjà expédié

	model_config = {"from_attributes": True}
