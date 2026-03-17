from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from ..schemas.commande import CommandeRead, CommandeArticleUpdateStatut, CommandeArticleRead, ExpeditionAFaireRead
from ..services.autorisation_service import AutorisationService
from ..services.commande_service import CommandeService


router = APIRouter()
auth_vendeur = AutorisationService([RoleUtilisateur.VENDEUR, RoleUtilisateur.ADMINISTRATEUR])


@router.get("", response_model=list[CommandeRead])
def lister_mes_ventes(utilisateur=Depends(auth_vendeur), db: Session = Depends(obtenir_session)):
	"""Liste toutes les commandes contenant mes produits."""
	service = CommandeService(db)
	return service.lister_mes_ventes(utilisateur.get("sub"))


@router.get("/expeditions-a-faire", response_model=list[ExpeditionAFaireRead])
def mes_expeditions_a_faire(utilisateur=Depends(auth_vendeur), db: Session = Depends(obtenir_session)):
	"""Vue opérationnelle: articles à expédier (prêts et pas encore confirmés)."""
	service = CommandeService(db)
	return service.expeditions_a_faire(utilisateur.get("sub"))


@router.patch("/articles/{article_id}", response_model=CommandeArticleRead)
def maj_statut_article(article_id: UUID, payload: CommandeArticleUpdateStatut, utilisateur=Depends(auth_vendeur), db: Session = Depends(obtenir_session)):
	"""Met à jour le statut d'un article (EN_PREPARATION, EXPEDIEE, LIVREE)."""
	service = CommandeService(db)
	return service.maj_statut_article(article_id, utilisateur.get("sub"), payload)
