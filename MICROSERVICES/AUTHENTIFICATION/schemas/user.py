from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from ..models.user import RoleUtilisateur


class UserBase(BaseModel):
    courriel: EmailStr
    nom_complet: str
    telephone: str | None = None


class UserCreate(UserBase):
    mot_de_passe: str | None = Field(default=None, min_length=8)


class UserLogin(BaseModel):
    courriel: EmailStr
    mot_de_passe: str


class UserRead(UserBase):
    identifiant: UUID
    role: RoleUtilisateur
    oauth_provider: str | None = None
    photo_url: str | None = None
    est_actif: bool
    date_creation: datetime

    model_config = {"from_attributes": True}


class TokenPaire(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Renouvellement(BaseModel):
    refresh_token: str


# ========== OAuth ==========

class OAuthUserData(BaseModel):
    """Données utilisateur récupérées depuis le provider OAuth."""
    email: str
    name: str
    picture: str | None = None
    provider: str  # 'google' ou 'facebook'
    provider_user_id: str


class OAuthCallback(BaseModel):
    """Callback OAuth avec le code d'autorisation."""
    code: str
    state: str | None = None
