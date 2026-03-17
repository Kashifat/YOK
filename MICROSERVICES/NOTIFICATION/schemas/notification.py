"""
Pydantic schemas pour les notifications.
"""
from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr

from ..models.notification import TypeNotification


class TypeNotificationEvenement(str, Enum):
    """Types d'événements acceptés par les endpoints legacy du microservice."""

    COMMANDE_CONFIRMEE = "commande_confirmee"
    PREPARATION_COMMENCEE = "preparation_commencee"
    EN_LIVRAISON = "en_livraison"
    LIVREE = "livree"
    ANNULEE = "annulee"
    PROBLEME = "probleme"
    REMBOURSEMENT = "remboursement"


TypeNotificationEnum = TypeNotificationEvenement


class NotificationCreate(BaseModel):
    """Schema interne aligné sur la table notifications."""

    utilisateur_identifiant: UUID
    type: TypeNotification
    titre: str
    message: str | None = None
    lien: str | None = None


class NotificationRead(BaseModel):
    """Schema de lecture aligné sur yok_db.sql."""

    identifiant: UUID
    utilisateur_identifiant: UUID
    type: TypeNotification
    titre: str
    message: str | None = None
    lien: str | None = None
    est_lue: bool
    date_lecture: datetime | None = None
    date_creation: datetime

    model_config = {"from_attributes": True}


class NotificationRequest(BaseModel):
    """Request pour déclencher une notification et éventuellement un email."""

    utilisateur_identifiant: UUID
    email_destinataire: EmailStr
    commande_identifiant: UUID
    type_event: TypeNotificationEvenement
    numero_commande: str | None = None
    montant_total: float | None = None
    date_livraison_estimee: str | None = None
    adresse_livraison: str | None = None
    raison_annulation: str | None = None
    message_probleme: str | None = None
    lien: str | None = None
