from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from ..schemas.wallet import (
	ActionRead,
	EvenementCommandeCreate,
	VendeurCompteFinancierRead,
	VendeurFinanceDashboardRead,
	VendeurFinanceTransactionsRead,
	VersementVendeurCreate,
	VersementVendeurRead,
	WalletDetailsRead,
)
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


@router.get("/moi", response_model=VendeurCompteFinancierRead)
def mon_wallet(utilisateur=Depends(auth_vendeur), db: Session = Depends(obtenir_session)):
	"""Vue financière vendeur (vocabulaire business, sans notion de portefeuille bancaire)."""
	service = WalletService(db)
	return service.mon_wallet(utilisateur)


@router.get("/finance/dashboard", response_model=VendeurFinanceDashboardRead)
def dashboard_financier(utilisateur=Depends(auth_vendeur), db: Session = Depends(obtenir_session)):
	"""Tableau financier vendeur (sans logique portefeuille bancaire)."""
	service = WalletService(db)
	return service.dashboard_financier_vendeur(utilisateur)


@router.get("/finance/transactions", response_model=VendeurFinanceTransactionsRead)
def transactions_financieres(
	statut: str | None = None,
	limite: int = 100,
	utilisateur=Depends(auth_vendeur),
	db: Session = Depends(obtenir_session),
):
	"""Historique vendeur: commande, produit, quantité, montant vendeur, statut financier."""
	service = WalletService(db)
	return service.transactions_financieres_vendeur(utilisateur, statut=statut, limite=limite)


@router.post("/finance/versements", response_model=VersementVendeurRead, status_code=status.HTTP_200_OK)
def enregistrer_versement(payload: VersementVendeurCreate, utilisateur=Depends(auth_admin), db: Session = Depends(obtenir_session)):
	"""Action admin/compta: enregistre un versement réel au vendeur."""
	service = WalletService(db)
	return service.enregistrer_versement_admin(payload)


@router.get("/{vendeur_id}", response_model=WalletDetailsRead)
def wallet_vendeur(vendeur_id: UUID, utilisateur=Depends(auth_admin), db: Session = Depends(obtenir_session)):
	"""Wallet détaillé d'un vendeur (admin)."""
	service = WalletService(db)
	return service.wallet_vendeur(vendeur_id)
