from sqlalchemy.orm import Session

from ..models.media import ImageProduit, VideoProduit


class MediaRepository:
	def __init__(self, db: Session):
		self.db = db

	def ajouter_image(self, image: ImageProduit):
		self.db.add(image)
		self.db.flush()
		return image

	def ajouter_video(self, video: VideoProduit):
		self.db.add(video)
		self.db.flush()
		return video

	def lister_images(self, produit_id):
		return self.db.query(ImageProduit).filter(ImageProduit.produit_identifiant == produit_id).all()

	def lister_videos(self, produit_id):
		return self.db.query(VideoProduit).filter(VideoProduit.produit_identifiant == produit_id).all()