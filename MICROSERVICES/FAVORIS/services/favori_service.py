from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from uuid import UUID

from ..models.favori import Favori
from ..respositories.favori_repository import FavoriRepository
from ..schemas.favori import FavoriCreate


class FavoriService:
    """Service métier pour gérer les favoris"""

    def __init__(self, db: Session):
        self.db = db
        self.repo = FavoriRepository(db)

    def lister_mes_favoris(self, utilisateur_id: UUID):
        """Lister les favoris d'un utilisateur avec les détails des produits"""
        favoris = self.repo.lister_par_utilisateur(utilisateur_id)
        
        # Enrichir avec les détails des produits
        from MICROSERVICES.CATALOGUE.models.produit import Produit
        
        resultats = []
        for fav in favoris:
            produit = self.db.query(Produit).filter(Produit.identifiant == fav.produit_identifiant).first()
            
            fav_dict = {
                "identifiant": fav.identifiant,
                "utilisateur_identifiant": fav.utilisateur_identifiant,
                "produit_identifiant": fav.produit_identifiant,
                "date_creation": fav.date_creation,
                "produit_nom": produit.nom if produit else None,
                "produit_prix_cfa": produit.prix_cfa if produit else None,
                "produit_stock": produit.stock if produit else None,
                "produit_est_actif": produit.est_actif if produit else None
            }
            resultats.append(fav_dict)
        
        return resultats

    def ajouter_favori(self, utilisateur_id: UUID, payload: FavoriCreate):
        """Ajouter un produit aux favoris"""
        # Vérifier que le produit existe
        from MICROSERVICES.CATALOGUE.models.produit import Produit
        produit = self.db.query(Produit).filter(Produit.identifiant == payload.produit_identifiant).first()
        
        if not produit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produit introuvable"
            )

        # Vérifier si déjà en favoris
        existe = self.repo.get_by_user_and_product(utilisateur_id, payload.produit_identifiant)
        if existe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ce produit est déjà dans vos favoris"
            )

        # Ajouter aux favoris
        favori = Favori(
            utilisateur_identifiant=utilisateur_id,
            produit_identifiant=payload.produit_identifiant
        )
        return self.repo.ajouter(favori)

    def retirer_favori(self, utilisateur_id: UUID, produit_id: UUID):
        """Retirer un produit des favoris"""
        favori = self.repo.get_by_user_and_product(utilisateur_id, produit_id)
        
        if not favori:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ce produit n'est pas dans vos favoris"
            )

        return self.repo.supprimer(favori)

    def verifier_favori(self, utilisateur_id: UUID, produit_id: UUID):
        """Vérifier si un produit est dans les favoris"""
        favori = self.repo.get_by_user_and_product(utilisateur_id, produit_id)
        return {"est_favori": favori is not None}

    def compter_mes_favoris(self, utilisateur_id: UUID):
        """Compter le nombre de favoris d'un utilisateur"""
        count = self.repo.compter_par_utilisateur(utilisateur_id)
        return {"total_favoris": count}

    def popularite_produit(self, produit_id: UUID):
        """Nombre d'utilisateurs ayant ajouté ce produit en favori"""
        count = self.repo.compter_par_produit(produit_id)
        return {"nombre_favoris": count}
