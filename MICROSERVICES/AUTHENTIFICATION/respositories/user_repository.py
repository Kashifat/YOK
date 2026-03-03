from __future__ import annotations

from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from ..models.user import RoleUtilisateur, Utilisateur


class UserRepository:
    """Accès aux données utilisateur (CRUD minimal + opérations auth)."""

    def __init__(self, db: Session):
        self.db = db

    # ---------- LECTURE ----------
    def get_by_email(self, courriel: str) -> Optional[Utilisateur]:
        return (
            self.db.query(Utilisateur)
            .filter(Utilisateur.courriel == courriel)
            .first()
        )

    def get_by_id(self, identifiant: UUID) -> Optional[Utilisateur]:
        return (
            self.db.query(Utilisateur)
            .filter(Utilisateur.identifiant == identifiant)
            .first()
        )

    def existe_courriel(self, courriel: str) -> bool:
        return (
            self.db.query(Utilisateur.identifiant)
            .filter(Utilisateur.courriel == courriel)
            .first()
            is not None
        )

    def lister(self, limite: int = 50, offset: int = 0) -> List[Utilisateur]:
        return (
            self.db.query(Utilisateur)
            .order_by(Utilisateur.date_creation.desc())
            .offset(offset)
            .limit(limite)
            .all()
        )

    def get_by_oauth(self, provider: str, oauth_id: str) -> Optional[Utilisateur]:
        """Récupère un utilisateur par provider OAuth et ID."""
        return (
            self.db.query(Utilisateur)
            .filter(
                Utilisateur.oauth_provider == provider,
                Utilisateur.oauth_id == oauth_id
            )
            .first()
        )

    # ---------- CRÉATION ----------
    def creer_utilisateur(
        self,
        *,
        courriel: str,
        nom_complet: str,
        mot_de_passe_hash: str | None = None,
        role: RoleUtilisateur,
        telephone: Optional[str] = None,
        oauth_provider: Optional[str] = None,
        oauth_id: Optional[str] = None,
        photo_url: Optional[str] = None,
        est_actif: bool = True,
    ) -> Utilisateur:
        utilisateur = Utilisateur(
            courriel=courriel,
            nom_complet=nom_complet,
            mot_de_passe_hash=mot_de_passe_hash,
            role=role,
            telephone=telephone,
            oauth_provider=oauth_provider,
            oauth_id=oauth_id,
            photo_url=photo_url,
            est_actif=est_actif,
        )

        self.db.add(utilisateur)
        self.db.flush()
        self.db.refresh(utilisateur)
        return utilisateur

    # ---------- MISE À JOUR ----------
    def mettre_a_jour_mot_de_passe(self, identifiant: UUID, nouveau_hash: str) -> bool:
        utilisateur = self.get_by_id(identifiant)
        if not utilisateur:
            return False

        utilisateur.mot_de_passe_hash = nouveau_hash
        self.db.flush()
        return True

    def activer_desactiver(self, identifiant: UUID, est_actif: bool) -> bool:
        utilisateur = self.get_by_id(identifiant)
        if not utilisateur:
            return False

        utilisateur.est_actif = est_actif
        self.db.flush()
        return True

    # ---------- SUPPRESSION (optionnel) ----------
    def supprimer(self, identifiant: UUID) -> bool:
        utilisateur = self.get_by_id(identifiant)
        if not utilisateur:
            return False

        self.db.delete(utilisateur)
        self.db.flush()
        return True
