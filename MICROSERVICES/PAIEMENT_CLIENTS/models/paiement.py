import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, JSON, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from shared.db.base import Base


class StatutPaiementTransaction(str, enum.Enum):
	EN_ATTENTE = "EN_ATTENTE"
	EN_COURS = "EN_COURS"
	PAYEE = "PAYEE"
	ECHOUE = "ECHOUE"
	ANNULEE = "ANNULEE"


class FournisseurPaiement(str, enum.Enum):
	CINETPAY = "CINETPAY"


class Paiement(Base):
	__tablename__ = "paiements"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	commande_identifiant = Column(UUID(as_uuid=True), ForeignKey("commandes.identifiant", ondelete="CASCADE"), nullable=False, unique=True)
	utilisateur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant", ondelete="CASCADE"), nullable=False)
	montant_cfa = Column(Integer, nullable=False)
	devise = Column(Text, nullable=False, server_default=text("'XOF'"))
	fournisseur = Column(Enum(FournisseurPaiement, name="fournisseur_paiement", create_type=False), nullable=False, server_default=text("'CINETPAY'"))
	statut = Column(Enum(StatutPaiementTransaction, name="statut_paiement_transaction", create_type=False), nullable=False, server_default=text("'EN_ATTENTE'"))
	provider_transaction_id = Column(Text, unique=True)
	provider_payment_url = Column(Text)
	methode = Column(Text)
	description = Column(Text)
	payload_initialisation = Column(JSON)
	payload_webhook = Column(JSON)
	date_confirmation = Column(DateTime(timezone=True))
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))
	date_mise_a_jour = Column(DateTime(timezone=True), server_default=text("NOW()"), onupdate=text("NOW()"))

	evenements = relationship("PaiementEvenement", backref="paiement", lazy="joined", cascade="all, delete-orphan")


class PaiementEvenement(Base):
	__tablename__ = "paiement_evenements"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	paiement_identifiant = Column(UUID(as_uuid=True), ForeignKey("paiements.identifiant", ondelete="CASCADE"), nullable=False)
	type_evenement = Column(Text, nullable=False)
	source = Column(Text, nullable=False)
	ancien_statut = Column(Enum(StatutPaiementTransaction, name="statut_paiement_transaction", create_type=False))
	nouveau_statut = Column(Enum(StatutPaiementTransaction, name="statut_paiement_transaction", create_type=False), nullable=False)
	payload = Column(JSON)
	commentaire = Column(Text)
	date_evenement = Column(DateTime(timezone=True), server_default=text("NOW()"))
