from fastapi import Header, HTTPException, status
from jose import jwt, JWTError

from ..config import settings


class AutorisationService:
    """Service pour vérifier les autorisations"""

    def __init__(self, roles_autorises: list):
        self.roles_autorises = roles_autorises

    def __call__(self, authorization: str = Header(None)) -> dict:
        """Vérifie le token JWT et le rôle"""
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token manquant"
            )

        try:
            token = authorization.split(" ", 1)[1]

            # Décoder le token
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])

            if payload.get("type") != "access":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token invalide"
                )
            
            # Vérifier le rôle
            role = payload.get("role")
            if role not in [r.value if hasattr(r, 'value') else r for r in self.roles_autorises]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Accès refusé"
                )

            return payload

        except JWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide"
            ) from exc
