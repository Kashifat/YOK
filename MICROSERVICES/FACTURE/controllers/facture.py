from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from ..schemas.facture import FactureRead, FacturePaiementUpdate, FacturePaiementSuiviRead, HistoriqueUtilisateurAdminRead
from ..services.autorisation_service import AutorisationService
from ..services.facture_service import FactureService


router = APIRouter()
auth_client = AutorisationService([RoleUtilisateur.CLIENT, RoleUtilisateur.ADMINISTRATEUR])
auth_admin = AutorisationService([RoleUtilisateur.ADMINISTRATEUR])


@router.post("/commande/{commande_id}", response_model=FactureRead, status_code=status.HTTP_201_CREATED)
def generer_facture_commande(commande_id: UUID, utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Génère la facture d'une commande (ou retourne l'existante)."""
	service = FactureService(db)
	return service.generer_depuis_commande(commande_id, utilisateur)


@router.get("/mes-factures", response_model=list[FactureRead])
def lister_mes_factures(utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Liste les factures du client connecté."""
	service = FactureService(db)
	return service.lister_mes_factures(utilisateur.get("sub"))


@router.get("/{facture_id}", response_model=FactureRead)
def obtenir_facture(facture_id: UUID, utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Détail d'une facture."""
	service = FactureService(db)
	return service.obtenir_pour_utilisateur(facture_id, utilisateur)


@router.get("/{facture_id}/telecharger")
def telecharger_facture(facture_id: UUID, utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Télécharge une facture au format HTML esthétique."""
	service = FactureService(db)
	contenu, nom_fichier = service.telecharger_contenu(facture_id, utilisateur)
	return Response(
		content=contenu,
		media_type="text/html",
		headers={"Content-Disposition": f'attachment; filename="{nom_fichier}"'},
	)


@router.patch("/{facture_id}/paiement", response_model=FactureRead)
def maj_statut_paiement(
	facture_id: UUID,
	payload: FacturePaiementUpdate,
	utilisateur=Depends(auth_admin),
	db: Session = Depends(obtenir_session),
):
	"""Mise à jour du statut de paiement (admin/webhook interne)."""
	service = FactureService(db)
	return service.mettre_a_jour_paiement(facture_id, payload, utilisateur)


@router.get("/{facture_id}/suivi-paiement", response_model=list[FacturePaiementSuiviRead])
def suivi_paiement(facture_id: UUID, utilisateur=Depends(auth_client), db: Session = Depends(obtenir_session)):
	"""Historique de suivi paiement d'une facture."""
	service = FactureService(db)
	return service.lister_suivis(facture_id, utilisateur)


@router.get("/admin/utilisateurs/{utilisateur_id}/historique", response_model=HistoriqueUtilisateurAdminRead)
def historique_utilisateur(utilisateur_id: UUID, utilisateur=Depends(auth_admin), db: Session = Depends(obtenir_session)):
	"""Admin: liste commandes + factures d'un utilisateur."""
	service = FactureService(db)
	return service.historique_utilisateur_admin(utilisateur_id)
