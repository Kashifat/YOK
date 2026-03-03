from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.avis import Avis
from ..models.image import ImageAvis
from ..respositories.avis_repository import AvisRepository
from ..respositories.image_repository import ImageAvisRepository
from ..schemas.avis import AvisCreate, AvisUpdate, ImageAvisCreate


class AvisService:
	def __init__(self, db: Session):
		self.db = db
		self.repo = AvisRepository(db)
		self.image_repo = ImageAvisRepository(db)

	def lister_par_produit(self, produit_id):
		"""Liste publique des avis d'un produit."""
		return self.repo.lister_par_produit(produit_id)

	def obtenir(self, identifiant):
		avis = self.repo.get_by_id(identifiant)
		if not avis:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avis introuvable")
		return avis

	def creer(self, client_id, payload: AvisCreate):
		"""Client crée un avis pour un produit."""
		# Vérifier que le produit existe
		from MICROSERVICES.CATALOGUE.models.produit import Produit
		produit = self.db.query(Produit).filter(
			Produit.identifiant == payload.produit_identifiant,
			Produit.est_actif == True
		).first()
		if not produit:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Produit introuvable"
			)

		# Vérifier si avis existe déjà
		existant = self.repo.get_avis_client_produit(client_id, payload.produit_identifiant)
		if existant:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Vous avez déjà laissé un avis pour ce produit"
			)

		avis = Avis(
			produit_identifiant=payload.produit_identifiant,
			client_identifiant=client_id,
			note=payload.note,
			titre=payload.titre,
			commentaire=payload.commentaire,
		)
		return self.repo.creer(avis)

	def maj(self, identifiant, client_id, est_admin: bool, payload: AvisUpdate):
		"""Client modifie SON avis."""
		avis = self.obtenir(identifiant)

		# Seul le propriétaire ou admin peut modifier
		if not est_admin and str(avis.client_identifiant) != str(client_id):
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

		donnees = payload.model_dump(exclude_unset=True)
		return self.repo.maj(avis, donnees)

	def supprimer(self, identifiant, client_id, est_admin: bool):
		"""Client supprime SON avis, admin peut supprimer n'importe lequel (modération)."""
		avis = self.obtenir(identifiant)

		if not est_admin and str(avis.client_identifiant) != str(client_id):
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

		self.repo.supprimer(avis)
		return {"message": "Avis supprimé"}

	def ajouter_image(self, avis_id, client_id, est_admin: bool, payload: ImageAvisCreate):
		"""Client ajoute une image à SON avis."""
		avis = self.obtenir(avis_id)

		if not est_admin and str(avis.client_identifiant) != str(client_id):
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

		image = ImageAvis(
			avis_identifiant=avis_id,
			url_image=payload.url_image,
			position=payload.position,
		)
		return self.image_repo.ajouter(image)
