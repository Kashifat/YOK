import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Text, text
from sqlalchemy.dialects.postgresql import UUID

from shared.db.base import Base


class TypeTransactionWallet(str, enum.Enum):
	CREDIT_ATTENTE = "CREDIT_ATTENTE"
	DEBIT_ATTENTE = "DEBIT_ATTENTE"
	CREDIT_DISPONIBLE = "CREDIT_DISPONIBLE"
	PAIEMENT_EFFECTUE = "PAIEMENT_EFFECTUE"


class StatutReservationWallet(str, enum.Enum):
	EN_ATTENTE = "EN_ATTENTE"
	PARTIELLEMENT_LIBEREE = "PARTIELLEMENT_LIBEREE"
	LIBEREE = "LIBEREE"
	ANNULEE = "ANNULEE"


class WalletVendeur(Base):
	__tablename__ = "wallet_vendeurs"

	vendeur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant", ondelete="CASCADE"), primary_key=True)
	solde_disponible_cfa = Column(Integer, nullable=False, server_default=text("0"))
	solde_en_attente_cfa = Column(Integer, nullable=False, server_default=text("0"))
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))
	date_mise_a_jour = Column(DateTime(timezone=True), server_default=text("NOW()"), onupdate=text("NOW()"))


class WalletReservationCommande(Base):
	__tablename__ = "wallet_reservations_commandes"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	vendeur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant", ondelete="CASCADE"), nullable=False)
	commande_identifiant = Column(UUID(as_uuid=True), ForeignKey("commandes.identifiant", ondelete="CASCADE"), nullable=False)
	montant_total_net_cfa = Column(Integer, nullable=False)
	montant_en_attente_restant_cfa = Column(Integer, nullable=False)
	montant_avance_debloque_cfa = Column(Integer, nullable=False, server_default=text("0"))
	montant_solde_debloque_cfa = Column(Integer, nullable=False, server_default=text("0"))
	statut = Column(Enum(StatutReservationWallet, name="statut_reservation_wallet", create_type=False), nullable=False, server_default=text("'EN_ATTENTE'"))
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))
	date_mise_a_jour = Column(DateTime(timezone=True), server_default=text("NOW()"), onupdate=text("NOW()"))


class TransactionWallet(Base):
	__tablename__ = "transactions_wallet"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	vendeur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant", ondelete="CASCADE"), nullable=False)
	commande_identifiant = Column(UUID(as_uuid=True), ForeignKey("commandes.identifiant", ondelete="SET NULL"))
	type = Column(Enum(TypeTransactionWallet, name="type_transaction_wallet", create_type=False), nullable=False)
	montant_cfa = Column(Integer, nullable=False)
	commentaire = Column(Text)
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))
