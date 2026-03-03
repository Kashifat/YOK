from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from fastapi import HTTPException, status
from uuid import UUID
import logging

from MICROSERVICES.AUTHENTIFICATION.models.user import Utilisateur, ProfilVendeur, RoleUtilisateur
from MICROSERVICES.COMMANDE.models.commande import Commande, CommandeArticle, StatutCommande
from ..models.produit import Produit


logger = logging.getLogger(__name__)


class DashboardService:
    """Service pour les dashboards et statistiques"""

    def __init__(self, db: Session):
        self.db = db

    def dashboard_vendeur(self, vendeur_id: UUID):
        """Dashboard pour un vendeur"""
        # Vérifier que c'est un vendeur
        vendeur = self.db.query(Utilisateur).filter(Utilisateur.identifiant == vendeur_id).first()
        if not vendeur or vendeur.role != RoleUtilisateur.VENDEUR:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

        # Profil vendeur
        profil = self.db.query(ProfilVendeur).filter(ProfilVendeur.utilisateur_identifiant == vendeur_id).first()

        # Stats produits
        total_produits = self.db.query(func.count(Produit.identifiant)).filter(
            Produit.vendeur_identifiant == vendeur_id
        ).scalar() or 0

        produits_actifs = self.db.query(func.count(Produit.identifiant)).filter(
            and_(
                Produit.vendeur_identifiant == vendeur_id,
                Produit.est_actif == True
            )
        ).scalar() or 0

        produits_rupture = self.db.query(func.count(Produit.identifiant)).filter(
            and_(
                Produit.vendeur_identifiant == vendeur_id,
                Produit.stock == 0,
                Produit.est_actif == True
            )
        ).scalar() or 0

        # Stats commandes (nécessite table commande_articles)
        total_commandes = 0
        commandes_en_cours = 0
        chiffre_affaires_total = 0
        chiffre_affaires_mois = 0

        # Stats commandes (si les tables COMMANDE sont disponibles dans le même schéma)
        try:
            total_commandes = self.db.query(func.count(func.distinct(CommandeArticle.commande_identifiant))).filter(
                CommandeArticle.vendeur_identifiant == vendeur_id
            ).scalar() or 0

            commandes_en_cours = self.db.query(func.count(func.distinct(CommandeArticle.commande_identifiant))).filter(
                and_(
                    CommandeArticle.vendeur_identifiant == vendeur_id,
                    CommandeArticle.statut.in_([
                        StatutCommande.EN_ATTENTE_PAIEMENT,
                        StatutCommande.PAYEE,
                        StatutCommande.EN_PREPARATION,
                        StatutCommande.EXPEDIEE,
                    ])
                )
            ).scalar() or 0

            chiffre_affaires_total = self.db.query(func.sum(CommandeArticle.total_ligne_cfa)).filter(
                and_(
                    CommandeArticle.vendeur_identifiant == vendeur_id,
                    CommandeArticle.statut != StatutCommande.ANNULEE
                )
            ).scalar() or 0

            chiffre_affaires_mois = self.db.query(func.sum(CommandeArticle.total_ligne_cfa)).filter(
                and_(
                    CommandeArticle.vendeur_identifiant == vendeur_id,
                    CommandeArticle.statut != StatutCommande.ANNULEE,
                    func.date_trunc('month', CommandeArticle.date_creation) == func.date_trunc('month', func.now())
                )
            ).scalar() or 0
        except Exception as exc:
            logger.warning("Stats commandes indisponibles (dashboard vendeur): %s", exc)

        return {
            "vendeur_id": vendeur_id,
            "nom_entreprise": profil.nom_entreprise if profil else None,
            "total_produits": total_produits,
            "produits_actifs": produits_actifs,
            "produits_rupture_stock": produits_rupture,
            "total_commandes": total_commandes,
            "commandes_en_cours": commandes_en_cours,
            "chiffre_affaires_total_cfa": chiffre_affaires_total,
            "chiffre_affaires_mois_cfa": chiffre_affaires_mois
        }

    def stock_vendeur(self, vendeur_id: UUID):
        """Liste des produits avec leur stock"""
        return self.db.query(Produit).filter(
            Produit.vendeur_identifiant == vendeur_id
        ).order_by(Produit.stock.asc(), Produit.nom).all()

    def dashboard_admin(self):
        """Dashboard pour l'admin"""
        total_utilisateurs = self.db.query(func.count(Utilisateur.identifiant)).scalar() or 0

        total_clients = self.db.query(func.count(Utilisateur.identifiant)).filter(
            Utilisateur.role == RoleUtilisateur.CLIENT
        ).scalar() or 0

        total_vendeurs = self.db.query(func.count(Utilisateur.identifiant)).filter(
            Utilisateur.role == RoleUtilisateur.VENDEUR
        ).scalar() or 0

        total_admins = self.db.query(func.count(Utilisateur.identifiant)).filter(
            Utilisateur.role == RoleUtilisateur.ADMINISTRATEUR
        ).scalar() or 0

        total_produits = self.db.query(func.count(Produit.identifiant)).scalar() or 0

        # Stats commandes
        total_commandes = 0
        chiffre_affaires_total = 0
        try:
            total_commandes = self.db.query(func.count(Commande.identifiant)).scalar() or 0
            chiffre_affaires_total = self.db.query(func.sum(CommandeArticle.total_ligne_cfa)).filter(
                CommandeArticle.statut != StatutCommande.ANNULEE
            ).scalar() or 0
        except Exception as exc:
            logger.warning("Stats commandes indisponibles (dashboard admin): %s", exc)

        return {
            "total_utilisateurs": total_utilisateurs,
            "total_clients": total_clients,
            "total_vendeurs": total_vendeurs,
            "total_admins": total_admins,
            "total_produits": total_produits,
            "total_commandes": total_commandes,
            "chiffre_affaires_total_cfa": chiffre_affaires_total
        }

    def lister_utilisateurs(self, role: str = None):
        """Lister tous les utilisateurs (admin only)"""
        query = self.db.query(Utilisateur)
        if role:
            query = query.filter(Utilisateur.role == role)
        return query.order_by(Utilisateur.date_creation.desc()).all()

    def lister_boutiques(self):
        """Lister toutes les boutiques avec leurs stats"""
        vendeurs = self.db.query(Utilisateur).filter(
            Utilisateur.role == RoleUtilisateur.VENDEUR
        ).all()

        boutiques = []
        for vendeur in vendeurs:
            profil = self.db.query(ProfilVendeur).filter(
                ProfilVendeur.utilisateur_identifiant == vendeur.identifiant
            ).first()

            total_produits = self.db.query(func.count(Produit.identifiant)).filter(
                Produit.vendeur_identifiant == vendeur.identifiant
            ).scalar() or 0

            chiffre_affaires = 0
            try:
                chiffre_affaires = self.db.query(func.sum(CommandeArticle.total_ligne_cfa)).filter(
                    and_(
                        CommandeArticle.vendeur_identifiant == vendeur.identifiant,
                        CommandeArticle.statut != StatutCommande.ANNULEE
                    )
                ).scalar() or 0
            except Exception as exc:
                logger.warning("CA indisponible pour vendeur %s: %s", vendeur.identifiant, exc)

            boutiques.append({
                "vendeur_id": vendeur.identifiant,
                "nom_complet": vendeur.nom_complet,
                "courriel": vendeur.courriel,
                "nom_entreprise": profil.nom_entreprise if profil else None,
                "statut_kyc": profil.statut_kyc.value if profil else None,
                "total_produits": total_produits,
                "chiffre_affaires_cfa": chiffre_affaires
            })

        return boutiques

    def rechercher_produits(self, terme: str, vendeur_id: UUID = None):
        """Recherche de produits par nom ou description"""
        query = self.db.query(Produit).filter(
            or_(
                Produit.nom.ilike(f"%{terme}%"),
                Produit.description.ilike(f"%{terme}%")
            )
        )

        if vendeur_id:
            query = query.filter(Produit.vendeur_identifiant == vendeur_id)

        return query.order_by(Produit.date_creation.desc()).all()
