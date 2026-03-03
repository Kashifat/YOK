from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import logging

from ..models.commande import Commande, CommandeArticle, StatutCommande
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
			"statut": commande.statut,
			"total_cfa": commande.total_cfa,
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
			remarques=payload.remarques,
			statut=StatutCommande.EN_ATTENTE_PAIEMENT,
			total_cfa=0
		)
		commande = self.repo.creer(commande)

		# Créer les articles de commande (avec traçabilité vendeur)
		from MICROSERVICES.CATALOGUE.models.produit import Produit
		total = 0

		for article_panier in panier.articles:
			produit = self.db.query(Produit).filter(Produit.identifiant == article_panier.produit_identifiant).first()
			if not produit:
				continue

			# Vérifier le stock
			if produit.stock < article_panier.quantite:
				raise HTTPException(
					status_code=status.HTTP_400_BAD_REQUEST,
					detail=f"Stock insuffisant pour {produit.nom}"
				)

			# Créer l'article de commande
			prix_unitaire = produit.prix_cfa
			quantite = article_panier.quantite
			total_ligne = prix_unitaire * quantite

			article_commande = CommandeArticle(
				commande_identifiant=commande.identifiant,
				produit_identifiant=produit.identifiant,
				vendeur_identifiant=produit.vendeur_identifiant,  # Traçabilité vendeur !
				prix_unitaire_cfa=prix_unitaire,
				quantite=quantite,
				total_ligne_cfa=total_ligne,
				statut=StatutCommande.EN_ATTENTE_PAIEMENT
			)
			self.repo.ajouter_article(article_commande)
			total += total_ligne

			# Décrémenter le stock
			produit.stock -= quantite

		# Mettre à jour le total de la commande
		commande.total_cfa = total
		self.db.flush()

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
		for article in commande.articles:
			produit = self.db.query(Produit).filter(Produit.identifiant == article.produit_identifiant).first()
			if produit:
				produit.stock += article.quantite

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
