from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text, text
from sqlalchemy.dialects.postgresql import ARRAY, UUID

from shared.db.base import Base


class Produit(Base):
	__tablename__ = "produits"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	vendeur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant"), nullable=False)
	categorie_identifiant = Column(UUID(as_uuid=True), ForeignKey("categories.identifiant"), nullable=False)
	nom = Column(Text, nullable=False)
	description = Column(Text)
	prix_cfa = Column(Integer, nullable=False)
	stock = Column(Integer, default=0)
	tailles = Column(ARRAY(Text), server_default=text("'{}'"))
	couleurs = Column(ARRAY(Text), server_default=text("'{}'"))
	est_actif = Column(Boolean, default=True)
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))