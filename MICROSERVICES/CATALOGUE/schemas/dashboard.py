from pydantic import BaseModel, UUID4
from datetime import datetime


class VendeurStats(BaseModel):
    """Statistiques d'un vendeur"""
    vendeur_id: UUID4
    nom_complet: str
    nom_entreprise: str | None
    total_produits: int
    produits_actifs: int
    total_ventes: int
    chiffre_affaires_cfa: int

    class Config:
        from_attributes = True


class DashboardVendeur(BaseModel):
    """Dashboard pour le vendeur"""
    vendeur_id: UUID4
    nom_entreprise: str | None
    total_produits: int
    produits_actifs: int
    produits_rupture_stock: int
    total_commandes: int
    commandes_en_cours: int
    chiffre_affaires_total_cfa: int
    chiffre_affaires_mois_cfa: int

    class Config:
        from_attributes = True


class ProduitStockInfo(BaseModel):
    """Info stock d'un produit"""
    identifiant: UUID4
    nom: str
    stock: int
    prix_cfa: int
    est_actif: bool
    date_creation: datetime

    class Config:
        from_attributes = True


class UtilisateurInfo(BaseModel):
    """Info utilisateur pour admin"""
    identifiant: UUID4
    role: str
    nom_complet: str
    courriel: str
    telephone: str | None
    est_actif: bool
    oauth_provider: str | None
    date_creation: datetime

    class Config:
        from_attributes = True


class BoutiqueInfo(BaseModel):
    """Info boutique pour admin"""
    vendeur_id: UUID4
    nom_complet: str
    courriel: str
    nom_entreprise: str | None
    statut_kyc: str | None
    total_produits: int
    chiffre_affaires_cfa: int

    class Config:
        from_attributes = True


class DashboardAdmin(BaseModel):
    """Dashboard admin"""
    total_utilisateurs: int
    total_clients: int
    total_vendeurs: int
    total_admins: int
    total_produits: int
    total_commandes: int
    chiffre_affaires_total_cfa: int

    class Config:
        from_attributes = True
