from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text, UniqueConstraint, text
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
	slug = Column(Text, unique=True)
	mots_cles = Column(ARRAY(Text))
	marque = Column(Text)
	origine_pays = Column(Text, server_default=text("'CN'"))
	est_actif = Column(Boolean, default=True)
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))


class VariantProduit(Base):
	__tablename__ = "variantes_produits"
	__table_args__ = (
		UniqueConstraint("produit_identifiant", "taille", "couleur", name="uq_variantes_produit_taille_couleur"),
	)

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	produit_identifiant = Column(UUID(as_uuid=True), ForeignKey("produits.identifiant", ondelete="CASCADE"), nullable=False)
	taille = Column(Text)
	couleur = Column(Text)
	stock = Column(Integer, nullable=False, default=0)
	prix_supplementaire_cfa = Column(Integer, nullable=False, default=0)
	sku = Column(Text, unique=True)
	est_actif = Column(Boolean, default=True)
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))