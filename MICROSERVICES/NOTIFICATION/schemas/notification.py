"""
Pydantic schemas pour les notifications
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID
from enum import Enum

class TypeNotificationEnum(str, Enum):
    """Types de notifications"""
    COMMANDE_CONFIRMEE = "commande_confirmee"
    PREPARATION_COMMENCEE = "preparation_commencee"
    EN_LIVRAISON = "en_livraison"
    LIVREE = "livree"
    ANNULEE = "annulee"
    PROBLEME = "probleme"
    REMBOURSEMENT = "remboursement"

class NotificationCreate(BaseModel):
    """Schema pour créer une notification"""
    utilisateur_identifiant: UUID
    email_destinataire: EmailStr
    type_notification: TypeNotificationEnum
    commande_identifiant: UUID | None = None
    sujet: str
    contenu_html: str

class NotificationRead(BaseModel):
    """Schema pour lire une notification"""
    identifiant: UUID
    utilisateur_identifiant: UUID
    email_destinataire: str
    type_notification: TypeNotificationEnum
    commande_identifiant: UUID | None
    sujet: str
    email_envoye: bool
    date_envoi: datetime | None
    erreur_message: str | None
    date_creation: datetime
    
    class Config:
        from_attributes = True

class NotificationRequest(BaseModel):
    """Request pour trigger une notification depuis COMMANDE"""
    utilisateur_identifiant: UUID
    email_destinataire: EmailStr
    commande_identifiant: UUID
    type_event: TypeNotificationEnum
    # Données optionnelles pour template
    numero_commande: str | None = None
    montant_total: float | None = None
    date_livraison_estimee: str | None = None
    adresse_livraison: str | None = None
    raison_annulation: str | None = None
    message_probleme: str | None = None
