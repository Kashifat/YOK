from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, text
from sqlalchemy.dialects.postgresql import UUID

from shared.db.base import Base


class ImageAvis(Base):
	__tablename__ = "images_avis"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	avis_identifiant = Column(UUID(as_uuid=True), ForeignKey("avis.identifiant"), nullable=False)
	url_image = Column(Text, nullable=False)
	position = Column(Integer, default=0)
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))
