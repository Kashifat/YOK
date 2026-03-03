from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from ..schemas.categorie import CategorieRead
from ..schemas.produit import ProduitRead
from ..services.categorie_service import CategorieService
from ..services.produit_service import ProduitService


router = APIRouter()


@router.get("/categories", response_model=list[CategorieRead])
def lister_categories(db: Session = Depends(obtenir_session)):
	service = CategorieService(db)
	return service.lister_actives()


@router.get("/categories/{categorie_id}", response_model=CategorieRead)
def obtenir_categorie(categorie_id: UUID, db: Session = Depends(obtenir_session)):
	service = CategorieService(db)
	return service.obtenir(categorie_id)


@router.get("/produits", response_model=list[ProduitRead])
def lister_produits(categorie_id: UUID | None = None, db: Session = Depends(obtenir_session)):
	service = ProduitService(db)
	return service.lister_public(categorie_id=categorie_id)


@router.get("/produits/{produit_id}", response_model=ProduitRead)
def obtenir_produit(produit_id: UUID, db: Session = Depends(obtenir_session)):
	service = ProduitService(db)
	return service.obtenir_public(produit_id)

@router.get("/produits/recherche/{terme}", response_model=list[ProduitRead])
def rechercher_produits(terme: str, db: Session = Depends(obtenir_session)):
    service = ProduitService(db)
    return service.rechercher_public(terme)

