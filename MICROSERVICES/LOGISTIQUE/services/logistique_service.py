from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur
from MICROSERVICES.AUTHENTIFICATION.models.user import Utilisateur
from MICROSERVICES.COMMANDE.models.commande import Commande, CommandeArticle

from ..models.logistique import (
	ConsolidationEvenement,
	DossierConsolidation,
	ReceptionFournisseur,
	StatutConsolidation,
	StatutReceptionFournisseur,
)
from ..respositories.logistique_repository import LogistiqueRepository
from ..schemas.logistique import (
	ArriveeAbidjanPayload,
	AssignerAgentPayload,
	DemarrerConsolidationPayload,
	DossierConsolidationCreate,
	ExpeditionInternationalePayload,
	ExpeditionVendeurPayload,
	PreparerExpeditionPayload,
	ProblemeReceptionPayload,
	ReceptionAgentPayload,
	RemiseLivraisonLocalePayload,
)


class LogistiqueService:
	def __init__(self, db: Session):
		self.db = db
		self.repo = LogistiqueRepository(db)

	def _ajouter_evenement(self, dossier, statut_apres: StatutConsolidation, acteur_identifiant=None, commentaire=None, preuve_url=None):
		evenement = ConsolidationEvenement(
			dossier_consolidation_identifiant=dossier.identifiant,
			statut_avant=dossier.statut,
			statut_apres=statut_apres,
			acteur_identifiant=acteur_identifiant,
			commentaire=commentaire,
			preuve_url=preuve_url,
		)
		self.repo.ajouter_evenement(evenement)

	def _changer_statut_dossier(self, dossier, statut_apres: StatutConsolidation, acteur_identifiant=None, commentaire=None, preuve_url=None, extras=None):
		donnees = {"statut": statut_apres}
		if extras:
			donnees.update(extras)
		dossier = self.repo.maj_dossier(dossier, donnees)
		self._ajouter_evenement(dossier, statut_apres, acteur_identifiant, commentaire, preuve_url)
		return dossier

	def _recalculer_statut_reception(self, dossier, acteur_identifiant=None):
		receptions = dossier.receptions
		if not receptions:
			return dossier

		statuts = {r.statut for r in receptions}
		tous_recus = all(s == StatutReceptionFournisseur.RECU_PAR_AGENT for s in statuts)

		donnees = {
			"nombre_colis_fournisseurs": len(receptions),
			"tous_colis_recus": tous_recus,
		}

		if tous_recus and dossier.statut in {StatutConsolidation.EN_ATTENTE_RECEPTION, StatutConsolidation.RECEPTION_PARTIELLE}:
			dossier = self.repo.maj_dossier(dossier, donnees)
			return self._changer_statut_dossier(
				dossier,
				StatutConsolidation.TOUS_COLIS_RECUS,
				acteur_identifiant=acteur_identifiant,
				commentaire="Tous les colis fournisseurs sont reçus",
			)

		if not tous_recus and dossier.statut == StatutConsolidation.EN_ATTENTE_RECEPTION:
			dossier = self.repo.maj_dossier(dossier, donnees)
			return self._changer_statut_dossier(
				dossier,
				StatutConsolidation.RECEPTION_PARTIELLE,
				acteur_identifiant=acteur_identifiant,
				commentaire="Réception partielle des colis fournisseurs",
			)

		return self.repo.maj_dossier(dossier, donnees)

	def _valider_article_vendeur(self, dossier: DossierConsolidation, vendeur_identifiant, commande_article_identifiant):
		if commande_article_identifiant is None:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="commande_article_identifiant est obligatoire pour l'expédition vendeur",
			)

		article = (
			self.db.query(CommandeArticle)
			.filter(
				CommandeArticle.identifiant == commande_article_identifiant,
				CommandeArticle.commande_identifiant == dossier.commande_identifiant,
			)
			.first()
		)
		if not article:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Ligne de commande introuvable pour ce dossier",
			)

		if str(article.vendeur_identifiant) != str(vendeur_identifiant):
			raise HTTPException(
				status_code=status.HTTP_403_FORBIDDEN,
				detail="Un vendeur ne peut expédier que ses propres articles",
			)

	def _notifier_utilisateur(self, utilisateur_id, titre: str, message: str, lien: str | None = None, notification_type=None):
		try:
			from MICROSERVICES.NOTIFICATION.models.notification import Notification, TypeNotification

			notification = Notification(
				utilisateur_identifiant=utilisateur_id,
				type=notification_type or TypeNotification.COMMANDE_EXPEDIEE,
				titre=titre,
				message=message,
				lien=lien,
			)
			self.db.add(notification)
			self.db.flush()
		except Exception:
			pass

	def creer_ou_obtenir_dossier(self, payload: DossierConsolidationCreate, acteur_payload: dict):
		dossier = self.repo.get_dossier_par_commande(payload.commande_identifiant)
		if dossier:
			return dossier

		dossier = DossierConsolidation(
			commande_identifiant=payload.commande_identifiant,
			agent_identifiant=acteur_payload.get("sub"),
		)
		dossier = self.repo.creer_dossier(dossier)
		self._ajouter_evenement(
			dossier,
			StatutConsolidation.EN_ATTENTE_RECEPTION,
			acteur_identifiant=acteur_payload.get("sub"),
			commentaire="Dossier de consolidation créé",
		)
		return dossier

	def obtenir_dossier(self, dossier_id):
		dossier = self.repo.get_dossier(dossier_id)
		if not dossier:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dossier introuvable")
		return dossier

	def lister_dossiers(self, statut=None, agent_id=None, limite: int = 100, offset: int = 0):
		return self.repo.lister_dossiers(statut=statut, agent_id=agent_id, limite=limite, offset=offset)

	def lister_dossiers_a_risque(self, seuil_retard_heures: int = 24, limite: int = 50):
		"""Retourne les dossiers avec retards, problèmes ou colis manquants."""
		dossiers = self.repo.lister_dossiers_a_risque(seuil_retard_heures=seuil_retard_heures, limite=limite)
		resultat = []
		for dossier in dossiers:
			nombre_attendu = len(dossier.receptions) if dossier.receptions else 0
			nombre_recus = sum(1 for r in dossier.receptions if r.statut == StatutReceptionFournisseur.RECU_PAR_AGENT) if dossier.receptions else 0
			problemes = sum(1 for r in dossier.receptions if r.statut == StatutReceptionFournisseur.PROBLEME_RECEPTION) if dossier.receptions else 0
			
			raison = []
			if dossier.statut == StatutConsolidation.RECEPTION_PARTIELLE:
				raison.append(f"Reception partielle ({nombre_recus}/{nombre_attendu})")
			if problemes > 0:
				raison.append(f"Problemes recus: {problemes}")
			if nombre_attendu > 0 and nombre_recus < nombre_attendu:
				raison.append(f"Colis manquants: {nombre_attendu - nombre_recus}")
				
			resultat.append({
				"dossier": dossier,
				"nombre_colis_attendu": nombre_attendu,
				"nombre_colis_recus": nombre_recus,
				"nombre_problemes": problemes,
				"raisons_risque": raison,
			})
		return resultat

	def verifier_et_escalader_sla(self):
		"""
		Vérifie les règles SLA et escalade les alertes aux admins si dépassement.
		- Si EXPEDIE_PAR_VENDEUR > 24h sans confirmation agent → escalade
		- Si RECEPTION_PARTIELLE > 48h → escalade
		Peut être appelée par un scheduler ou endpoint .
		"""
		from datetime import datetime, timedelta, timezone
		
		maintenant = datetime.now(timezone.utc)
		escalades = []
		
		# Récupérer tous les dossiers actifs
		dossiers_actifs = self.db.query(DossierConsolidation).filter(
			DossierConsolidation.statut.in_([
				StatutConsolidation.EN_ATTENTE_RECEPTION,
				StatutConsolidation.RECEPTION_PARTIELLE,
				StatutConsolidation.TOUS_COLIS_RECUS,
				StatutConsolidation.EN_CONSOLIDATION,
				StatutConsolidation.PRET_EXPEDITION,
			])
		).all()
		
		for dossier in dossiers_actifs:
			if not dossier.receptions:
				continue
				
			# SLA 1 : Vérifier expéditions du vendeur confirmées
			receptions_expedies = [r for r in dossier.receptions if r.statut == StatutReceptionFournisseur.EXPEDIE_PAR_VENDEUR]
			for reception in receptions_expedies:
				if reception.date_expedition_vendeur:
					delai = maintenant - reception.date_expedition_vendeur
					seuil_24h = timedelta(hours=24)
					if delai > seuil_24h:
						escalades.append({
							"dossier_id": dossier.identifiant,
							"commande_id": dossier.commande_identifiant,
							"type": "EXPEDIE_NON_CONFIRMÉ",
							"delai_heures": int(delai.total_seconds() / 3600),
							"message": f"Article expédié depuis {int(delai.total_seconds() / 3600)}h, pas encore confirmé par agent",
							"severite": "MOYEN",
						})
			
			# SLA 2 : Vérifier réceptions partielles
			if dossier.statut == StatutConsolidation.RECEPTION_PARTIELLE:
				seuil_48h = timedelta(hours=48)
				delai = maintenant - dossier.date_creation
				if delai > seuil_48h:
					escalades.append({
						"dossier_id": dossier.identifiant,
						"commande_id": dossier.commande_identifiant,
						"type": "RECEPTION_PARTIELLE_LONGUE",
						"delai_heures": int(delai.total_seconds() / 3600),
						"message": f"Dossier en réception partielle depuis {int(delai.total_seconds() / 3600)}h",
						"severite": "ELEVE",
					})
		
		# Notifier les admins et créer les escalades
		if escalades:
			admins = self.db.query(Utilisateur).filter(Utilisateur.role == RoleUtilisateur.ADMINISTRATEUR).all()
			for admin in admins:
				for escalade in escalades:
					self._notifier_utilisateur(
						admin.identifiant,
						f"Alerte SLA: {escalade['type']}",
						f"Dossier {escalade['dossier_id']}: {escalade['message']} (Sévérité: {escalade['severite']})",
						lien=f"/admin/logistique/dossiers/{escalade['dossier_id']}",
					)
		
		return {
			"nombre_escalades": len(escalades),
			"escalades": escalades,
		}

	def assigner_agent(self, dossier_id, payload: AssignerAgentPayload, acteur_payload: dict):
		dossier = self.obtenir_dossier(dossier_id)
		return self.repo.maj_dossier(
			dossier,
			{
				"agent_identifiant": payload.agent_identifiant,
				"commentaire": payload.commentaire or dossier.commentaire,
			},
		)

	def signaler_expedition_vendeur(self, dossier_id, payload: ExpeditionVendeurPayload, acteur_payload: dict):
		dossier = self.obtenir_dossier(dossier_id)
		acteur_id = acteur_payload.get("sub")
		role = acteur_payload.get("role")

		vendeur_identifiant = payload.vendeur_identifiant
		if role == RoleUtilisateur.VENDEUR.value:
			if not acteur_id:
				raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identité vendeur introuvable")
			if str(vendeur_identifiant) != str(acteur_id):
				raise HTTPException(
					status_code=status.HTTP_403_FORBIDDEN,
					detail="Un vendeur ne peut déclarer que ses propres expéditions",
				)

		self._valider_article_vendeur(dossier, vendeur_identifiant, payload.commande_article_identifiant)

		reception = self.repo.get_reception_par_dossier_vendeur_article(
			dossier.identifiant,
			vendeur_identifiant,
			payload.commande_article_identifiant,
		)
		if reception:
			reception = self.repo.maj_reception(
				reception,
				{
					"statut": StatutReceptionFournisseur.EXPEDIE_PAR_VENDEUR,
					"tracking_fournisseur": payload.tracking_fournisseur,
					"transporteur_fournisseur": payload.transporteur_fournisseur,
					"preuve_expedition_url": payload.preuve_expedition_url,
					"commentaire": payload.commentaire,
					"date_expedition_vendeur": datetime.now(timezone.utc),
				},
			)
		else:
			reception = ReceptionFournisseur(
				dossier_consolidation_identifiant=dossier.identifiant,
				vendeur_identifiant=vendeur_identifiant,
				commande_article_identifiant=payload.commande_article_identifiant,
				statut=StatutReceptionFournisseur.EXPEDIE_PAR_VENDEUR,
				tracking_fournisseur=payload.tracking_fournisseur,
				transporteur_fournisseur=payload.transporteur_fournisseur,
				preuve_expedition_url=payload.preuve_expedition_url,
				commentaire=payload.commentaire,
				date_expedition_vendeur=datetime.now(timezone.utc),
			)
			reception = self.repo.creer_reception(reception)

		dossier = self._recalculer_statut_reception(dossier, acteur_identifiant=acteur_id)
		
		# Déclencher la libération de l'avance (30%) au wallet vendeur
		try:
			from MICROSERVICES.PAIEMENT_VENDEURS.services.wallet_service import WalletService
			wallet_service = WalletService(self.db)
			wallet_service.traiter_evenement_logistique(
				dossier.commande_identifiant,
				action="EXPEDITION_VENDEUR",
				reception_id=reception.identifiant,
			)
		except Exception as e:
			# Log warning mais ne bloque pas l'expédition
			pass
		
		self.db.refresh(dossier)
		return dossier

	def confirmer_reception_agent(self, dossier_id, reception_id, payload: ReceptionAgentPayload, acteur_payload: dict):
		dossier = self.obtenir_dossier(dossier_id)
		reception = self.repo.get_reception(reception_id)
		if not reception or str(reception.dossier_consolidation_identifiant) != str(dossier.identifiant):
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Réception introuvable")

		self.repo.maj_reception(
			reception,
			{
				"statut": StatutReceptionFournisseur.RECU_PAR_AGENT,
				"preuve_reception_url": payload.preuve_reception_url,
				"commentaire": payload.commentaire,
				"date_reception_agent": datetime.now(timezone.utc),
			},
		)

		dossier = self._recalculer_statut_reception(dossier, acteur_identifiant=acteur_payload.get("sub"))
		
		# Déclencher la libération du solde (70%) au wallet vendeur après vérification agent
		try:
			from MICROSERVICES.PAIEMENT_VENDEURS.services.wallet_service import WalletService
			wallet_service = WalletService(self.db)
			wallet_service.traiter_evenement_logistique(
				dossier.commande_identifiant,
				action="VERIFICATION_AGENT",
			)
		except Exception as e:
			# Log warning mais ne bloque pas la vérification
			pass
		
		self.db.refresh(dossier)
		return dossier

	def signaler_probleme_reception(self, dossier_id, reception_id, payload: ProblemeReceptionPayload, acteur_payload: dict):
		dossier = self.obtenir_dossier(dossier_id)
		reception = self.repo.get_reception(reception_id)
		if not reception or str(reception.dossier_consolidation_identifiant) != str(dossier.identifiant):
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Réception introuvable")

		self.repo.maj_reception(
			reception,
			{
				"statut": StatutReceptionFournisseur.PROBLEME_RECEPTION,
				"preuve_reception_url": payload.preuve_reception_url,
				"commentaire": payload.commentaire,
			},
		)

		if dossier.statut in {StatutConsolidation.EN_ATTENTE_RECEPTION, StatutConsolidation.RECEPTION_PARTIELLE}:
			dossier = self._changer_statut_dossier(
				dossier,
				StatutConsolidation.RECEPTION_PARTIELLE,
				acteur_identifiant=acteur_payload.get("sub"),
				commentaire="Problème de réception signalé",
				preuve_url=payload.preuve_reception_url,
			)

		admins = self.db.query(Utilisateur).filter(Utilisateur.role == RoleUtilisateur.ADMINISTRATEUR).all()
		for admin in admins:
			self._notifier_utilisateur(
				admin.identifiant,
				"Alerte logistique: probleme reception",
				f"Probleme reception sur dossier {dossier.identifiant}: {payload.commentaire}",
				lien=f"/admin/logistique/dossiers/{dossier.identifiant}",
			)
		self.db.refresh(dossier)
		return dossier

	def demarrer_consolidation(self, dossier_id, payload: DemarrerConsolidationPayload, acteur_payload: dict):
		dossier = self.obtenir_dossier(dossier_id)
		if dossier.statut not in {StatutConsolidation.TOUS_COLIS_RECUS, StatutConsolidation.RECEPTION_PARTIELLE}:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transition invalide vers EN_CONSOLIDATION")
		return self._changer_statut_dossier(
			dossier,
			StatutConsolidation.EN_CONSOLIDATION,
			acteur_identifiant=acteur_payload.get("sub"),
			commentaire=payload.commentaire or "Consolidation démarrée",
		)

	def preparer_expedition(self, dossier_id, payload: PreparerExpeditionPayload, acteur_payload: dict):
		dossier = self.obtenir_dossier(dossier_id)
		if dossier.statut != StatutConsolidation.EN_CONSOLIDATION:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transition invalide vers PRET_EXPEDITION")

		extras = {
			"poids_total_kg": payload.poids_total_kg,
			"longueur_cm": payload.longueur_cm,
			"largeur_cm": payload.largeur_cm,
			"hauteur_cm": payload.hauteur_cm,
			"preuve_emballage_url": payload.preuve_emballage_url,
			"commentaire": payload.commentaire or dossier.commentaire,
		}
		return self._changer_statut_dossier(
			dossier,
			StatutConsolidation.PRET_EXPEDITION,
			acteur_identifiant=acteur_payload.get("sub"),
			commentaire=payload.commentaire or "Colis consolidé et prêt à expédier",
			preuve_url=payload.preuve_emballage_url,
			extras=extras,
		)

	def expedier_vers_abidjan(self, dossier_id, payload: ExpeditionInternationalePayload, acteur_payload: dict):
		dossier = self.obtenir_dossier(dossier_id)
		if dossier.statut != StatutConsolidation.PRET_EXPEDITION:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transition invalide vers EXPEDIE")

		if not dossier.poids_total_kg or not dossier.longueur_cm or not dossier.largeur_cm or not dossier.hauteur_cm:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Poids et dimensions finales obligatoires avant l'expédition",
			)
		if not payload.transporteur_international:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Transporteur international obligatoire",
			)
		if not payload.tracking_interne:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Tracking international obligatoire",
			)

		extras = {
			"tracking_interne": payload.tracking_interne,
			"transporteur_international": payload.transporteur_international,
			"numero_vol_ou_cargo": payload.numero_vol_ou_cargo,
			"date_depart_chine": datetime.now(timezone.utc),
			"commentaire": payload.commentaire or dossier.commentaire,
		}
		dossier = self._changer_statut_dossier(
			dossier,
			StatutConsolidation.EXPEDIE,
			acteur_identifiant=acteur_payload.get("sub"),
			commentaire=payload.commentaire or "Expédition internationale lancée",
			extras=extras,
		)

		return dossier

	def confirmer_arrivee_abidjan(self, dossier_id, payload: ArriveeAbidjanPayload, acteur_payload: dict):
		dossier = self.obtenir_dossier(dossier_id)
		if dossier.statut != StatutConsolidation.EXPEDIE:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transition invalide vers ARRIVE_ABIDJAN")

		dossier = self._changer_statut_dossier(
			dossier,
			StatutConsolidation.ARRIVE_ABIDJAN,
			acteur_identifiant=acteur_payload.get("sub"),
			commentaire=payload.commentaire or "Colis arrivé à Abidjan",
			extras={"date_arrivee_abidjan": datetime.now(timezone.utc)},
		)

		commande = self.db.query(Commande).filter(Commande.identifiant == dossier.commande_identifiant).first()
		if commande:
			from MICROSERVICES.NOTIFICATION.models.notification import TypeNotification

			self._notifier_utilisateur(
				commande.client_identifiant,
				"Colis arrive a Abidjan",
				f"Votre commande {commande.identifiant} est arrivee a Abidjan.",
				lien=f"/commandes/{commande.identifiant}",
				notification_type=TypeNotification.COLIS_ARRIVE_ABIDJAN,
			)

		return dossier

	def remettre_a_livraison_locale(self, dossier_id, payload: RemiseLivraisonLocalePayload, acteur_payload: dict):
		dossier = self.obtenir_dossier(dossier_id)
		if dossier.statut != StatutConsolidation.ARRIVE_ABIDJAN:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transition invalide vers REMIS_LIVRAISON_LOCALE")

		dossier = self._changer_statut_dossier(
			dossier,
			StatutConsolidation.REMIS_LIVRAISON_LOCALE,
			acteur_identifiant=acteur_payload.get("sub"),
			commentaire=payload.commentaire or "Dossier remis au service de livraison locale",
		)

		# Crée automatiquement la livraison locale (si absente) dès la remise.
		from MICROSERVICES.LIVRAISON.schemas.livraison import LivraisonCreate
		from MICROSERVICES.LIVRAISON.services.livraison_service import LivraisonService

		livraison_service = LivraisonService(self.db)
		livraison_service.creer(
			LivraisonCreate(
				commande_identifiant=dossier.commande_identifiant,
				dossier_consolidation_identifiant=dossier.identifiant,
				commentaire="Créée automatiquement depuis le dossier de consolidation",
			),
			acteur_payload,
		)
		return dossier
