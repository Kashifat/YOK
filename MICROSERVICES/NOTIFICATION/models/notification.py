"""
Modèle SQLAlchemy pour les notifications.
"""
import enum

from sqlalchemy import Boolean, Column, DateTime, Enum as SQLEnum, ForeignKey, Text, text
from sqlalchemy.dialects.postgresql import UUID

from shared.db.base import Base


class TypeNotification(str, enum.Enum):
    """Types de notifications conformes à yok_db.sql."""

    COMMANDE_PAYEE = "COMMANDE_PAYEE"
    COMMANDE_EXPEDIEE = "COMMANDE_EXPEDIEE"
    COMMANDE_LIVREE = "COMMANDE_LIVREE"
    COLIS_ARRIVE_ABIDJAN = "COLIS_ARRIVE_ABIDJAN"
    PAIEMENT_VENDEUR_RECU = "PAIEMENT_VENDEUR_RECU"
    AVIS_RECU = "AVIS_RECU"
    PROMO_DISPONIBLE = "PROMO_DISPONIBLE"
    POST_LIKE = "POST_LIKE"
    NOUVEAU_COMMENTAIRE = "NOUVEAU_COMMENTAIRE"


class Notification(Base):
    """Table notifications alignée sur la base PostgreSQL réelle."""

    __tablename__ = "notifications"

    identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    utilisateur_identifiant = Column(
        UUID(as_uuid=True),
        ForeignKey("utilisateurs.identifiant", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    type = Column(
        SQLEnum(TypeNotification, name="type_notification", create_type=False),
        nullable=False,
        index=True,
    )
    titre = Column(Text, nullable=False)
    message = Column(Text)
    lien = Column(Text)
    est_lue = Column(Boolean, server_default=text("FALSE"), index=True)
    date_lecture = Column(DateTime(timezone=True))
    date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))

    def __repr__(self):
        return f"<Notification {self.identifiant} - {self.type}>"
