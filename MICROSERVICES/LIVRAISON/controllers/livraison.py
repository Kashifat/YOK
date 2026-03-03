from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from ..schemas.livraison import ActionRead, LivraisonCreate, LivraisonRead, LivraisonUpdateEntrepot, LivraisonUpdateLivree, LivraisonUpdateRamassage, LivraisonUpdateTransit
from ..services.autorisation_service import AutorisationService
from ..services.livraison_service import LivraisonService


router = APIRouter()
auth_vendeur = AutorisationService([RoleUtilisateur.VENDEUR, RoleUtilisateur.ADMINISTRATEUR])
auth_logistique = AutorisationService([RoleUtilisateur.ADMINISTRATEUR])
auth_admin = AutorisationService([RoleUtilisateur.ADMINISTRATEUR])


@router.post("", response_model=LivraisonRead, status_code=status.HTTP_201_CREATED)
def creer_livraison(payload: LivraisonCreate, utilisateur=Depends(auth_admin), db: Session = Depends(obtenir_session)):
	"""Crée/assigne une livraison pour une commande."""
	service = LivraisonService(db)
	return service.creer(payload, utilisateur)


@router.get("/{livraison_id}", response_model=LivraisonRead)
def obtenir_livraison(livraison_id: UUID, utilisateur=Depends(auth_logistique), db: Session = Depends(obtenir_session)):
	"""Récupère le détail d'une livraison."""
	service = LivraisonService(db)
	return service.obtenir(livraison_id)


@router.patch("/{livraison_id}/expedier-vendeur", response_model=LivraisonRead)
def expedier_vendeur(
	livraison_id: UUID,
	payload: LivraisonUpdateRamassage,
	utilisateur=Depends(auth_vendeur),
	db: Session = Depends(obtenir_session),
):
	"""Le vendeur expédie le colis -> commande EXPEDIEE."""
	service = LivraisonService(db)
	return service.signaler_expedition_vendeur(livraison_id, payload, utilisateur)


@router.patch("/{livraison_id}/ramassage-vendeur", response_model=LivraisonRead)
def ramassage_vendeur_legacy(
	livraison_id: UUID,
	payload: LivraisonUpdateRamassage,
	utilisateur=Depends(auth_vendeur),
	db: Session = Depends(obtenir_session),
):
	"""Alias legacy: redirige vers l'expédition vendeur."""
	service = LivraisonService(db)
	return service.signaler_expedition_vendeur(livraison_id, payload, utilisateur)


@router.patch("/{livraison_id}/en-transit", response_model=LivraisonRead)
def en_transit(
	livraison_id: UUID,
	payload: LivraisonUpdateTransit,
	utilisateur=Depends(auth_logistique),
	db: Session = Depends(obtenir_session),
):
	"""Le colis est en transit."""
	service = LivraisonService(db)
	return service.signaler_en_transit(livraison_id, payload, utilisateur)


@router.patch("/{livraison_id}/verification-entrepot-abidjan", response_model=LivraisonRead)
def verification_entrepot_abidjan(
	livraison_id: UUID,
	payload: LivraisonUpdateEntrepot,
	utilisateur=Depends(auth_logistique),
	db: Session = Depends(obtenir_session),
):
	"""Entrepôt Abidjan: vérification avant livraison finale."""
	service = LivraisonService(db)
	return service.verifier_entrepot_abidjan(livraison_id, payload, utilisateur)


@router.patch("/{livraison_id}/livree-client", response_model=LivraisonRead)
def livree_client(
	livraison_id: UUID,
	payload: LivraisonUpdateLivree,
	utilisateur=Depends(auth_logistique),
	db: Session = Depends(obtenir_session),
):
	"""Le livreur confirme livraison client avec preuve -> commande LIVREE."""
	service = LivraisonService(db)
	return service.signaler_livree_client(livraison_id, payload, utilisateur)


@router.get("/health/ping", response_model=ActionRead)
def ping():
	return {"message": "service livraison actif"}
