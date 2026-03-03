import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from shared.db.base import Base


class StatutModerationPost(str, enum.Enum):
	ACTIF = "ACTIF"
	MASQUE = "MASQUE"
	SUPPRIME = "SUPPRIME"


class StatutModerationCommentaire(str, enum.Enum):
	ACTIF = "ACTIF"
	MASQUE = "MASQUE"
	SUPPRIME = "SUPPRIME"


class ReseauPost(Base):
	__tablename__ = "reseau_posts"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	auteur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant", ondelete="CASCADE"), nullable=False)
	contenu = Column(Text, nullable=False)
	statut_moderation = Column(Enum(StatutModerationPost, name="statut_moderation_post", create_type=False), nullable=False, server_default=text("'ACTIF'"))
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))

	images = relationship("ReseauPostImage", backref="post", lazy="joined", cascade="all, delete-orphan")
	tags = relationship("ReseauPostTagProduit", backref="post", lazy="joined", cascade="all, delete-orphan")
	commentaires = relationship("ReseauCommentaire", backref="post", lazy="selectin", cascade="all, delete-orphan")
	likes = relationship("ReseauLike", backref="post", lazy="selectin", cascade="all, delete-orphan")
	partages = relationship("ReseauPartage", backref="post", lazy="selectin", cascade="all, delete-orphan")


class ReseauPostImage(Base):
	__tablename__ = "reseau_post_images"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	post_identifiant = Column(UUID(as_uuid=True), ForeignKey("reseau_posts.identifiant", ondelete="CASCADE"), nullable=False)
	url_image = Column(Text, nullable=False)
	position = Column(Integer, default=0)
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))


class ReseauPostTagProduit(Base):
	__tablename__ = "reseau_post_tags_produits"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	post_identifiant = Column(UUID(as_uuid=True), ForeignKey("reseau_posts.identifiant", ondelete="CASCADE"), nullable=False)
	produit_identifiant = Column(UUID(as_uuid=True), ForeignKey("produits.identifiant"), nullable=False)
	boutique_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant"), nullable=False)

	__table_args__ = (
		UniqueConstraint("post_identifiant", "produit_identifiant", name="uq_reseau_post_produit"),
	)


class ReseauCommentaire(Base):
	__tablename__ = "reseau_commentaires"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	post_identifiant = Column(UUID(as_uuid=True), ForeignKey("reseau_posts.identifiant", ondelete="CASCADE"), nullable=False)
	auteur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant", ondelete="CASCADE"), nullable=False)
	contenu = Column(Text, nullable=False)
	statut_moderation = Column(Enum(StatutModerationCommentaire, name="statut_moderation_commentaire", create_type=False), nullable=False, server_default=text("'ACTIF'"))
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))

	likes = relationship("ReseauCommentaireLike", backref="commentaire", lazy="selectin", cascade="all, delete-orphan")


class ReseauLike(Base):
	__tablename__ = "reseau_likes"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	post_identifiant = Column(UUID(as_uuid=True), ForeignKey("reseau_posts.identifiant", ondelete="CASCADE"), nullable=False)
	utilisateur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant", ondelete="CASCADE"), nullable=False)
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))

	__table_args__ = (
		UniqueConstraint("post_identifiant", "utilisateur_identifiant", name="uq_reseau_like_post_user"),
	)


class ReseauPartage(Base):
	__tablename__ = "reseau_partages"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	post_identifiant = Column(UUID(as_uuid=True), ForeignKey("reseau_posts.identifiant", ondelete="CASCADE"), nullable=False)
	utilisateur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant", ondelete="CASCADE"), nullable=False)
	plateforme = Column(Text)
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))


class ReseauCommentaireLike(Base):
	__tablename__ = "reseau_commentaire_likes"

	identifiant = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
	commentaire_identifiant = Column(UUID(as_uuid=True), ForeignKey("reseau_commentaires.identifiant", ondelete="CASCADE"), nullable=False)
	utilisateur_identifiant = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.identifiant", ondelete="CASCADE"), nullable=False)
	date_creation = Column(DateTime(timezone=True), server_default=text("NOW()"))

	__table_args__ = (
		UniqueConstraint("commentaire_identifiant", "utilisateur_identifiant", name="uq_reseau_like_comment_user"),
	)
