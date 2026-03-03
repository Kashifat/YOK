from uuid import UUID

from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from ..schemas.favori import FavoriCreate, FavoriRead, FavoriSimple
from ..services.autorisation_service import AutorisationService
from ..services.favori_service import FavoriService


router = APIRouter()
auth_client = AutorisationService([RoleUtilisateur.CLIENT, RoleUtilisateur.VENDEUR, RoleUtilisateur.ADMINISTRATEUR])


@router.get("/mes-favoris", response_model=list[FavoriRead])
def lister_mes_favoris(
    utilisateur=Depends(auth_client),
    db: Session = Depends(obtenir_session)
):
    """Lister tous mes produits favoris"""
    service = FavoriService(db)
    return service.lister_mes_favoris(utilisateur.get("sub"))


@router.post("/ajouter", response_model=FavoriSimple, status_code=status.HTTP_201_CREATED)
def ajouter_favori(
    payload: FavoriCreate,
    utilisateur=Depends(auth_client),
    db: Session = Depends(obtenir_session)
):
    """Ajouter un produit à mes favoris"""
    service = FavoriService(db)
    return service.ajouter_favori(utilisateur.get("sub"), payload)


@router.delete("/retirer/{produit_id}", status_code=status.HTTP_204_NO_CONTENT)
def retirer_favori(
    produit_id: UUID,
    utilisateur=Depends(auth_client),
    db: Session = Depends(obtenir_session)
):
    """Retirer un produit de mes favoris"""
    service = FavoriService(db)
    service.retirer_favori(utilisateur.get("sub"), produit_id)
    return None


@router.get("/verifier/{produit_id}")
def verifier_favori(
    produit_id: UUID,
    utilisateur=Depends(auth_client),
    db: Session = Depends(obtenir_session)
):
    """Vérifier si un produit est dans mes favoris"""
    service = FavoriService(db)
    return service.verifier_favori(utilisateur.get("sub"), produit_id)


@router.get("/count")
def compter_favoris(
    utilisateur=Depends(auth_client),
    db: Session = Depends(obtenir_session)
):
    """Compter mes favoris"""
    service = FavoriService(db)
    return service.compter_mes_favoris(utilisateur.get("sub"))


@router.get("/produit/{produit_id}/popularite")
def popularite_produit(
    produit_id: UUID,
    db: Session = Depends(obtenir_session)
):
    """Voir combien d'utilisateurs ont mis ce produit en favori (route publique)"""
    service = FavoriService(db)
    return service.popularite_produit(produit_id)
