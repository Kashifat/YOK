from uuid import UUID

from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from ..schemas.paiement import ActionRead, PaiementInitialisationCreate, PaiementInitialisationRead, PaiementRead, PaiementVerificationRead
from ..services.autorisation_service import AutorisationService
from ..services.paiement_service import PaiementService


router = APIRouter()
auth_client = AutorisationService([RoleUtilisateur.CLIENT, RoleUtilisateur.ADMINISTRATEUR])


@router.post("/initialiser", response_model=PaiementInitialisationRead, status_code=status.HTTP_201_CREATED)
def initialiser_paiement(
	payload: PaiementInitialisationCreate,
	utilisateur=Depends(auth_client),
	db: Session = Depends(obtenir_session),
):
	"""Initialise un paiement CinetPay pour une commande."""
	service = PaiementService(db)
	return service.initialiser(utilisateur, payload)


@router.get("/commande/{commande_id}", response_model=PaiementRead)
def obtenir_paiement_commande(
	commande_id: UUID,
	utilisateur=Depends(auth_client),
	db: Session = Depends(obtenir_session),
):
	"""Récupère le paiement associé à une commande."""
	service = PaiementService(db)
	return service.obtenir_par_commande(commande_id, utilisateur)


@router.get("/retour/cinetpay", response_model=PaiementVerificationRead)
def retour_frontend_cinetpay(
	transaction_id: str,
	utilisateur=Depends(auth_client),
	db: Session = Depends(obtenir_session),
):
	"""Retour frontend CinetPay avec tentative de vérification immédiate."""
	service = PaiementService(db)
	return service.retour_frontend(transaction_id, utilisateur)


@router.get("/{paiement_id}", response_model=PaiementRead)
def obtenir_paiement(paiement_id: UUID, utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Détail d'un paiement."""
	service = PaiementService(db)
	return service.obtenir(paiement_id, utilisateur)


@router.post("/{paiement_id}/verifier", response_model=PaiementVerificationRead)
def verifier_paiement(paiement_id: UUID, utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Vérifie le statut d'un paiement auprès de CinetPay."""
	service = PaiementService(db)
	return service.verifier(paiement_id, utilisateur)


@router.post("/webhooks/cinetpay", response_model=PaiementVerificationRead)
def webhook_cinetpay(
	payload: dict,
	x_cinetpay_signature: str | None = Header(default=None),
	db: Session = Depends(obtenir_session),
):
	"""Webhook CinetPay (source de vérité serveur)."""
	service = PaiementService(db)
	return service.traiter_webhook_brut(payload, signature_header=x_cinetpay_signature)


@router.get("/webhooks/cinetpay/health", response_model=ActionRead)
def webhook_health():
	"""Health endpoint pour monitorer la route webhook."""
	return {"message": "webhook endpoint actif"}
