from pydantic import BaseModel, UUID4
from datetime import datetime


class FavoriCreate(BaseModel):
    """Schema pour ajouter un produit aux favoris"""
    produit_identifiant: UUID4


class FavoriRead(BaseModel):
    """Schema de lecture d'un favori avec détails produit"""
    identifiant: UUID4
    utilisateur_identifiant: UUID4
    produit_identifiant: UUID4
    date_creation: datetime
    
    # Détails du produit
    produit_nom: str | None = None
    produit_prix_cfa: int | None = None
    produit_stock: int | None = None
    produit_est_actif: bool | None = None

    class Config:
        from_attributes = True


class FavoriSimple(BaseModel):
    """Schema simple pour compter/lister les favoris"""
    identifiant: UUID4
    utilisateur_identifiant: UUID4
    produit_identifiant: UUID4
    date_creation: datetime

    class Config:
        from_attributes = True
