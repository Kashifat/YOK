from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import logging
from datetime import datetime, timedelta, timezone

from ..models.commande import Commande, CommandeArticle, StatutCommande
from ..config import settings
from ..respositories.commande_repository import CommandeRepository
from ..respositories.panier_repository import PanierRepository
from ..schemas.commande import CommandeCreate, CommandeUpdate, CommandeArticleUpdateStatut


class CommandeService:
	def __init__(self, db: Session):
		self.db = db
		self.repo = CommandeRepository(db)
		self.panier_repo = PanierRepository(db)
		self.logger = logging.getLogger(__name__)

	def _declencher_wallet_vendeur(self, commande_id, statut: StatutCommande, source: str):
		try:
			from MICROSERVICES.PAIEMENT_VENDEURS.services.wallet_service import WalletService
			wallet_service = WalletService(self.db)
			wallet_service.traiter_evenement_commande(commande_id, statut, source=source)
		except Exception as exc:
			self.logger.warning("Synchronisation wallet vendeurs échouée pour commande %s (%s): %s", commande_id, statut.value, exc)

	def _vers_reponse_creation(self, commande, paiement_infos: dict | None = None):
		reponse = {
			"identifiant": commande.identifiant,
			"client_identifiant": commande.client_identifiant,
			"adresse_identifiant": commande.adresse_identifiant,
			"code_promo_identifiant": commande.code_promo_identifiant,
			"statut": commande.statut,
			"total_cfa": commande.total_cfa,
			"frais_livraison_cfa": commande.frais_livraison_cfa,
			"montant_remise_cfa": commande.montant_remise_cfa,
			"remarques": commande.remarques,
			"date_creation": commande.date_creation,
			"articles": commande.articles,
			"paiement_identifiant": None,
			"payment_url": None,
			"provider_transaction_id": None,
			"payment_mode": None,
			"payment_message": None,
		}
		if paiement_infos:
			reponse.update(paiement_infos)
		return reponse

	def _notifier_vendeurs_creation_commande(self, commande: Commande, details_articles: list[dict]):
		from collections import defaultdict

		from MICROSERVICES.NOTIFICATION.models.notification import Notification, TypeNotification

		deadline = datetime.now(timezone.utc) + timedelta(hours=settings.delai_expedition_vendeur_heures)
		par_vendeur = defaultdict(list)
		for detail in details_articles:
			par_vendeur[detail["vendeur_identifiant"]].append(detail)

		for vendeur_id, items in par_vendeur.items():
			lignes = []
			for item in items:
				variante = ""
				if item.get("taille") or item.get("couleur"):
					variante = f" ({item.get('taille') or '-'} / {item.get('couleur') or '-'})"
				lignes.append(f"- {item['produit_nom']} x{item['quantite']}{variante}")

			message = (
				"Nouvelle commande a preparer.\n"
				f"Commande: {commande.identifiant}\n"
				f"Adresse agent logistique: {settings.logistique_adresse_agent}\n"
				f"Delai expedition: {deadline.isoformat()}\n"
				"Articles:\n"
				+ "\n".join(lignes)
			)

			notification = Notification(
				utilisateur_identifiant=vendeur_id,
				type=TypeNotification.COMMANDE_PAYEE,
				titre="Nouvelle commande vendeur",
				message=message,
				lien=f"/vendeur/commandes/{commande.identifiant}",
			)
			self.db.add(notification)
		self.db.flush()

	def statut_ux_client(self, commande_id, client_id):
		commande = self.obtenir_commande_client(commande_id, client_id)

		statut_consolidation = None
		statut_livraison = None
		try:
			from MICROSERVICES.LOGISTIQUE.services.logistique_service import LogistiqueService

			logistique_service = LogistiqueService(self.db)
			dossier = logistique_service.repo.get_dossier_par_commande(commande.identifiant)
			if dossier:
				statut_consolidation = dossier.statut.value
		except Exception:
			dossier = None

		try:
			from MICROSERVICES.LIVRAISON.respositories.livraison_repository import LivraisonRepository

			livraison = LivraisonRepository(self.db).get_by_commande(commande.identifiant)
			if livraison:
				statut_livraison = livraison.statut.value
		except Exception:
			pass

		if commande.statut == StatutCommande.EN_ATTENTE_PAIEMENT:
			return {
				"commande_identifiant": commande.identifiant,
				"statut_ux": "commande confirmee",
				"statut_commande": commande.statut,
				"statut_consolidation": statut_consolidation,
				"statut_livraison": statut_livraison,
				"message": "Votre commande est confirmee et en attente de paiement.",
			}

		if commande.statut in {StatutCommande.ANNULEE, StatutCommande.REMBOURSEE}:
			return {
				"commande_identifiant": commande.identifiant,
				"statut_ux": "annulee",
				"statut_commande": commande.statut,
				"statut_consolidation": statut_consolidation,
				"statut_livraison": statut_livraison,
				"message": "Cette commande est annulee ou remboursee.",
			}

		if statut_livraison == "LIVREE_CLIENT" or commande.statut == StatutCommande.LIVREE:
			return {
				"commande_identifiant": commande.identifiant,
				"statut_ux": "livree",
				"statut_commande": commande.statut,
				"statut_consolidation": statut_consolidation,
				"statut_livraison": statut_livraison,
				"message": "Votre commande a ete livree.",
			}

		if statut_livraison in {"CREEE", "ASSIGNEE", "EN_TRANSIT", "ARRIVEE_ENTREPOT_ABIDJAN"}:
			return {
				"commande_identifiant": commande.identifiant,
				"statut_ux": "en livraison",
				"statut_commande": commande.statut,
				"statut_consolidation": statut_consolidation,
				"statut_livraison": statut_livraison,
				"message": "Votre commande est en livraison locale.",
			}

		if statut_consolidation == "ARRIVE_ABIDJAN":
			return {
				"commande_identifiant": commande.identifiant,
				"statut_ux": "arrivee a abidjan",
				"statut_commande": commande.statut,
				"statut_consolidation": statut_consolidation,
				"statut_livraison": statut_livraison,
				"message": "Votre colis est arrive a Abidjan.",
			}

		if statut_consolidation == "EXPEDIE" or commande.statut == StatutCommande.EXPEDIEE:
			return {
				"commande_identifiant": commande.identifiant,
				"statut_ux": "expediee",
				"statut_commande": commande.statut,
				"statut_consolidation": statut_consolidation,
				"statut_livraison": statut_livraison,
				"message": "Votre colis est en transport international.",
			}

		if statut_consolidation in {"EN_CONSOLIDATION", "PRET_EXPEDITION"}:
			return {
				"commande_identifiant": commande.identifiant,
				"statut_ux": "en consolidation",
				"statut_commande": commande.statut,
				"statut_consolidation": statut_consolidation,
				"statut_livraison": statut_livraison,
				"message": "Votre commande est en consolidation logistique.",
			}

		return {
			"commande_identifiant": commande.identifiant,
			"statut_ux": "en preparation",
			"statut_commande": commande.statut,
			"statut_consolidation": statut_consolidation,
			"statut_livraison": statut_livraison,
			"message": "Votre commande est en preparation.",
		}

	def creer_depuis_panier(self, utilisateur_payload: dict, payload: CommandeCreate):
		"""Crée une commande à partir du panier."""
		utilisateur_id = utilisateur_payload.get("sub")

		# Récupérer le panier
		panier = self.panier_repo.get_by_utilisateur(utilisateur_id)
		if not panier or not panier.articles:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Panier vide"
			)

		# Vérifier l'adresse
		from MICROSERVICES.AUTHENTIFICATION.models.user import Utilisateur
		# On suppose que l'adresse existe et appartient à l'utilisateur
		# (on pourrait ajouter une vérification ici)

		# Créer la commande
		commande = Commande(
			client_identifiant=utilisateur_id,
			adresse_identifiant=payload.adresse_identifiant,
			code_promo_identifiant=payload.code_promo_identifiant,
			frais_livraison_cfa=payload.frais_livraison_cfa,
			montant_remise_cfa=payload.montant_remise_cfa,
			remarques=payload.remarques,
			statut=StatutCommande.EN_ATTENTE_PAIEMENT,
			total_cfa=0
		)
		commande = self.repo.creer(commande)

		# Créer les articles de commande (avec traçabilité vendeur)
		from MICROSERVICES.CATALOGUE.models.produit import Produit, VariantProduit
		total_articles = 0
		details_articles_notifications = []

		for article_panier in panier.articles:
			produit = self.db.query(Produit).filter(Produit.identifiant == article_panier.produit_identifiant).first()
			if not produit:
				continue

			variante = None
			if article_panier.variante_identifiant:
				variante = self.db.query(VariantProduit).filter(
					VariantProduit.identifiant == article_panier.variante_identifiant,
					VariantProduit.produit_identifiant == produit.identifiant,
					VariantProduit.est_actif.is_(True),
				).first()
				if not variante:
					raise HTTPException(
						status_code=status.HTTP_400_BAD_REQUEST,
						detail=f"Variante introuvable pour {produit.nom}",
					)

			# Vérifier le stock
			stock_disponible = produit.stock
			if variante:
				stock_disponible = min(produit.stock, variante.stock)

			if stock_disponible < article_panier.quantite:
				raise HTTPException(
					status_code=status.HTTP_400_BAD_REQUEST,
					detail=f"Stock insuffisant pour {produit.nom}"
				)

			# Créer l'article de commande
			prix_unitaire = produit.prix_cfa + (variante.prix_supplementaire_cfa if variante else 0)
			quantite = article_panier.quantite
			total_ligne = prix_unitaire * quantite

			article_commande = CommandeArticle(
				commande_identifiant=commande.identifiant,
				produit_identifiant=produit.identifiant,
				vendeur_identifiant=produit.vendeur_identifiant,  # Traçabilité vendeur !
				variante_identifiant=article_panier.variante_identifiant,
				prix_unitaire_cfa=prix_unitaire,
				quantite=quantite,
				taille_selectionnee=variante.taille if variante else None,
				couleur_selectionnee=variante.couleur if variante else None,
				total_ligne_cfa=total_ligne,
				statut=StatutCommande.EN_ATTENTE_PAIEMENT
			)
			self.repo.ajouter_article(article_commande)
			total_articles += total_ligne
			details_articles_notifications.append(
				{
					"vendeur_identifiant": produit.vendeur_identifiant,
					"produit_nom": produit.nom,
					"quantite": quantite,
					"taille": variante.taille if variante else None,
					"couleur": variante.couleur if variante else None,
				}
			)

			# Décrémenter le stock
			produit.stock -= quantite
			if variante:
				variante.stock -= quantite

		# Mettre à jour le total de la commande
		commande.total_cfa = max(0, total_articles + commande.frais_livraison_cfa - commande.montant_remise_cfa)
		self.db.flush()

		# Créer automatiquement le dossier de consolidation logistique
		from MICROSERVICES.LOGISTIQUE.schemas.logistique import DossierConsolidationCreate
		from MICROSERVICES.LOGISTIQUE.services.logistique_service import LogistiqueService
		logistique_service = LogistiqueService(self.db)
		logistique_service.creer_ou_obtenir_dossier(
			DossierConsolidationCreate(commande_identifiant=commande.identifiant),
			{"sub": None},
		)

		# Notification vendeur ciblée (produits, quantités, variante, adresse agent, délai)
		try:
			self._notifier_vendeurs_creation_commande(commande, details_articles_notifications)
		except Exception as exc:
			self.logger.warning("Notifications vendeurs non envoyees pour commande %s: %s", commande.identifiant, exc)

		# Vider le panier
		self.panier_repo.vider_panier(panier)

		# Générer automatiquement la facture associée à la commande
		from MICROSERVICES.FACTURE.services.facture_service import FactureService
		facture_service = FactureService(self.db)
		facture_service.generer_depuis_commande(
			commande.identifiant,
			{"role": "ADMINISTRATEUR", "sub": str(utilisateur_id)},
		)

		paiement_infos = {
			"payment_mode": "NON_INITIALISE",
			"payment_message": "Paiement non initialisé",
		}
		try:
			from MICROSERVICES.PAIEMENT_CLIENTS.schemas.paiement import PaiementInitialisationCreate
			from MICROSERVICES.PAIEMENT_CLIENTS.services.paiement_service import PaiementService

			paiement_service = PaiementService(self.db)
			resultat_paiement = paiement_service.initialiser(
				utilisateur_payload,
				PaiementInitialisationCreate(
					commande_identifiant=commande.identifiant,
					canal="ALL",
					description=f"Paiement commande {commande.identifiant}",
				),
			)

			paiement = resultat_paiement.get("paiement")
			paiement_infos = {
				"paiement_identifiant": paiement.identifiant if paiement else None,
				"payment_url": resultat_paiement.get("payment_url"),
				"provider_transaction_id": resultat_paiement.get("provider_transaction_id"),
				"payment_mode": resultat_paiement.get("mode"),
				"payment_message": "Paiement initialisé",
			}
		except HTTPException as exc:
			paiement_infos = {
				"payment_mode": "ERREUR",
				"payment_message": f"Paiement non initialisé: {exc.detail}",
			}
		except Exception:
			paiement_infos = {
				"payment_mode": "ERREUR",
				"payment_message": "Paiement non initialisé: erreur interne",
			}

		self.db.refresh(commande)
		return self._vers_reponse_creation(commande, paiement_infos)

	def lister_mes_commandes(self, utilisateur_id):
		"""Liste toutes les commandes d'un client."""
		return self.repo.lister_par_client(utilisateur_id)

	def obtenir(self, identifiant):
		"""Récupère une commande par ID."""
		commande = self.repo.get_by_id(identifiant)
		if not commande:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Commande introuvable"
			)
		return commande

	def obtenir_commande_client(self, identifiant, client_id):
		"""Récupère une commande si elle appartient au client."""
		commande = self.obtenir(identifiant)
		if str(commande.client_identifiant) != str(client_id):
			raise HTTPException(
				status_code=status.HTTP_403_FORBIDDEN,
				detail="Accès refusé"
			)
		return commande

	def annuler_commande(self, identifiant, client_id):
		"""Annule une commande (seulement si EN_ATTENTE_PAIEMENT)."""
		commande = self.obtenir_commande_client(identifiant, client_id)

		if commande.statut != StatutCommande.EN_ATTENTE_PAIEMENT:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Commande déjà payée, impossible d'annuler"
			)

		# Remettre le stock
		from MICROSERVICES.CATALOGUE.models.produit import Produit
		from MICROSERVICES.CATALOGUE.models.produit import VariantProduit
		for article in commande.articles:
			produit = self.db.query(Produit).filter(Produit.identifiant == article.produit_identifiant).first()
			if produit:
				produit.stock += article.quantite
			if article.variante_identifiant:
				variante = self.db.query(VariantProduit).filter(VariantProduit.identifiant == article.variante_identifiant).first()
				if variante:
					variante.stock += article.quantite

		commande = self.repo.maj(commande, {"statut": StatutCommande.ANNULEE})
		self._declencher_wallet_vendeur(commande.identifiant, StatutCommande.ANNULEE, source="COMMANDE_ANNULATION_CLIENT")
		return commande

	# ========== VENDEUR ==========

	def lister_mes_ventes(self, vendeur_id):
		"""Liste toutes les commandes contenant des produits du vendeur."""
		return self.repo.lister_par_vendeur(vendeur_id)

	def maj_statut_article(self, article_id, vendeur_id, payload: CommandeArticleUpdateStatut):
		"""Vendeur met à jour le statut d'un article."""
		article = self.repo.get_article_by_id(article_id)
		if not article:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Article introuvable"
			)

		if str(article.vendeur_identifiant) != str(vendeur_id):
			raise HTTPException(
				status_code=status.HTTP_403_FORBIDDEN,
				detail="Cet article n'appartient pas à vos produits"
			)

		return self.repo.maj_article_statut(article, payload.statut)

	# ========== ADMIN ==========

	def lister_toutes(self, limite: int = 100, offset: int = 0):
		"""Admin liste toutes les commandes."""
		return self.repo.lister_toutes(limite, offset)

	def maj_commande(self, identifiant, payload: CommandeUpdate):
		"""Admin met à jour une commande."""
		commande = self.obtenir(identifiant)
		donnees = payload.model_dump(exclude_unset=True)
		commande = self.repo.maj(commande, donnees)

		if commande.statut in {
			StatutCommande.EXPEDIEE,
			StatutCommande.LIVREE,
			StatutCommande.ANNULEE,
			StatutCommande.REMBOURSEE,
		}:
			self._declencher_wallet_vendeur(commande.identifiant, commande.statut, source="COMMANDE_MAJ_ADMIN")

		return commande

	def expeditions_a_faire(self, vendeur_id):
		"""Liste les articles que le vendeur doit expédier (vue opérationnelle)."""
		from MICROSERVICES.CATALOGUE.models.produit import Produit
		
		resultats = self.repo.lister_expeditions_a_faire_vendeur(vendeur_id)
		expeditions = []
		
		for article, commande, dossier, reception in resultats:
			produit = self.db.query(Produit).filter(Produit.identifiant == article.produit_identifiant).first()
			produit_nom = produit.nom if produit else "N/A"
			
			est_expedie = reception and reception.statut == "EXPEDIE_PAR_VENDEUR"
			tracking = reception.tracking_fournisseur if reception and est_expedie else None
			statut_reception = reception.statut if reception else "EN_ATTENTE_EXPEDITION_VENDEUR"
			
			expeditions.append({
				"article_identifiant": article.identifiant,
				"commande_identifiant": commande.identifiant,
				"dossier_consolidation_identifiant": dossier.identifiant,
				"produit_nom": produit_nom,
				"taille_selectionnee": article.taille_selectionnee,
				"couleur_selectionnee": article.couleur_selectionnee,
				"quantite": article.quantite,
				"prix_unitaire_cfa": article.prix_unitaire_cfa,
				"total_ligne_cfa": article.total_ligne_cfa,
				"statut_reception": statut_reception,
				"date_commande": commande.date_creation,
				"est_expedie": est_expedie,
				"tracking": tracking,
			})
		
		return sorted(expeditions, key=lambda x: x["date_commande"])
