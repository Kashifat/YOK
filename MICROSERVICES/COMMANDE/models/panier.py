from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from shared.db.base import Base


class Panier(Base):
	__tablename__ = "paniers"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	utilisateur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant"), unique=True, nullable=False)
	date_mise_a_jour = Column(DateTime(timezone=True), server_default=text("NOW()"))

	articles = relationship("PanierArticle", backref="panier", lazy="joined", cascade="all, delete-orphan")


class PanierArticle(Base):
	__tablename__ = "panier_articles"
	__table_args__ = (
		UniqueConstraint(
			"panier_identifiant",
			"produit_identifiant",
			"variante_identifiant",
			name="uq_panier_article_variante",
		),
	)

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	panier_identifiant = Column(UUID(as_uuid=True), ForeignKey("paniers.identifiant"), nullable=False)
	produit_identifiant = Column(UUID(as_uuid=True), ForeignKey("produits.identifiant"), nullable=False)
	variante_identifiant = Column(UUID(as_uuid=True), ForeignKey("variantes_produits.identifiant"), nullable=True)
	quantite = Column(Integer, nullable=False)
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))
