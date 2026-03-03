from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, text
from sqlalchemy.dialects.postgresql import UUID

from shared.db.base import Base


class ImageProduit(Base):
	__tablename__ = "images_produits"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	produit_identifiant = Column(UUID(as_uuid=True), ForeignKey("produits.identifiant"), nullable=False)
	url_image = Column(Text, nullable=False)
	couleur = Column(Text)
	position = Column(Integer, default=0)
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))


class VideoProduit(Base):
	__tablename__ = "videos_produits"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	produit_identifiant = Column(UUID(as_uuid=True), ForeignKey("produits.identifiant"), nullable=False)
	url_video = Column(Text, nullable=False)
	position = Column(Integer, default=0)
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))