from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from ..schemas.panier import PanierArticleCreate, PanierArticleUpdate, PanierRead
from ..services.autorisation_service import AutorisationService
from ..services.panier_service import PanierService


router = APIRouter()
auth_client = AutorisationService([RoleUtilisateur.CLIENT, RoleUtilisateur.VENDEUR, RoleUtilisateur.ADMINISTRATEUR])


@router.get("", response_model=PanierRead)
def obtenir_mon_panier(utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Récupère le panier de l'utilisateur connecté."""
	service = PanierService(db)
	return service.obtenir_panier(utilisateur.get("sub"))


@router.post("/articles", status_code=status.HTTP_201_CREATED)
def ajouter_article(payload: PanierArticleCreate, utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Ajoute un article au panier (ou incrémente la quantité)."""
	service = PanierService(db)
	return service.ajouter_article(utilisateur.get("sub"), payload)


@router.patch("/articles/{produit_id}")
def maj_quantite_article(produit_id: UUID, payload: PanierArticleUpdate, variante_identifiant: UUID | None = None, utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Met à jour la quantité d'un article dans le panier."""
	service = PanierService(db)
	return service.maj_quantite(utilisateur.get("sub"), produit_id, payload, variante_identifiant)


@router.delete("/articles/{produit_id}")
def supprimer_article(produit_id: UUID, variante_identifiant: UUID | None = None, utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Supprime un article du panier."""
	service = PanierService(db)
	return service.supprimer_article(utilisateur.get("sub"), produit_id, variante_identifiant)


@router.delete("")
def vider_panier(utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Vide le panier."""
	service = PanierService(db)
	return service.vider_panier(utilisateur.get("sub"))
