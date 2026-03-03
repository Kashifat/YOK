from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from ..schemas.produit import ProduitCreate, ProduitRead, ProduitUpdate
from ..schemas.media import ImageCreate, ImageRead, VideoCreate, VideoRead
from ..schemas.dashboard import DashboardVendeur, ProduitStockInfo
from ..services.autorisation_service import AutorisationService
from ..services.produit_service import ProduitService
from ..services.dashboard_service import DashboardService


router = APIRouter()
auth_vendeur = AutorisationService([RoleUtilisateur.VENDEUR, RoleUtilisateur.ADMINISTRATEUR])


@router.get("/produits", response_model=list[ProduitRead])
def lister_mes_produits(utilisateur=Depends(auth_vendeur), db: Session = Depends(obtenir_session)):
	service = ProduitService(db)
	return service.lister_vendeur(utilisateur.get("sub"))


@router.post("/produits", response_model=ProduitRead, status_code=status.HTTP_201_CREATED)
def creer_produit(payload: ProduitCreate, utilisateur=Depends(auth_vendeur), db: Session = Depends(obtenir_session)):
	service = ProduitService(db)
	return service.creer(utilisateur.get("sub"), payload)


@router.patch("/produits/{produit_id}", response_model=ProduitRead)
def maj_produit(produit_id: UUID, payload: ProduitUpdate, utilisateur=Depends(auth_vendeur), db: Session = Depends(obtenir_session)):
	service = ProduitService(db)
	role = utilisateur.get("role")
	est_admin = role == RoleUtilisateur.ADMINISTRATEUR.value
	return service.maj(produit_id, utilisateur.get("sub"), est_admin, payload)


@router.delete("/produits/{produit_id}")
def desactiver_produit(produit_id: UUID, utilisateur=Depends(auth_vendeur), db: Session = Depends(obtenir_session)):
	service = ProduitService(db)
	role = utilisateur.get("role")
	est_admin = role == RoleUtilisateur.ADMINISTRATEUR.value
	return service.desactiver(produit_id, utilisateur.get("sub"), est_admin)


@router.post("/produits/{produit_id}/images", response_model=ImageRead, status_code=status.HTTP_201_CREATED)
def ajouter_image(produit_id: UUID, payload: ImageCreate, utilisateur=Depends(auth_vendeur), db: Session = Depends(obtenir_session)):
	service = ProduitService(db)
	role = utilisateur.get("role")
	est_admin = role == RoleUtilisateur.ADMINISTRATEUR.value
	return service.ajouter_image(produit_id, utilisateur.get("sub"), est_admin, payload)


@router.post("/produits/{produit_id}/videos", response_model=VideoRead, status_code=status.HTTP_201_CREATED)
def ajouter_video(produit_id: UUID, payload: VideoCreate, utilisateur=Depends(auth_vendeur), db: Session = Depends(obtenir_session)):
	service = ProduitService(db)
	role = utilisateur.get("role")
	est_admin = role == RoleUtilisateur.ADMINISTRATEUR.value
	return service.ajouter_video(produit_id, utilisateur.get("sub"), est_admin, payload)


# ==================== DASHBOARD VENDEUR ====================
@router.get("/dashboard", response_model=DashboardVendeur)
def obtenir_dashboard(utilisateur=Depends(auth_vendeur), db: Session = Depends(obtenir_session)):
	"""Dashboard avec statistiques du vendeur"""
	service = DashboardService(db)
	return service.dashboard_vendeur(utilisateur.get("sub"))


@router.get("/stock", response_model=list[ProduitStockInfo])
def lister_stock(utilisateur=Depends(auth_vendeur), db: Session = Depends(obtenir_session)):
	"""Liste des produits avec leur stock (triés par stock croissant)"""
	service = DashboardService(db)
	return service.stock_vendeur(utilisateur.get("sub"))


@router.get("/produits/recherche/{terme}", response_model=list[ProduitRead])
def rechercher_mes_produits(terme: str, utilisateur=Depends(auth_vendeur), db: Session = Depends(obtenir_session)):
	"""Rechercher dans mes propres produits"""
	service = DashboardService(db)
	return service.rechercher_produits(terme, vendeur_id=utilisateur.get("sub"))