from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from ..schemas.wallet import ActionRead, EvenementCommandeCreate, WalletDetailsRead
from ..services.autorisation_service import AutorisationService
from ..services.wallet_service import WalletService


router = APIRouter()
auth_vendeur = AutorisationService([RoleUtilisateur.VENDEUR, RoleUtilisateur.ADMINISTRATEUR])
auth_admin = AutorisationService([RoleUtilisateur.ADMINISTRATEUR])


@router.post("/evenements/commande", response_model=ActionRead, status_code=status.HTTP_200_OK)
def evenement_commande(payload: EvenementCommandeCreate, utilisateur=Depends(auth_admin), db: Session = Depends(obtenir_session)):
	"""Synchronise les wallets vendeurs selon le statut de commande."""
	service = WalletService(db)
	return service.traiter_evenement_commande(payload.commande_identifiant, payload.nouveau_statut, payload.source)


@router.get("/moi", response_model=WalletDetailsRead)
def mon_wallet(utilisateur=Depends(auth_vendeur), db: Session = Depends(obtenir_session)):
	"""Wallet du vendeur connecté."""
	service = WalletService(db)
	return service.mon_wallet(utilisateur)


@router.get("/{vendeur_id}", response_model=WalletDetailsRead)
def wallet_vendeur(vendeur_id: UUID, utilisateur=Depends(auth_admin), db: Session = Depends(obtenir_session)):
	"""Wallet détaillé d'un vendeur (admin)."""
	service = WalletService(db)
	return service.wallet_vendeur(vendeur_id)
