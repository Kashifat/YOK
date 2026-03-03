from sqlalchemy import Column, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from shared.db.base import Base


class Favori(Base):
    __tablename__ = "favoris"

    identifiant = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    utilisateur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant", ondelete="CASCADE"), nullable=False, index=True)
    produit_identifiant = Column(UUID(as_uuid=True), ForeignKey("produits.identifiant", ondelete="CASCADE"), nullable=False, index=True)
    date_creation = Column(TIMESTAMP(timezone=True), server_default=func.now())
