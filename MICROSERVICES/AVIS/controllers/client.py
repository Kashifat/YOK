from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from ..schemas.avis import AvisCreate, AvisRead, AvisUpdate, ImageAvisCreate, ImageAvisRead
from ..services.autorisation_service import AutorisationService
from ..services.avis_service import AvisService


router = APIRouter()
auth_client = AutorisationService([RoleUtilisateur.CLIENT, RoleUtilisateur.ADMINISTRATEUR])


@router.post("/avis", response_model=AvisRead, status_code=status.HTTP_201_CREATED)
def creer_avis(payload: AvisCreate, utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Client crée un avis pour un produit."""
	service = AvisService(db)
	return service.creer(utilisateur.get("sub"), payload)


@router.get("/mes-avis", response_model=list[AvisRead])
def lister_mes_avis(utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Liste tous les avis du client connecté."""
	from ..respositories.avis_repository import AvisRepository
	repo = AvisRepository(db)
	return repo.lister_par_client(utilisateur.get("sub"))


@router.patch("/avis/{avis_id}", response_model=AvisRead)
def maj_avis(avis_id: UUID, payload: AvisUpdate, utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Client modifie SON avis (ou admin modère)."""
	service = AvisService(db)
	role = utilisateur.get("role")
	est_admin = role == RoleUtilisateur.ADMINISTRATEUR.value
	return service.maj(avis_id, utilisateur.get("sub"), est_admin, payload)


@router.delete("/avis/{avis_id}")
def supprimer_avis(avis_id: UUID, utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Client supprime SON avis (ou admin modère)."""
	service = AvisService(db)
	role = utilisateur.get("role")
	est_admin = role == RoleUtilisateur.ADMINISTRATEUR.value
	return service.supprimer(avis_id, utilisateur.get("sub"), est_admin)


@router.post("/avis/{avis_id}/images", response_model=ImageAvisRead, status_code=status.HTTP_201_CREATED)
def ajouter_image_avis(avis_id: UUID, payload: ImageAvisCreate, utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Client ajoute une image à SON avis."""
	service = AvisService(db)
	role = utilisateur.get("role")
	est_admin = role == RoleUtilisateur.ADMINISTRATEUR.value
	return service.ajouter_image(avis_id, utilisateur.get("sub"), est_admin, payload)
