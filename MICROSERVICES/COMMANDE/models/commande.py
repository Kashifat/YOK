import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from shared.db.base import Base


class StatutCommande(str, enum.Enum):
	EN_ATTENTE_PAIEMENT = "EN_ATTENTE_PAIEMENT"
	PAYEE = "PAYEE"
	EN_PREPARATION = "EN_PREPARATION"
	EXPEDIEE = "EXPEDIEE"
	LIVREE = "LIVREE"
	ANNULEE = "ANNULEE"
	REMBOURSEE = "REMBOURSEE"


class Commande(Base):
	__tablename__ = "commandes"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	client_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant"), nullable=False)
	adresse_identifiant = Column(UUID(as_uuid=True), ForeignKey("adresses.identifiant"), nullable=False)
	statut = Column(Enum(StatutCommande, name="statut_commande", create_type=False), server_default=text("'EN_ATTENTE_PAIEMENT'"))
	total_cfa = Column(Integer, default=0)
	remarques = Column(Text)
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))

	articles = relationship("CommandeArticle", backref="commande", lazy="joined", cascade="all, delete-orphan")


class CommandeArticle(Base):
	__tablename__ = "commande_articles"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	commande_identifiant = Column(UUID(as_uuid=True), ForeignKey("commandes.identifiant"), nullable=False)
	produit_identifiant = Column(UUID(as_uuid=True), ForeignKey("produits.identifiant"), nullable=False)
	vendeur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant"), nullable=False)
	prix_unitaire_cfa = Column(Integer, nullable=False)
	quantite = Column(Integer, nullable=False)
	total_ligne_cfa = Column(Integer, nullable=False)
	statut = Column(Enum(StatutCommande, name="statut_commande", create_type=False), server_default=text("'EN_ATTENTE_PAIEMENT'"))
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))
