"""
Modèle SQLAlchemy pour les notifications
"""
from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import enum
from shared.db.base import Base

class TypeNotification(str, enum.Enum):
    """Types de notifications"""
    COMMANDE_CONFIRMEE = "commande_confirmee"
    PREPARATION_COMMENCEE = "preparation_commencee"
    EN_LIVRAISON = "en_livraison"
    LIVREE = "livree"
    ANNULEE = "annulee"
    PROBLEME = "probleme"
    REMBOURSEMENT = "remboursement"

class Notification(Base):
    """
    Table pour tracer les notifications envoyées
    """
    __tablename__ = "notifications"
    
    identifiant = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Référence utilisateur
    utilisateur_identifiant = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Email destinataire
    email_destinataire = Column(String(255), nullable=False)
    
    # Type d'événement
    type_notification = Column(SQLEnum(TypeNotification), nullable=False, index=True)
    
    # Référence commande
    commande_identifiant = Column(UUID(as_uuid=True), nullable=True, index=True)
    
    # Contenu de l'email
    sujet = Column(String(255), nullable=False)
    contenu_html = Column(Text, nullable=False)
    
    # Statut d'envoi
    email_envoye = Column(Boolean, default=False, index=True)
    date_envoi = Column(DateTime, nullable=True)
    erreur_message = Column(String(500), nullable=True)
    
    # Timestamps
    date_creation = Column(DateTime, default=datetime.utcnow)
    date_modification = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Notification {self.identifiant} - {self.type_notification}>"
