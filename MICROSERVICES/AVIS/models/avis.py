from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from shared.db.base import Base


class Avis(Base):
	__tablename__ = "avis"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	produit_identifiant = Column(UUID(as_uuid=True), ForeignKey("produits.identifiant"), nullable=False)
	client_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant"), nullable=False)
	note = Column(Integer, nullable=False)
	titre = Column(Text)
	commentaire = Column(Text)
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))

	images = relationship("ImageAvis", backref="avis", lazy="joined")

	__table_args__ = (
		CheckConstraint('note >= 1 AND note <= 5', name='check_note_range'),
		UniqueConstraint('produit_identifiant', 'client_identifiant', name='uq_avis_produit_client'),
	)
