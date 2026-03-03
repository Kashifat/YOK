from sqlalchemy.orm import Session
from sqlalchemy import and_
from uuid import UUID

from ..models.favori import Favori


class FavoriRepository:
    """Repository pour gérer les favoris"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, identifiant: UUID):
        """Récupérer un favori par ID"""
        return self.db.query(Favori).filter(Favori.identifiant == identifiant).first()

    def get_by_user_and_product(self, utilisateur_id: UUID, produit_id: UUID):
        """Vérifier si un produit est déjà dans les favoris"""
        return self.db.query(Favori).filter(
            and_(
                Favori.utilisateur_identifiant == utilisateur_id,
                Favori.produit_identifiant == produit_id
            )
        ).first()

    def lister_par_utilisateur(self, utilisateur_id: UUID):
        """Lister tous les favoris d'un utilisateur"""
        return self.db.query(Favori).filter(
            Favori.utilisateur_identifiant == utilisateur_id
        ).order_by(Favori.date_creation.desc()).all()

    def compter_par_utilisateur(self, utilisateur_id: UUID):
        """Compter le nombre de favoris d'un utilisateur"""
        return self.db.query(Favori).filter(
            Favori.utilisateur_identifiant == utilisateur_id
        ).count()

    def compter_par_produit(self, produit_id: UUID):
        """Compter combien d'utilisateurs ont mis ce produit en favori"""
        return self.db.query(Favori).filter(
            Favori.produit_identifiant == produit_id
        ).count()

    def ajouter(self, favori: Favori):
        """Ajouter un produit aux favoris"""
        self.db.add(favori)
        self.db.flush()
        return favori

    def supprimer(self, favori: Favori):
        """Retirer un produit des favoris"""
        self.db.delete(favori)
        self.db.flush()
        return True
