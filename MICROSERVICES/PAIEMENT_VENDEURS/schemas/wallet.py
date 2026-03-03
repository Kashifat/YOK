from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from MICROSERVICES.COMMANDE.models.commande import StatutCommande

from ..models.wallet import StatutReservationWallet, TypeTransactionWallet


class WalletRead(BaseModel):
	vendeur_identifiant: UUID
	solde_disponible_cfa: int
	solde_en_attente_cfa: int
	date_creation: datetime
	date_mise_a_jour: datetime

	model_config = {"from_attributes": True}


class WalletReservationRead(BaseModel):
	identifiant: UUID
	vendeur_identifiant: UUID
	commande_identifiant: UUID
	montant_total_net_cfa: int
	montant_en_attente_restant_cfa: int
	montant_avance_debloque_cfa: int
	montant_solde_debloque_cfa: int
	statut: StatutReservationWallet
	date_creation: datetime
	date_mise_a_jour: datetime

	model_config = {"from_attributes": True}


class TransactionWalletRead(BaseModel):
	identifiant: UUID
	vendeur_identifiant: UUID
	commande_identifiant: UUID | None
	type: TypeTransactionWallet
	montant_cfa: int
	commentaire: str | None
	date_creation: datetime

	model_config = {"from_attributes": True}


class EvenementCommandeCreate(BaseModel):
	commande_identifiant: UUID
	nouveau_statut: StatutCommande
	source: str | None = None


class ActionRead(BaseModel):
	message: str


class WalletDetailsRead(BaseModel):
	wallet: WalletRead
	reservations: list[WalletReservationRead]
	transactions: list[TransactionWalletRead]
