import enum

from sqlalchemy import Boolean, Column, DateTime, Text, text, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM, UUID

from shared.db.base import Base


class RoleUtilisateur(str, enum.Enum):
    CLIENT = "CLIENT"
    VENDEUR = "VENDEUR"
    ADMINISTRATEUR = "ADMINISTRATEUR"


class StatutKYC(str, enum.Enum):
    EN_ATTENTE = "EN_ATTENTE"
    VALIDEE = "VALIDEE"
    REJETEE = "REJETEE"
    EN_REVISION = "EN_REVISION"


class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    role = Column(ENUM(RoleUtilisateur, name="role_utilisateur", create_type=False), nullable=False)
    nom_complet = Column(Text, nullable=False)
    telephone = Column(Text, unique=True)
    courriel = Column(Text, unique=True, nullable=False, index=True)
    mot_de_passe_hash = Column(Text)
    oauth_provider = Column(Text)
    oauth_id = Column(Text, unique=True)
    photo_url = Column(Text)
    est_actif = Column(Boolean, default=True)
    date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))


class ProfilVendeur(Base):
    __tablename__ = "profils_vendeurs"

    utilisateur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant", ondelete="CASCADE"), primary_key=True)
    nom_entreprise = Column(Text, nullable=False)
    nom_contact = Column(Text)
    pays = Column(Text, default="Chine")
    statut_kyc = Column(ENUM(StatutKYC, name="statut_kyc", create_type=False), default=StatutKYC.EN_ATTENTE)
    date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))
