import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from shared.db.base import Base


class StatutLivraison(str, enum.Enum):
	CREEE = "CREEE"
	ASSIGNEE = "ASSIGNEE"
	EN_TRANSIT = "EN_TRANSIT"
	ARRIVEE_ENTREPOT_ABIDJAN = "ARRIVEE_ENTREPOT_ABIDJAN"
	LIVREE_CLIENT = "LIVREE_CLIENT"
	ANNULEE = "ANNULEE"


class Livraison(Base):
	__tablename__ = "livraisons"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	commande_identifiant = Column(UUID(as_uuid=True), ForeignKey("commandes.identifiant", ondelete="CASCADE"), nullable=False, unique=True)
	dossier_consolidation_identifiant = Column(UUID(as_uuid=True), ForeignKey("dossiers_consolidation.identifiant", ondelete="SET NULL"), nullable=True)
	statut = Column(Enum(StatutLivraison, name="statut_livraison", create_type=False), nullable=False, server_default=text("'CREEE'"))
	livreur_nom = Column(Text)
	livreur_telephone = Column(Text)
	preuve_livraison_url = Column(Text)
	commentaire = Column(Text)
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))
	date_mise_a_jour = Column(DateTime(timezone=True), server_default=text("NOW()"), onupdate=text("NOW()"))
	date_ramassage = Column(DateTime(timezone=True))
	date_verification_entrepot = Column(DateTime(timezone=True))
	date_livraison = Column(DateTime(timezone=True))

	evenements = relationship("LivraisonEvenement", backref="livraison", lazy="joined", cascade="all, delete-orphan")


class LivraisonEvenement(Base):
	__tablename__ = "livraison_evenements"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	livraison_identifiant = Column(UUID(as_uuid=True), ForeignKey("livraisons.identifiant", ondelete="CASCADE"), nullable=False)
	statut_avant = Column(Enum(StatutLivraison, name="statut_livraison", create_type=False))
	statut_apres = Column(Enum(StatutLivraison, name="statut_livraison", create_type=False), nullable=False)
	acteur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant", ondelete="SET NULL"))
	commentaire = Column(Text)
	date_evenement = Column(DateTime(timezone=True), server_default=text("NOW()"))
