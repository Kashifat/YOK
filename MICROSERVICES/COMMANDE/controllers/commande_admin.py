from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from ..schemas.commande import CommandeRead, CommandeUpdate
from ..services.autorisation_service import AutorisationService
from ..services.commande_service import CommandeService


router = APIRouter()
auth_admin = AutorisationService([RoleUtilisateur.ADMINISTRATEUR])


@router.get("", response_model=list[CommandeRead])
def lister_toutes_commandes(limite: int = 100, offset: int = 0, utilisateur=Depends(auth_admin), db: Session = Depends(obtenir_session)):
	"""Admin liste toutes les commandes."""
	service = CommandeService(db)
	return service.lister_toutes(limite, offset)


@router.get("/{commande_id}", response_model=CommandeRead)
def obtenir_commande(commande_id: UUID, utilisateur=Depends(auth_admin), db: Session = Depends(obtenir_session)):
	"""Admin récupère n'importe quelle commande."""
	service = CommandeService(db)
	return service.obtenir(commande_id)


@router.patch("/{commande_id}", response_model=CommandeRead)
def maj_commande(commande_id: UUID, payload: CommandeUpdate, utilisateur=Depends(auth_admin), db: Session = Depends(obtenir_session)):
	"""Admin met à jour une commande (statut, remarques)."""
	service = CommandeService(db)
	return service.maj_commande(commande_id, payload)
