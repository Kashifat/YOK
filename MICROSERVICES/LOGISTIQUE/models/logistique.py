import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, Numeric, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from shared.db.base import Base


class StatutConsolidation(str, enum.Enum):
	EN_ATTENTE_RECEPTION = "EN_ATTENTE_RECEPTION"
	RECEPTION_PARTIELLE = "RECEPTION_PARTIELLE"
	TOUS_COLIS_RECUS = "TOUS_COLIS_RECUS"
	EN_CONSOLIDATION = "EN_CONSOLIDATION"
	PRET_EXPEDITION = "PRET_EXPEDITION"
	EXPEDIE = "EXPEDIE"
	ARRIVE_ABIDJAN = "ARRIVE_ABIDJAN"
	REMIS_LIVRAISON_LOCALE = "REMIS_LIVRAISON_LOCALE"
	ANNULE = "ANNULE"


class StatutReceptionFournisseur(str, enum.Enum):
	EN_ATTENTE_EXPEDITION_VENDEUR = "EN_ATTENTE_EXPEDITION_VENDEUR"
	EXPEDIE_PAR_VENDEUR = "EXPEDIE_PAR_VENDEUR"
	RECU_PAR_AGENT = "RECU_PAR_AGENT"
	PROBLEME_RECEPTION = "PROBLEME_RECEPTION"
	ANNULE = "ANNULE"


class DossierConsolidation(Base):
	__tablename__ = "dossiers_consolidation"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	commande_identifiant = Column(UUID(as_uuid=True), ForeignKey("commandes.identifiant", ondelete="CASCADE"), nullable=False, unique=True)
	agent_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant", ondelete="SET NULL"), nullable=True)
	statut = Column(Enum(StatutConsolidation, name="statut_consolidation", create_type=False), nullable=False, server_default=text("'EN_ATTENTE_RECEPTION'"))
	poids_total_kg = Column(Numeric(10, 2))
	longueur_cm = Column(Numeric(10, 2))
	largeur_cm = Column(Numeric(10, 2))
	hauteur_cm = Column(Numeric(10, 2))
	nombre_colis_fournisseurs = Column(Integer, nullable=False, default=0)
	tous_colis_recus = Column(Boolean, nullable=False, default=False)
	tracking_interne = Column(Text)
	transporteur_international = Column(Text)
	numero_vol_ou_cargo = Column(Text)
	preuve_emballage_url = Column(Text)
	commentaire = Column(Text)
	date_depart_chine = Column(DateTime(timezone=True))
	date_arrivee_abidjan = Column(DateTime(timezone=True))
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))
	date_mise_a_jour = Column(DateTime(timezone=True), server_default=text("NOW()"), onupdate=text("NOW()"))

	receptions = relationship("ReceptionFournisseur", backref="dossier", lazy="joined", cascade="all, delete-orphan")
	evenements = relationship("ConsolidationEvenement", backref="dossier", lazy="joined", cascade="all, delete-orphan")


class ReceptionFournisseur(Base):
	__tablename__ = "receptions_fournisseurs"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	dossier_consolidation_identifiant = Column(UUID(as_uuid=True), ForeignKey("dossiers_consolidation.identifiant", ondelete="CASCADE"), nullable=False)
	vendeur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant", ondelete="CASCADE"), nullable=False)
	commande_article_identifiant = Column(UUID(as_uuid=True), ForeignKey("commande_articles.identifiant", ondelete="SET NULL"), nullable=True)
	statut = Column(Enum(StatutReceptionFournisseur, name="statut_reception_fournisseur", create_type=False), nullable=False, server_default=text("'EN_ATTENTE_EXPEDITION_VENDEUR'"))
	tracking_fournisseur = Column(Text)
	transporteur_fournisseur = Column(Text)
	preuve_expedition_url = Column(Text)
	preuve_reception_url = Column(Text)
	commentaire = Column(Text)
	date_expedition_vendeur = Column(DateTime(timezone=True))
	date_reception_agent = Column(DateTime(timezone=True))
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))
	date_mise_a_jour = Column(DateTime(timezone=True), server_default=text("NOW()"), onupdate=text("NOW()"))


class ConsolidationEvenement(Base):
	__tablename__ = "consolidation_evenements"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	dossier_consolidation_identifiant = Column(UUID(as_uuid=True), ForeignKey("dossiers_consolidation.identifiant", ondelete="CASCADE"), nullable=False)
	statut_avant = Column(Enum(StatutConsolidation, name="statut_consolidation", create_type=False))
	statut_apres = Column(Enum(StatutConsolidation, name="statut_consolidation", create_type=False), nullable=False)
	acteur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant", ondelete="SET NULL"), nullable=True)
	commentaire = Column(Text)
	preuve_url = Column(Text)
	date_evenement = Column(DateTime(timezone=True), server_default=text("NOW()"))
