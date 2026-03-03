from sqlalchemy.orm import Session

from ..models.image import ImageAvis


class ImageAvisRepository:
	def __init__(self, db: Session):
		self.db = db

	def lister_par_avis(self, avis_id):
		return self.db.query(ImageAvis).filter(ImageAvis.avis_identifiant == avis_id).all()

	def ajouter(self, image: ImageAvis):
		self.db.add(image)
		self.db.flush()
		return image
