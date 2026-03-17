from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from ..models.logistique import StatutConsolidation
from ..schemas.logistique import (
	ActionRead,
	ArriveeAbidjanPayload,
	AssignerAgentPayload,
	DemarrerConsolidationPayload,
	DossierConsolidationCreate,
	DossierConsolidationRead,
	DossierArisqueRead,
	ExpeditionInternationalePayload,
	ExpeditionVendeurPayload,
	PreparerExpeditionPayload,
	ProblemeReceptionPayload,
	ReceptionAgentPayload,
	RemiseLivraisonLocalePayload,
)
from ..services.autorisation_service import AutorisationService
from ..services.logistique_service import LogistiqueService


router = APIRouter()
auth_admin = AutorisationService([RoleUtilisateur.ADMINISTRATEUR])
auth_logistique = AutorisationService([RoleUtilisateur.AGENT_LOGISTIQUE, RoleUtilisateur.ADMINISTRATEUR])
auth_vendeur = AutorisationService([RoleUtilisateur.VENDEUR, RoleUtilisateur.ADMINISTRATEUR])


@router.post("/dossiers", response_model=DossierConsolidationRead, status_code=status.HTTP_201_CREATED)
def creer_dossier(payload: DossierConsolidationCreate, utilisateur=Depends(auth_admin), db: Session = Depends(obtenir_session)):
	service = LogistiqueService(db)
	return service.creer_ou_obtenir_dossier(payload, utilisateur)


@router.get("/dossiers", response_model=list[DossierConsolidationRead])
def lister_dossiers(
	statut: StatutConsolidation | None = Query(default=None),
	agent_identifiant: UUID | None = Query(default=None),
	limite: int = Query(default=100, ge=1, le=500),
	offset: int = Query(default=0, ge=0),
	utilisateur=Depends(auth_logistique),
	db: Session = Depends(obtenir_session),
):
	service = LogistiqueService(db)
	return service.lister_dossiers(statut=statut, agent_id=agent_identifiant, limite=limite, offset=offset)


@router.get("/dossiers/a-risque", response_model=list[DossierArisqueRead])
def dossiers_a_risque(
	seuil_retard_heures: int = Query(default=24, ge=1, le=168),
	limite: int = Query(default=50, ge=1, le=500),
	utilisateur=Depends(auth_logistique),
	db: Session = Depends(obtenir_session),
):
	"""Liste les dossiers à risque: retards, problèmes, colis manquants (vue agent opérationnelle)."""
	service = LogistiqueService(db)
	return service.lister_dossiers_a_risque(seuil_retard_heures=seuil_retard_heures, limite=limite)


@router.get("/dossiers/{dossier_id}", response_model=DossierConsolidationRead)
def obtenir_dossier(dossier_id: UUID, utilisateur=Depends(auth_logistique), db: Session = Depends(obtenir_session)):
	service = LogistiqueService(db)
	return service.obtenir_dossier(dossier_id)


@router.patch("/dossiers/{dossier_id}/assigner-agent", response_model=DossierConsolidationRead)
def assigner_agent(dossier_id: UUID, payload: AssignerAgentPayload, utilisateur=Depends(auth_admin), db: Session = Depends(obtenir_session)):
	service = LogistiqueService(db)
	return service.assigner_agent(dossier_id, payload, utilisateur)


@router.patch("/dossiers/{dossier_id}/expedition-vendeur", response_model=DossierConsolidationRead)
def signaler_expedition_vendeur(
	dossier_id: UUID,
	payload: ExpeditionVendeurPayload,
	utilisateur=Depends(auth_vendeur),
	db: Session = Depends(obtenir_session),
):
	service = LogistiqueService(db)
	return service.signaler_expedition_vendeur(dossier_id, payload, utilisateur)


@router.patch("/dossiers/{dossier_id}/receptions/{reception_id}/confirmer", response_model=DossierConsolidationRead)
def confirmer_reception_agent(
	dossier_id: UUID,
	reception_id: UUID,
	payload: ReceptionAgentPayload,
	utilisateur=Depends(auth_logistique),
	db: Session = Depends(obtenir_session),
):
	service = LogistiqueService(db)
	return service.confirmer_reception_agent(dossier_id, reception_id, payload, utilisateur)


@router.patch("/dossiers/{dossier_id}/receptions/{reception_id}/probleme", response_model=DossierConsolidationRead)
def signaler_probleme_reception(
	dossier_id: UUID,
	reception_id: UUID,
	payload: ProblemeReceptionPayload,
	utilisateur=Depends(auth_logistique),
	db: Session = Depends(obtenir_session),
):
	service = LogistiqueService(db)
	return service.signaler_probleme_reception(dossier_id, reception_id, payload, utilisateur)


@router.patch("/dossiers/{dossier_id}/demarrer-consolidation", response_model=DossierConsolidationRead)
def demarrer_consolidation(
	dossier_id: UUID,
	payload: DemarrerConsolidationPayload,
	utilisateur=Depends(auth_logistique),
	db: Session = Depends(obtenir_session),
):
	service = LogistiqueService(db)
	return service.demarrer_consolidation(dossier_id, payload, utilisateur)


@router.patch("/dossiers/{dossier_id}/pret-expedition", response_model=DossierConsolidationRead)
def preparer_expedition(
	dossier_id: UUID,
	payload: PreparerExpeditionPayload,
	utilisateur=Depends(auth_logistique),
	db: Session = Depends(obtenir_session),
):
	service = LogistiqueService(db)
	return service.preparer_expedition(dossier_id, payload, utilisateur)


@router.patch("/dossiers/{dossier_id}/expedier-abidjan", response_model=DossierConsolidationRead)
def expedier_vers_abidjan(
	dossier_id: UUID,
	payload: ExpeditionInternationalePayload,
	utilisateur=Depends(auth_logistique),
	db: Session = Depends(obtenir_session),
):
	service = LogistiqueService(db)
	return service.expedier_vers_abidjan(dossier_id, payload, utilisateur)


@router.patch("/dossiers/{dossier_id}/arrivee-abidjan", response_model=DossierConsolidationRead)
def confirmer_arrivee_abidjan(
	dossier_id: UUID,
	payload: ArriveeAbidjanPayload,
	utilisateur=Depends(auth_logistique),
	db: Session = Depends(obtenir_session),
):
	service = LogistiqueService(db)
	return service.confirmer_arrivee_abidjan(dossier_id, payload, utilisateur)


@router.patch("/dossiers/{dossier_id}/remise-livraison-locale", response_model=DossierConsolidationRead)
def remettre_livraison_locale(
	dossier_id: UUID,
	payload: RemiseLivraisonLocalePayload,
	utilisateur=Depends(auth_logistique),
	db: Session = Depends(obtenir_session),
):
	service = LogistiqueService(db)
	return service.remettre_a_livraison_locale(dossier_id, payload, utilisateur)


@router.post("/sla/verifier-escalades", response_model=ActionRead)
def verifier_escalades_sla(utilisateur=Depends(auth_admin), db: Session = Depends(obtenir_session)):
	"""Vérifie les SLA en vigueur et escalade les dossiers à risque (admin seulement)."""
	service = LogistiqueService(db)
	resultat = service.verifier_et_escalader_sla()
	return {
		"message": f"{resultat['nombre_escalades']} escalade(s) détectée(s) et notifiée(s)"
	}


@router.get("/health/ping", response_model=ActionRead)
def ping():
	return {"message": "service logistique actif"}
