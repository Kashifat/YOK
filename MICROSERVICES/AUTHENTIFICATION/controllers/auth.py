from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from ..schemas.user import Token, TokenPaire, Renouvellement, UserCreate, UserLogin, UserRead
from ..services.auth_service import AuthService


router = APIRouter(tags=["auth"])


@router.post("/inscription", response_model=UserRead, status_code=201)
def inscrire(payload: UserCreate, db: Session = Depends(obtenir_session)):
	service = AuthService(db)
	utilisateur = service.inscription_utilisateur(payload)
	return utilisateur


@router.post("/connexion", response_model=TokenPaire)
def connecter(request: Request, payload: UserLogin, db: Session = Depends(obtenir_session)):
	service = AuthService(db)
	return service.connexion_utilisateur(payload)


@router.post("/renouveler", response_model=Token)
def renouveler(payload: Renouvellement, db: Session = Depends(obtenir_session)):
	service = AuthService(db)
	return service.renouveler_token(payload)


@router.post("/deconnecter")
def deconnecter(token: str, db: Session = Depends(obtenir_session)):
	"""Déconnexion - envoie le access_token dans le body."""
	service = AuthService(db)
	return service.deconnecter(token)
