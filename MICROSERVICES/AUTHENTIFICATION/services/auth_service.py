from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from shared.security.password import hash_password, verify_password

from ..config import settings
from ..respositories.user_repository import UserRepository
from ..schemas.user import Token, TokenPaire, UserCreate, UserLogin, Renouvellement
from ..models.user import RoleUtilisateur
from ..utilitaires.blacklist import ajouter_blacklist, est_blacklist


class AuthService:
    """Logique métier pour l'authentification."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def inscription_utilisateur(self, payload: UserCreate):
        # CLIENT : OAuth obligatoire (pas de mot de passe)
        # VENDEUR/ADMIN : Email + mot de passe obligatoire
        role = RoleUtilisateur.CLIENT

        if self.repo.get_by_email(payload.courriel):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Courriel déjà utilisé"
            )

        # Le mot de passe est obligatoire pour l'inscription classique
        if not payload.mot_de_passe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mot de passe requis pour l'inscription"
            )

        mot_de_passe_hash = hash_password(payload.mot_de_passe)

        try:
            utilisateur = self.repo.creer_utilisateur(
                courriel=payload.courriel,
                nom_complet=payload.nom_complet,
                mot_de_passe_hash=mot_de_passe_hash,
                role=role,
                telephone=payload.telephone,
            )
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Courriel ou téléphone déjà utilisé"
            )

        return utilisateur

    def connexion_utilisateur(self, payload: UserLogin) -> TokenPaire:
        utilisateur = self.repo.get_by_email(payload.courriel)
        if not utilisateur:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Identifiants invalides"
            )

        if not verify_password(payload.mot_de_passe, utilisateur.mot_de_passe_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Identifiants invalides"
            )

        if not utilisateur.est_actif:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Compte désactivé"
            )

        access_token = self._creer_token(
            data={"sub": str(utilisateur.identifiant), "role": utilisateur.role.value, "type": "access"},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )
        refresh_token = self._creer_token(
            data={"sub": str(utilisateur.identifiant), "type": "refresh"},
            expires_delta=timedelta(days=settings.refresh_token_expire_days)
        )
        return TokenPaire(access_token=access_token, refresh_token=refresh_token)

    def renouveler_token(self, payload: Renouvellement) -> Token:
        donnees = self.decoder_token(payload.refresh_token)
        
        if donnees.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide"
            )

        utilisateur_id = donnees.get("sub")
        utilisateur = self.repo.get_by_id(utilisateur_id)
        
        if not utilisateur or not utilisateur.est_actif:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Utilisateur inactif"
            )

        access_token = self._creer_token(
            data={"sub": utilisateur_id, "role": utilisateur.role.value, "type": "access"},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )
        return Token(access_token=access_token)

    def deconnecter(self, token: str) -> dict:
        ajouter_blacklist(token)
        return {"message": "Déconnexion réussie"}

    def _creer_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        a_encoder = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        a_encoder.update({"exp": expire})

        return jwt.encode(
            a_encoder,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )

    def decoder_token(self, token: str) -> dict:
        if est_blacklist(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token révoqué"
            )
        
        try:
            return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        except JWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide"
            ) from exc

    # ========== OAuth ==========

    def oauth_login_ou_inscription(self, oauth_data: "OAuthUserData"):
        """Connecte ou crée un utilisateur via OAuth (CLIENT uniquement)."""
        from ..schemas.user import OAuthUserData
        
        # Chercher par OAuth ID
        utilisateur = self.repo.get_by_oauth(oauth_data.provider, oauth_data.provider_user_id)
        
        if utilisateur:
            # Utilisateur existe déjà via OAuth
            if not utilisateur.est_actif:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Compte désactivé"
                )
        else:
            # Vérifier si email existe déjà (compte classique)
            utilisateur_email = self.repo.get_by_email(oauth_data.email)
            if utilisateur_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cet email est déjà utilisé avec un compte classique"
                )
            
            # Créer nouvel utilisateur OAuth (CLIENT)
            try:
                utilisateur = self.repo.creer_utilisateur(
                    courriel=oauth_data.email,
                    nom_complet=oauth_data.name,
                    role=RoleUtilisateur.CLIENT,
                    oauth_provider=oauth_data.provider,
                    oauth_id=oauth_data.provider_user_id,
                    photo_url=oauth_data.picture,
                    mot_de_passe_hash=None,
                )
            except IntegrityError:
                self.db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Erreur lors de la création du compte"
                )
        
        # Générer tokens
        access_token = self._creer_token(
            data={"sub": str(utilisateur.identifiant), "role": utilisateur.role.value, "type": "access"},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )
        refresh_token = self._creer_token(
            data={"sub": str(utilisateur.identifiant), "type": "refresh"},
            expires_delta=timedelta(days=settings.refresh_token_expire_days)
        )
        return TokenPaire(access_token=access_token, refresh_token=refresh_token)
