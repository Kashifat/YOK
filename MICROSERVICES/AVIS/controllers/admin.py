from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from ..services.autorisation_service import AutorisationService
from ..services.avis_service import AvisService


router = APIRouter()
auth_admin = AutorisationService([RoleUtilisateur.ADMINISTRATEUR])


@router.delete("/avis/{avis_id}")
def supprimer_avis_moderation(avis_id: UUID, utilisateur=Depends(auth_admin), db: Session = Depends(obtenir_session)):
	"""Admin supprime n'importe quel avis (modération)."""
	service = AvisService(db)
	return service.supprimer(avis_id, utilisateur.get("sub"), True)
