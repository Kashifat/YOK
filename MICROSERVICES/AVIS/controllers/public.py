from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from ..schemas.avis import AvisRead
from ..services.avis_service import AvisService


router = APIRouter()


@router.get("/produits/{produit_id}/avis", response_model=list[AvisRead])
def lister_avis_produit(produit_id: UUID, db: Session = Depends(obtenir_session)):
	"""Liste publique des avis d'un produit."""
	service = AvisService(db)
	return service.lister_par_produit(produit_id)


@router.get("/avis/{avis_id}", response_model=AvisRead)
def obtenir_avis(avis_id: UUID, db: Session = Depends(obtenir_session)):
	"""Détail d'un avis."""
	service = AvisService(db)
	return service.obtenir(avis_id)
