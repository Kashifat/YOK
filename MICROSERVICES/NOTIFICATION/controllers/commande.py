"""
Controllers pour les notifications déclenchées par les commandes
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from ..schemas.notification import NotificationRequest, NotificationRead
from ..services.notification_service import NotificationService
from ..services.email_service import EmailService
from ..config import GMAIL_USER, GMAIL_APP_PASSWORD, EMAIL_FROM_NAME
from shared.db.conn import obtenir_session

router = APIRouter(prefix="/notifications", tags=["Notifications"])

def get_email_service() -> EmailService:
    """Dépendance pour le service email"""
    return EmailService(
        gmail_user=GMAIL_USER,
        gmail_app_password=GMAIL_APP_PASSWORD,
        email_from_name=EMAIL_FROM_NAME
    )

def get_notification_service(
    db: Session = Depends(obtenir_session),
    email_service: EmailService = Depends(get_email_service)
) -> NotificationService:
    """Dépendance pour le service notification"""
    return NotificationService(db=db, email_service=email_service)

@router.post(
    "/commande/confirmer",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Notifier confirmation de commande"
)
async def notifier_commande_confirmee(
    request: NotificationRequest,
    service: NotificationService = Depends(get_notification_service)
):
    """
    Endpoint webhook pour notifier la confirmation d'une commande
    
    Appelé depuis le service COMMANDE quand une commande est créée.
    """
    return await service.creer_et_envoyer_notification(request)

@router.post(
    "/commande/preparation",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Notifier début de préparation"
)
async def notifier_preparation_commencee(
    request: NotificationRequest,
    service: NotificationService = Depends(get_notification_service)
):
    """
    Endpoint webhook pour notifier le début de préparation
    
    Appelé depuis le service COMMANDE quand la préparation commence.
    """
    return await service.creer_et_envoyer_notification(request)

@router.post(
    "/commande/livraison",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Notifier livraison"
)
async def notifier_en_livraison(
    request: NotificationRequest,
    service: NotificationService = Depends(get_notification_service)
):
    """
    Endpoint webhook pour notifier l'expédition
    
    Appelé depuis le service COMMANDE quand la commande est expédiée.
    """
    return await service.creer_et_envoyer_notification(request)

@router.post(
    "/commande/livree",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Notifier livraison complète"
)
async def notifier_livree(
    request: NotificationRequest,
    service: NotificationService = Depends(get_notification_service)
):
    """
    Endpoint webhook pour notifier la livraison complète
    
    Appelé depuis le service COMMANDE quand la commande est livrée.
    """
    return await service.creer_et_envoyer_notification(request)

@router.post(
    "/commande/annulee",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Notifier annulation"
)
async def notifier_commande_annulee(
    request: NotificationRequest,
    service: NotificationService = Depends(get_notification_service)
):
    """
    Endpoint webhook pour notifier l'annulation d'une commande
    
    Appelé depuis le service COMMANDE quand une commande est annulée.
    """
    return await service.creer_et_envoyer_notification(request)

@router.post(
    "/commande/probleme",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Notifier un problème"
)
async def notifier_probleme(
    request: NotificationRequest,
    service: NotificationService = Depends(get_notification_service)
):
    """
    Endpoint webhook pour notifier un problème sur une commande
    
    Appelé depuis le service COMMANDE en cas d'erreur/problème.
    """
    return await service.creer_et_envoyer_notification(request)

@router.get(
    "/user/{utilisateur_id}",
    response_model=list[NotificationRead],
    summary="Lister les notifications d'un utilisateur"
)
async def lister_notifications_user(
    utilisateur_id: UUID,
    limit: int = 20,
    skip: int = 0,
    service: NotificationService = Depends(get_notification_service)
):
    """
    Récupérer l'historique des notifications d'un utilisateur
    
    Les utilisateurs CLIENT peuvent accéder à leurs propres notifications.
    """
    notifications = service.lister_notifications(
        utilisateur_id=utilisateur_id,
        limit=limit,
        skip=skip
    )
    return notifications
