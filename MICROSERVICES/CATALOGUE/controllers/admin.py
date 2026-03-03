from uuid import UUID

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from ..schemas.categorie import CategorieCreate, CategorieRead, CategorieUpdate
from ..schemas.produit import ProduitRead
from ..schemas.dashboard import DashboardAdmin, UtilisateurInfo, BoutiqueInfo
from ..services.autorisation_service import AutorisationService
from ..services.categorie_service import CategorieService
from ..services.produit_service import ProduitService
from ..services.dashboard_service import DashboardService


router = APIRouter()
auth_admin = AutorisationService([RoleUtilisateur.ADMINISTRATEUR])


@router.get("/categories", response_model=list[CategorieRead])
def lister_categories(db: Session = Depends(obtenir_session), _=Depends(auth_admin)):
	service = CategorieService(db)
	return service.lister_toutes()


@router.post("/categories", response_model=CategorieRead, status_code=status.HTTP_201_CREATED)
def creer_categorie(payload: CategorieCreate, db: Session = Depends(obtenir_session), _=Depends(auth_admin)):
	service = CategorieService(db)
	return service.creer(payload)


@router.patch("/categories/{categorie_id}", response_model=CategorieRead)
def maj_categorie(categorie_id: UUID, payload: CategorieUpdate, db: Session = Depends(obtenir_session), _=Depends(auth_admin)):
	service = CategorieService(db)
	return service.maj(categorie_id, payload)


@router.delete("/categories/{categorie_id}")
def desactiver_categorie(categorie_id: UUID, db: Session = Depends(obtenir_session), _=Depends(auth_admin)):
	service = CategorieService(db)
	return service.desactiver(categorie_id)


# ==================== DASHBOARD ADMIN ====================
@router.get("/dashboard", response_model=DashboardAdmin)
def obtenir_dashboard(db: Session = Depends(obtenir_session), _=Depends(auth_admin)):
	"""Dashboard admin avec statistiques globales"""
	service = DashboardService(db)
	return service.dashboard_admin()


# ==================== GESTION UTILISATEURS ====================
@router.get("/utilisateurs", response_model=list[UtilisateurInfo])
def lister_utilisateurs(role: str = Query(None), db: Session = Depends(obtenir_session), _=Depends(auth_admin)):
	"""Lister tous les utilisateurs (filtre par rôle optionnel)"""
	service = DashboardService(db)
	return service.lister_utilisateurs(role)


# ==================== GESTION BOUTIQUES ====================
@router.get("/boutiques", response_model=list[BoutiqueInfo])
def lister_boutiques(db: Session = Depends(obtenir_session), _=Depends(auth_admin)):
	"""Lister toutes les boutiques vendeurs avec leurs stats"""
	service = DashboardService(db)
	return service.lister_boutiques()


# ==================== GESTION PRODUITS ====================
@router.get("/produits", response_model=list[ProduitRead])
def lister_tous_produits(db: Session = Depends(obtenir_session), _=Depends(auth_admin)):
	"""Lister tous les produits (actifs et inactifs)"""
	service = ProduitService(db)
	return service.repo.lister_tous()


@router.get("/produits/recherche/{terme}", response_model=list[ProduitRead])
def rechercher_produits_admin(terme: str, db: Session = Depends(obtenir_session), _=Depends(auth_admin)):
	"""Rechercher des produits (admin voit tout)"""
	service = DashboardService(db)
	return service.rechercher_produits(terme)