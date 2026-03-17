from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime, timedelta, timezone

from ..models.logistique import ConsolidationEvenement, DossierConsolidation, ReceptionFournisseur, StatutReceptionFournisseur


class LogistiqueRepository:
	def __init__(self, db: Session):
		self.db = db

	def get_dossier(self, dossier_id):
		return self.db.query(DossierConsolidation).filter(DossierConsolidation.identifiant == dossier_id).first()

	def get_dossier_par_commande(self, commande_id):
		return self.db.query(DossierConsolidation).filter(DossierConsolidation.commande_identifiant == commande_id).first()

	def lister_dossiers(self, statut=None, agent_id=None, limite: int = 100, offset: int = 0):
		requete = self.db.query(DossierConsolidation)
		if statut is not None:
			requete = requete.filter(DossierConsolidation.statut == statut)
		if agent_id is not None:
			requete = requete.filter(DossierConsolidation.agent_identifiant == agent_id)
		return requete.order_by(DossierConsolidation.date_creation.desc()).limit(limite).offset(offset).all()

	def lister_dossiers_a_risque(self, seuil_retard_heures: int = 24, limite: int = 50):
		"""
		Liste les dossiers avec problèmes ou retards :
		- RECEPTION_PARTIELLE depuis > seuil_retard_heures
		- Contenant des PROBLEME_RECEPTION
		- Colis manquants (nombre attendu != nombre reçus)
		"""
		from sqlalchemy import case, cast, Integer
		
		# Subquery pour compter les statuts par dossier
		subquery = self.db.query(
			ReceptionFournisseur.dossier_consolidation_identifiant,
			func.count(ReceptionFournisseur.identifiant).label("nombre_problemes"),
		).filter(
			ReceptionFournisseur.statut == StatutReceptionFournisseur.PROBLEME_RECEPTION
		).group_by(
			ReceptionFournisseur.dossier_consolidation_identifiant
		).subquery()

		seuil_datetime = datetime.now(timezone.utc) - timedelta(hours=seuil_retard_heures)
		
		query = self.db.query(DossierConsolidation)
		# À risque si : RECEPTION_PARTIELLE ancien,  ou problèmes, ou colis manquants
		query = query.outerjoin(subquery, DossierConsolidation.identifiant == subquery.c.dossier_consolidation_identifiant)
		query = query.filter(
			(DossierConsolidation.statut == "RECEPTION_PARTIELLE") |  # Retard suspicion
			(subquery.c.nombre_problemes.isnot(None))  # Au moins 1 problème
		)
		
		return (
			query
			.order_by(DossierConsolidation.date_creation.asc())
			.limit(limite)
			.all()
		)

	def creer_dossier(self, dossier: DossierConsolidation):
		self.db.add(dossier)
		self.db.flush()
		self.db.refresh(dossier)
		return dossier

	def maj_dossier(self, dossier: DossierConsolidation, donnees: dict):
		for cle, valeur in donnees.items():
			setattr(dossier, cle, valeur)
		self.db.flush()
		self.db.refresh(dossier)
		return dossier

	def get_reception(self, reception_id):
		return self.db.query(ReceptionFournisseur).filter(ReceptionFournisseur.identifiant == reception_id).first()

	def get_reception_par_dossier_vendeur_article(self, dossier_id, vendeur_id, commande_article_id):
		requete = self.db.query(ReceptionFournisseur).filter(
			ReceptionFournisseur.dossier_consolidation_identifiant == dossier_id,
			ReceptionFournisseur.vendeur_identifiant == vendeur_id,
		)
		if commande_article_id is None:
			requete = requete.filter(ReceptionFournisseur.commande_article_identifiant.is_(None))
		else:
			requete = requete.filter(ReceptionFournisseur.commande_article_identifiant == commande_article_id)
		return requete.first()

	def creer_reception(self, reception: ReceptionFournisseur):
		self.db.add(reception)
		self.db.flush()
		self.db.refresh(reception)
		return reception

	def maj_reception(self, reception: ReceptionFournisseur, donnees: dict):
		for cle, valeur in donnees.items():
			setattr(reception, cle, valeur)
		self.db.flush()
		self.db.refresh(reception)
		return reception

	def ajouter_evenement(self, evenement: ConsolidationEvenement):
		self.db.add(evenement)
		self.db.flush()
		self.db.refresh(evenement)
		return evenement
