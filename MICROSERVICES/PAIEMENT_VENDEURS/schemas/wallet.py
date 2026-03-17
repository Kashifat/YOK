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


class VendeurCompteFinancierRead(BaseModel):
	mes_revenus_cfa: int
	montant_en_attente_cfa: int
	montant_confirme_cfa: int
	montant_verse_cfa: int
	historique_transactions: list["VendeurFinanceTransactionRead"]


class VendeurFinanceDashboardRead(BaseModel):
	total_ventes_cfa: int
	montant_en_attente_cfa: int
	montant_confirme_cfa: int
	montant_verse_cfa: int


class VendeurFinanceTransactionRead(BaseModel):
	commande_identifiant: UUID
	article_identifiant: UUID
	produit_identifiant: UUID
	produit_nom: str
	quantite: int
	montant_vendeur_cfa: int
	statut_financier: str
	date_commande: datetime
	date_confirmation: datetime | None = None
	date_versement: datetime | None = None


class VendeurFinanceTransactionsRead(BaseModel):
	transactions: list[VendeurFinanceTransactionRead]
	total: int


class VersementVendeurCreate(BaseModel):
	commande_identifiant: UUID
	vendeur_identifiant: UUID | None = None
	montant_cfa: int
	reference_versement: str | None = None


class VersementVendeurRead(BaseModel):
	message: str
	vendeur_identifiant: UUID
	commande_identifiant: UUID
	montant_cfa: int
