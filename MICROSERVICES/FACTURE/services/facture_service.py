from datetime import datetime
from uuid import UUID, uuid4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur
from MICROSERVICES.COMMANDE.models.commande import Commande
from MICROSERVICES.CATALOGUE.models.produit import Produit
from MICROSERVICES.CATALOGUE.models.media import ImageProduit

from ..models.facture import Facture, FacturePaiementSuivi, StatutPaiementFacture
from ..respositories.facture_repository import FactureRepository
from ..schemas.facture import FacturePaiementUpdate


class FactureService:
	def __init__(self, db: Session):
		self.db = db
		self.repo = FactureRepository(db)

	def _generer_numero_facture(self) -> str:
		date_part = datetime.utcnow().strftime("%Y%m%d")
		rand_part = uuid4().hex[:8].upper()
		return f"FAC-{date_part}-{rand_part}"

	def generer_depuis_commande(self, commande_id: UUID, utilisateur_payload: dict):
		commande = self.db.query(Commande).filter(Commande.identifiant == commande_id).first()
		if not commande:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande introuvable")

		role = utilisateur_payload.get("role")
		utilisateur_id = utilisateur_payload.get("sub")

		if role != RoleUtilisateur.ADMINISTRATEUR.value and str(commande.client_identifiant) != str(utilisateur_id):
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

		existante = self.repo.get_by_commande(commande.identifiant)
		if existante:
			return existante

		facture = Facture(
			numero_facture=self._generer_numero_facture(),
			commande_identifiant=commande.identifiant,
			client_identifiant=commande.client_identifiant,
			montant_total_cfa=commande.total_cfa,
			statut_paiement=StatutPaiementFacture.EN_ATTENTE,
		)
		facture = self.repo.creer(facture)

		suivi = FacturePaiementSuivi(
			facture_identifiant=facture.identifiant,
			ancien_statut=None,
			nouveau_statut=StatutPaiementFacture.EN_ATTENTE,
			commentaire="Facture générée après création de commande",
			acteur_identifiant=commande.client_identifiant,
		)
		self.repo.ajouter_suivi(suivi)

		self.db.refresh(facture)
		return facture

	def lister_mes_factures(self, client_id: UUID):
		return self.repo.lister_par_client(client_id)

	def obtenir(self, facture_id: UUID):
		facture = self.repo.get_by_id(facture_id)
		if not facture:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Facture introuvable")
		return facture

	def obtenir_pour_utilisateur(self, facture_id: UUID, utilisateur_payload: dict):
		facture = self.obtenir(facture_id)
		role = utilisateur_payload.get("role")
		utilisateur_id = utilisateur_payload.get("sub")
		if role != RoleUtilisateur.ADMINISTRATEUR.value and str(facture.client_identifiant) != str(utilisateur_id):
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
		return facture

	def _format_cfa(self, montant: int) -> str:
		return f"{montant:,.0f}".replace(",", " ")

	def telecharger_contenu(self, facture_id: UUID, utilisateur_payload: dict) -> tuple[str, str]:
		facture = self.obtenir_pour_utilisateur(facture_id, utilisateur_payload)
		commande = self.db.query(Commande).filter(Commande.identifiant == facture.commande_identifiant).first()
		if not commande:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande associée introuvable")

		lignes_html = []
		for article in commande.articles:
			produit = self.db.query(Produit).filter(Produit.identifiant == article.produit_identifiant).first()
			image = self.db.query(ImageProduit).filter(ImageProduit.produit_identifiant == article.produit_identifiant).order_by(ImageProduit.position.asc()).first()

			nom_produit = produit.nom if produit else f"Produit {article.produit_identifiant}"
			description = (produit.description or "") if produit else ""
			tailles = ", ".join(produit.tailles or []) if produit and produit.tailles else "Non renseignée"
			image_url = image.url_image if image else ""

			image_cell = (
				f'<img src="{image_url}" alt="{nom_produit}" style="width:64px;height:64px;object-fit:cover;border-radius:8px;border:1px solid #eee;" />'
				if image_url else
				'<div style="width:64px;height:64px;border-radius:8px;background:#f1f3f5;border:1px solid #eee;display:flex;align-items:center;justify-content:center;color:#999;font-size:12px;">N/A</div>'
			)

			lignes_html.append(
				f"""
				<tr>
					<td style="padding:12px;vertical-align:top;">{image_cell}</td>
					<td style="padding:12px;vertical-align:top;">
						<div style="font-weight:600;">{nom_produit}</div>
						<div style="font-size:12px;color:#666;">{description}</div>
						<div style="font-size:12px;color:#444;margin-top:6px;">Taille(s): {tailles}</div>
					</td>
					<td style="padding:12px;text-align:right;white-space:nowrap;">{self._format_cfa(article.prix_unitaire_cfa)} CFA</td>
					<td style="padding:12px;text-align:center;">{article.quantite}</td>
					<td style="padding:12px;text-align:right;white-space:nowrap;font-weight:600;">{self._format_cfa(article.total_ligne_cfa)} CFA</td>
				</tr>
				"""
			)

		suivis_html = "".join([
			f"<li><strong>{s.date_evenement}</strong> — {s.nouveau_statut.value} {('- ' + s.commentaire) if s.commentaire else ''}</li>"
			for s in sorted(facture.suivis, key=lambda x: x.date_evenement)
		])

		paiement_date = facture.date_paiement.isoformat() if facture.date_paiement else "Non payé"
		mode_paiement = facture.mode_paiement or "Non renseigné"
		reference_paiement = facture.reference_paiement or "Non renseignée"

		contenu = f"""
		<!DOCTYPE html>
		<html lang="fr">
		<head>
			<meta charset="utf-8" />
			<meta name="viewport" content="width=device-width, initial-scale=1" />
			<title>{facture.numero_facture}</title>
		</head>
		<body style="font-family:Arial,Helvetica,sans-serif;background:#f7f8fb;padding:24px;color:#1f2937;">
			<div style="max-width:900px;margin:0 auto;background:#fff;border-radius:14px;box-shadow:0 8px 24px rgba(0,0,0,.08);overflow:hidden;">
				<div style="background:linear-gradient(120deg,#2b6cb0,#4c51bf);color:#fff;padding:20px 24px;display:flex;justify-content:space-between;align-items:center;">
					<div>
						<div style="font-size:24px;font-weight:700;">YOK Marketplace</div>
						<div style="opacity:.9;">Facture client</div>
					</div>
					<div style="text-align:right;">
						<div style="font-size:12px;opacity:.9;">N° FACTURE</div>
						<div style="font-size:18px;font-weight:700;">{facture.numero_facture}</div>
					</div>
				</div>

				<div style="padding:20px 24px;display:grid;grid-template-columns:1fr 1fr;gap:16px;">
					<div style="background:#f8fafc;border:1px solid #e5e7eb;border-radius:10px;padding:14px;">
						<div style="font-weight:700;margin-bottom:8px;">Détails commande</div>
						<div>Commande: {commande.identifiant}</div>
						<div>Client ID: {facture.client_identifiant}</div>
						<div>Date émission: {facture.date_emission}</div>
					</div>
					<div style="background:#f8fafc;border:1px solid #e5e7eb;border-radius:10px;padding:14px;">
						<div style="font-weight:700;margin-bottom:8px;">Paiement</div>
						<div>Statut: <strong>{facture.statut_paiement.value}</strong></div>
						<div>Mode: {mode_paiement}</div>
						<div>Référence: {reference_paiement}</div>
						<div>Date paiement: {paiement_date}</div>
					</div>
				</div>

				<div style="padding:0 24px 20px 24px;">
					<table style="width:100%;border-collapse:collapse;border:1px solid #e5e7eb;border-radius:10px;overflow:hidden;">
						<thead>
							<tr style="background:#f3f4f6;color:#374151;">
								<th style="padding:12px;text-align:left;">Image</th>
								<th style="padding:12px;text-align:left;">Produit</th>
								<th style="padding:12px;text-align:right;">Prix unitaire</th>
								<th style="padding:12px;text-align:center;">Quantité</th>
								<th style="padding:12px;text-align:right;">Total ligne</th>
							</tr>
						</thead>
						<tbody>
							{''.join(lignes_html)}
						</tbody>
					</table>
				</div>

				<div style="padding:0 24px 20px 24px;display:flex;justify-content:space-between;align-items:flex-start;gap:16px;">
					<div style="flex:1;background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:12px;">
						<div style="font-weight:700;margin-bottom:8px;">Suivi paiement</div>
						<ul style="margin:0;padding-left:18px;line-height:1.5;">{suivis_html or '<li>Pas encore d\'événement.</li>'}</ul>
					</div>
					<div style="min-width:260px;background:#ecfeff;border:1px solid #a5f3fc;border-radius:10px;padding:14px;">
						<div style="font-size:12px;color:#0f766e;">TOTAL À PAYER</div>
						<div style="font-size:28px;font-weight:800;color:#0f172a;">{self._format_cfa(facture.montant_total_cfa)} CFA</div>
					</div>
				</div>

				<div style="padding:14px 24px;background:#f8fafc;color:#64748b;font-size:12px;">
					Facture générée automatiquement par YOK. Cette facture n'affiche pas les informations vendeurs.
				</div>
			</div>
		</body>
		</html>
		"""

		nom_fichier = f"{facture.numero_facture}.html"
		return contenu, nom_fichier

	def mettre_a_jour_paiement(self, facture_id: UUID, payload: FacturePaiementUpdate, acteur_payload: dict):
		facture = self.obtenir(facture_id)
		ancien = facture.statut_paiement

		donnees = {
			"statut_paiement": payload.nouveau_statut,
			"mode_paiement": payload.mode_paiement,
			"reference_paiement": payload.reference_paiement,
			"notes": payload.notes,
		}
		if payload.nouveau_statut == StatutPaiementFacture.PAYEE and not facture.date_paiement:
			donnees["date_paiement"] = datetime.utcnow()

		facture = self.repo.maj(facture, donnees)

		suivi = FacturePaiementSuivi(
			facture_identifiant=facture.identifiant,
			ancien_statut=ancien,
			nouveau_statut=payload.nouveau_statut,
			commentaire=payload.commentaire,
			acteur_identifiant=acteur_payload.get("sub"),
		)
		self.repo.ajouter_suivi(suivi)
		self.db.refresh(facture)
		return facture

	def lister_suivis(self, facture_id: UUID, utilisateur_payload: dict):
		facture = self.obtenir_pour_utilisateur(facture_id, utilisateur_payload)
		return facture.suivis

	def historique_utilisateur_admin(self, utilisateur_id: UUID):
		commandes = self.db.query(Commande).filter(Commande.client_identifiant == utilisateur_id).order_by(Commande.date_creation.desc()).all()
		factures = self.repo.lister_par_client(utilisateur_id)
		return {
			"utilisateur_identifiant": utilisateur_id,
			"nombre_commandes": len(commandes),
			"nombre_factures": len(factures),
			"commandes": commandes,
			"factures": factures,
		}
