from sqlalchemy.orm import Session

from ..models.facture import Facture, FacturePaiementSuivi


class FactureRepository:
	def __init__(self, db: Session):
		self.db = db

	def get_by_id(self, identifiant):
		return self.db.query(Facture).filter(Facture.identifiant == identifiant).first()

	def get_by_commande(self, commande_id):
		return self.db.query(Facture).filter(Facture.commande_identifiant == commande_id).first()

	def lister_par_client(self, client_id):
		return self.db.query(Facture).filter(Facture.client_identifiant == client_id).order_by(Facture.date_emission.desc()).all()

	def creer(self, facture: Facture):
		self.db.add(facture)
		self.db.flush()
		self.db.refresh(facture)
		return facture

	def ajouter_suivi(self, suivi: FacturePaiementSuivi):
		self.db.add(suivi)
		self.db.flush()
		return suivi

	def maj(self, facture: Facture, donnees: dict):
		for cle, valeur in donnees.items():
			setattr(facture, cle, valeur)
		self.db.flush()
		self.db.refresh(facture)
		return facture
