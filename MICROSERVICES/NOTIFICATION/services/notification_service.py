"""
Service métier pour les notifications
"""
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import desc
import logging
from datetime import datetime

from ..models.notification import Notification, TypeNotification
from ..schemas.notification import NotificationRequest, TypeNotificationEnum
from .email_service import EmailService, TemplateEmail

logger = logging.getLogger(__name__)

class NotificationService:
    """Service métier pour la gestion des notifications"""
    
    def __init__(self, db: Session, email_service: EmailService):
        self.db = db
        self.email_service = email_service
        self.template = TemplateEmail()
    
    async def creer_et_envoyer_notification(
        self,
        request: NotificationRequest
    ) -> dict:
        """
        Créer une notification et l'envoyer par email
        
        Args:
            request: Données de la notification
        
        Returns:
            Résultat de l'envoi
        """
        try:
            # Déterminer le sujet et contenu selon le type
            sujet, contenu_html = self._generer_template(
                request.type_event,
                request.numero_commande or "",
                request.montant_total or 0.0,
                request.date_livraison_estimee or "",
                request.adresse_livraison or "",
                request.raison_annulation or "",
                request.message_probleme or ""
            )
            
            # Envoyer l'email
            succes, erreur = await self.email_service.envoyer_email(
                email_destinataire=request.email_destinataire,
                sujet=sujet,
                contenu_html=contenu_html
            )
            
            # Créer l'enregistrement en base
            notification = Notification(
                utilisateur_identifiant=request.utilisateur_identifiant,
                email_destinataire=request.email_destinataire,
                type_notification=TypeNotification[request.type_event.value.upper()],
                commande_identifiant=request.commande_identifiant,
                sujet=sujet,
                contenu_html=contenu_html,
                email_envoye=succes,
                date_envoi=datetime.utcnow() if succes else None,
                erreur_message=erreur
            )
            
            self.db.add(notification)
            self.db.commit()
            self.db.refresh(notification)
            
            return {
                "succes": succes,
                "notification_id": str(notification.identifiant),
                "erreur": erreur
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la création/envoi de notification: {str(e)}")
            self.db.rollback()
            return {
                "succes": False,
                "erreur": str(e)
            }
    
    def _generer_template(
        self,
        type_event: TypeNotificationEnum,
        numero_commande: str,
        montant_total: float,
        date_livraison: str,
        adresse_livraison: str,
        raison: str,
        message: str
    ) -> tuple[str, str]:
        """Générer le sujet et contenu selon le type d'événement"""
        
        # Nom client temporaire (à récupérer depuis la BD si nécessaire)
        nom_client = "Client YOK"
        
        if type_event == TypeNotificationEnum.COMMANDE_CONFIRMEE:
            sujet = f"Commande confirmée - #{numero_commande}"
            contenu = self.template.template_commande_confirmee(
                nom_client, numero_commande, montant_total, adresse_livraison
            )
        elif type_event == TypeNotificationEnum.PREPARATION_COMMENCEE:
            sujet = f"Votre commande #{numero_commande} est en cours de préparation"
            contenu = self.template.template_preparation_commencee(
                nom_client, numero_commande
            )
        elif type_event == TypeNotificationEnum.EN_LIVRAISON:
            sujet = f"Votre commande #{numero_commande} est en route!"
            contenu = self.template.template_en_livraison(
                nom_client, numero_commande, date_livraison
            )
        elif type_event == TypeNotificationEnum.LIVREE:
            sujet = f"Commande livrée - #{numero_commande}"
            contenu = self.template.template_livree(
                nom_client, numero_commande
            )
        elif type_event == TypeNotificationEnum.ANNULEE:
            sujet = f"Commande annulée - #{numero_commande}"
            contenu = self.template.template_annulee(
                nom_client, numero_commande, raison
            )
        elif type_event == TypeNotificationEnum.PROBLEME:
            sujet = f"Alerte sur votre commande - #{numero_commande}"
            contenu = self.template.template_probleme(
                nom_client, numero_commande, message
            )
        else:
            sujet = f"Notification - #{numero_commande}"
            contenu = "<p>Merci de votre confiance!</p>"
        
        return sujet, contenu
    
    def lister_notifications(
        self,
        utilisateur_id: UUID | None = None,
        limit: int = 20,
        skip: int = 0
    ) -> list[Notification]:
        """Lister les notifications"""
        query = self.db.query(Notification)
        
        if utilisateur_id:
            query = query.filter(Notification.utilisateur_identifiant == utilisateur_id)
        
        return query.order_by(desc(Notification.date_creation)).offset(skip).limit(limit).all()
    
    def obtenir_notification(self, notification_id: UUID) -> Notification | None:
        """Obtenir une notification par ID"""
        return self.db.query(Notification).filter(
            Notification.identifiant == notification_id
        ).first()
