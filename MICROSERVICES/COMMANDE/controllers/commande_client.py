from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from ..schemas.commande import CommandeCreate, CommandeCreationRead, CommandeRead
from ..services.autorisation_service import AutorisationService
from ..services.commande_service import CommandeService


router = APIRouter()
auth_client = AutorisationService([RoleUtilisateur.CLIENT, RoleUtilisateur.VENDEUR, RoleUtilisateur.ADMINISTRATEUR])


@router.post("", response_model=CommandeCreationRead, status_code=status.HTTP_201_CREATED)
def creer_commande(payload: CommandeCreate, utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Crée une commande à partir du panier."""
	service = CommandeService(db)
	return service.creer_depuis_panier(utilisateur, payload)


@router.get("", response_model=list[CommandeRead])
def lister_mes_commandes(utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Liste toutes mes commandes."""
	service = CommandeService(db)
	return service.lister_mes_commandes(utilisateur.get("sub"))


@router.get("/{commande_id}", response_model=CommandeRead)
def obtenir_commande(commande_id: UUID, utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Récupère le détail d'une commande."""
	service = CommandeService(db)
	return service.obtenir_commande_client(commande_id, utilisateur.get("sub"))


@router.delete("/{commande_id}")
def annuler_commande(commande_id: UUID, utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Annule une commande (seulement si EN_ATTENTE_PAIEMENT)."""
	service = CommandeService(db)
	return service.annuler_commande(commande_id, utilisateur.get("sub"))
