from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Text, text
from sqlalchemy.dialects.postgresql import UUID

from shared.db.base import Base


class Categorie(Base):
	__tablename__ = "categories"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	nom = Column(Text, unique=True, nullable=False)
	parent_identifiant = Column(UUID(as_uuid=True), ForeignKey("categories.identifiant"), nullable=True)
	description = Column(Text)
	est_actif = Column(Boolean, default=True)
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))