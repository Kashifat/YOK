from fastapi import Header, HTTPException, status
from jose import JWTError, jwt

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from ..config import settings


class AutorisationService:
	"""Valide le JWT et contrôle les rôles."""

	def __init__(self, roles: list[RoleUtilisateur] | None = None):
		self.roles = roles or []

	def __call__(self, authorization: str = Header(None)) -> dict:
		if not authorization or not authorization.startswith("Bearer "):
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token manquant")

		token = authorization.split(" ", 1)[1]

		try:
			payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
		except JWTError as exc:
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide") from exc

		if payload.get("type") != "access":
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")

		role = payload.get("role")
		if self.roles and role not in [r.value for r in self.roles]:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

		return payload
