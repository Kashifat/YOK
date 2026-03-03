import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from shared.db.base import Base


class StatutPaiementFacture(str, enum.Enum):
	EN_ATTENTE = "EN_ATTENTE"
	PAYEE = "PAYEE"
	ECHOUE = "ECHOUE"
	REMBOURSEE = "REMBOURSEE"


class Facture(Base):
	__tablename__ = "factures"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	numero_facture = Column(Text, unique=True, nullable=False)
	commande_identifiant = Column(UUID(as_uuid=True), ForeignKey("commandes.identifiant", ondelete="CASCADE"), unique=True, nullable=False)
	client_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant", ondelete="CASCADE"), nullable=False)
	montant_total_cfa = Column(Integer, nullable=False)
	statut_paiement = Column(Enum(StatutPaiementFacture, name="statut_facture_paiement", create_type=False), nullable=False, server_default=text("'EN_ATTENTE'"))
	mode_paiement = Column(Text)
	reference_paiement = Column(Text)
	date_emission = Column(DateTime(timezone=True), server_default=text("NOW()"))
	date_paiement = Column(DateTime(timezone=True))
	notes = Column(Text)

	suivis = relationship("FacturePaiementSuivi", backref="facture", lazy="joined", cascade="all, delete-orphan")


class FacturePaiementSuivi(Base):
	__tablename__ = "facture_paiement_suivis"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	facture_identifiant = Column(UUID(as_uuid=True), ForeignKey("factures.identifiant", ondelete="CASCADE"), nullable=False)
	ancien_statut = Column(Enum(StatutPaiementFacture, name="statut_facture_paiement", create_type=False))
	nouveau_statut = Column(Enum(StatutPaiementFacture, name="statut_facture_paiement", create_type=False), nullable=False)
	commentaire = Column(Text)
	acteur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant"))
	date_evenement = Column(DateTime(timezone=True), server_default=text("NOW()"))
