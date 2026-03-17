"""Tests du microservice CATALOGUE."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from uuid import uuid4

from MICROSERVICES.CATALOGUE.main import creer_application
from MICROSERVICES.AUTHENTIFICATION.main import creer_application as creer_app_auth
from MICROSERVICES.AUTHENTIFICATION.services.auth_service import AuthService
from MICROSERVICES.AUTHENTIFICATION.schemas.user import UserCreate
from MICROSERVICES.AUTHENTIFICATION.models.user import RoleUtilisateur

from shared.db.conn import SessionLocale


@pytest.fixture(scope="module", autouse=True)
def verifier_db_disponible():
	"""Skip les tests catalogue si la DB locale n'est pas disponible."""
	session = SessionLocale()
	try:
		session.execute(text("SELECT 1"))
	except OperationalError:
		pytest.skip("DB locale indisponible pour tests catalogue")
	finally:
		session.close()


# ============ FIXTURES ============

@pytest.fixture
def db():
	"""Session BD pour les tests."""
	session = SessionLocale()
	yield session
	session.rollback()
	session.close()


@pytest.fixture(autouse=True)
def nettoyer_donnees_catalogue():
	"""Réinitialise les données catalogue pour éviter les fuites entre tests."""
	session = SessionLocale()
	try:
		session.execute(text("TRUNCATE TABLE categories, produits, variantes_produits, images_produits, videos_produits RESTART IDENTITY CASCADE"))
		session.commit()
		yield
	finally:
		session.rollback()
		session.close()


@pytest.fixture
def app_catalogue():
	"""App catalogue de test."""
	return creer_application()


@pytest.fixture
def client_catalogue(app_catalogue):
	"""Client test catalogue."""
	return TestClient(app_catalogue)


@pytest.fixture
def app_auth():
	"""App auth de test."""
	return creer_app_auth()


@pytest.fixture
def client_auth(app_auth):
	"""Client test auth."""
	return TestClient(app_auth)


@pytest.fixture
def utilisateur_client(db, client_auth):
	"""Crée un utilisateur CLIENT et retourne ses tokens."""
	payload = {
		"nom_complet": "Jean Dupont",
		"courriel": f"client_{uuid4().hex[:8]}@test.com",
		"mot_de_passe": "Test123!",
		"telephone": f"555000{uuid4().hex[:3]}"
	}
	
	response = client_auth.post("/auth/inscription", json=payload)
	assert response.status_code == 201
	user_id = response.json()["identifiant"]
	
	# Connexion
	response = client_auth.post(
		"/auth/connexion",
		json={
			"courriel": payload["courriel"],
			"mot_de_passe": payload["mot_de_passe"]
		}
	)
	assert response.status_code == 200
	data = response.json()
	
	return {
		"token": data["access_token"],
		"utilisateur_id": user_id,
		"email": payload["courriel"]
	}


@pytest.fixture
def utilisateur_vendeur(db, client_auth):
	"""Crée un utilisateur VENDEUR et retourne ses tokens."""
	# Créer compte CLIENT d'abord
	payload = {
		"nom_complet": "Ahmed Vendeur",
		"courriel": f"vendeur_{uuid4().hex[:8]}@test.com",
		"mot_de_passe": "Test123!",
		"telephone": f"555100{uuid4().hex[:3]}"
	}
	
	response = client_auth.post("/auth/inscription", json=payload)
	assert response.status_code == 201
	user_id = response.json()["identifiant"]
	
	# Changer rôle en VENDEUR directement en BD (hack pour tests)
	from MICROSERVICES.AUTHENTIFICATION.models.user import Utilisateur
	utilisateur = db.query(Utilisateur).filter(Utilisateur.identifiant == user_id).first()
	utilisateur.role = RoleUtilisateur.VENDEUR
	db.commit()
	
	# Connexion
	response = client_auth.post(
		"/auth/connexion",
		json={
			"courriel": payload["courriel"],
			"mot_de_passe": payload["mot_de_passe"]
		}
	)
	assert response.status_code == 200
	data = response.json()
	
	return {
		"token": data["access_token"],
		"utilisateur_id": user_id,
		"email": payload["courriel"]
	}


@pytest.fixture
def utilisateur_admin(db, client_auth):
	"""Crée un utilisateur ADMIN et retourne ses tokens."""
	payload = {
		"nom_complet": "Admin Master",
		"courriel": f"admin_{uuid4().hex[:8]}@test.com",
		"mot_de_passe": "Test123!",
		"telephone": f"555200{uuid4().hex[:3]}"
	}
	
	response = client_auth.post("/auth/inscription", json=payload)
	assert response.status_code == 201
	user_id = response.json()["identifiant"]
	
	# Changer rôle en ADMIN
	from MICROSERVICES.AUTHENTIFICATION.models.user import Utilisateur
	utilisateur = db.query(Utilisateur).filter(Utilisateur.identifiant == user_id).first()
	utilisateur.role = RoleUtilisateur.ADMINISTRATEUR
	db.commit()
	
	# Connexion
	response = client_auth.post(
		"/auth/connexion",
		json={
			"courriel": payload["courriel"],
			"mot_de_passe": payload["mot_de_passe"]
		}
	)
	assert response.status_code == 200
	data = response.json()
	
	return {
		"token": data["access_token"],
		"utilisateur_id": user_id,
		"email": payload["courriel"]
	}


# ============ TESTS ROUTES PUBLIQUES ============

class TestCataloguePublique:
	"""Tests des routes publiques (sans auth)."""

	def test_lister_categories_vide(self, client_catalogue):
		"""GET /catalogue/public/categories - Aucune catégorie."""
		response = client_catalogue.get("/catalogue/public/categories")
		assert response.status_code == 200
		assert response.json() == []

	def test_lister_produits_vide(self, client_catalogue):
		"""GET /catalogue/public/produits - Aucun produit."""
		response = client_catalogue.get("/catalogue/public/produits")
		assert response.status_code == 200
		assert response.json() == []

	def test_obtenir_categorie_inexistante(self, client_catalogue):
		"""GET /catalogue/public/categories/{id} - Catégorie inexistante."""
		response = client_catalogue.get(f"/catalogue/public/categories/{uuid4()}")
		assert response.status_code == 404

	def test_obtenir_produit_inexistant(self, client_catalogue):
		"""GET /catalogue/public/produits/{id} - Produit inexistant."""
		response = client_catalogue.get(f"/catalogue/public/produits/{uuid4()}")
		assert response.status_code == 404


# ============ TESTS ROUTES ADMIN ============

class TestCatalogueAdmin:
	"""Tests des routes admin (catégories)."""

	def test_admin_creer_categorie(self, client_catalogue, utilisateur_admin):
		"""POST /catalogue/admin/categories - Admin crée catégorie."""
		headers = {"Authorization": f"Bearer {utilisateur_admin['token']}"}
		payload = {
			"nom": "Électronique",
			"description": "Tous les appareils électroniques"
		}
		
		response = client_catalogue.post(
			"/catalogue/admin/categories",
			json=payload,
			headers=headers
		)
		
		assert response.status_code == 201
		data = response.json()
		assert data["nom"] == "Électronique"
		assert data["est_actif"] is True
		assert "identifiant" in data

	def test_client_cannot_creer_categorie(self, client_catalogue, utilisateur_client):
		"""POST /catalogue/admin/categories - Client ne peut pas créer."""
		headers = {"Authorization": f"Bearer {utilisateur_client['token']}"}
		payload = {"nom": "Test"}
		
		response = client_catalogue.post(
			"/catalogue/admin/categories",
			json=payload,
			headers=headers
		)
		
		assert response.status_code == 403  # Forbidden

	def test_sans_token_cannot_creer_categorie(self, client_catalogue):
		"""POST /catalogue/admin/categories - Sans token = 401."""
		payload = {"nom": "Test"}
		
		response = client_catalogue.post("/catalogue/admin/categories", json=payload)
		
		assert response.status_code == 401

	def test_admin_lister_categories(self, client_catalogue, utilisateur_admin):
		"""GET /catalogue/admin/categories - Admin voit toutes."""
		headers = {"Authorization": f"Bearer {utilisateur_admin['token']}"}
		
		# Créer 2 catégories
		for i in range(2):
			client_catalogue.post(
				"/catalogue/admin/categories",
				json={"nom": f"Cat {i}"},
				headers=headers
			)
		
		response = client_catalogue.get(
			"/catalogue/admin/categories",
			headers=headers
		)
		
		assert response.status_code == 200
		assert len(response.json()) == 2

	def test_admin_maj_categorie(self, client_catalogue, utilisateur_admin):
		"""PATCH /catalogue/admin/categories/{id} - Modifier."""
		headers = {"Authorization": f"Bearer {utilisateur_admin['token']}"}
		
		# Créer
		response = client_catalogue.post(
			"/catalogue/admin/categories",
			json={"nom": "Informatique"},
			headers=headers
		)
		cat_id = response.json()["identifiant"]
		
		# Modifier
		response = client_catalogue.patch(
			f"/catalogue/admin/categories/{cat_id}",
			json={"nom": "Informatique & Gadgets", "description": "Updated"},
			headers=headers
		)
		
		assert response.status_code == 200
		data = response.json()
		assert data["nom"] == "Informatique & Gadgets"
		assert data["description"] == "Updated"

	def test_admin_desactiver_categorie(self, client_catalogue, utilisateur_admin):
		"""DELETE /catalogue/admin/categories/{id} - Désactiver."""
		headers = {"Authorization": f"Bearer {utilisateur_admin['token']}"}
		
		# Créer
		response = client_catalogue.post(
			"/catalogue/admin/categories",
			json={"nom": "À supprimer"},
			headers=headers
		)
		cat_id = response.json()["identifiant"]
		
		# Désactiver
		response = client_catalogue.delete(
			f"/catalogue/admin/categories/{cat_id}",
			headers=headers
		)
		
		assert response.status_code == 200


# ============ TESTS ROUTES VENDEUR ============

class TestCatalogueVendeur:
	"""Tests des routes vendeur (produits)."""

	def test_vendeur_creer_produit(self, client_catalogue, utilisateur_vendeur, utilisateur_admin):
		"""POST /catalogue/vendeur/produits - Vendeur crée produit."""
		# D'abord créer une catégorie (admin)
		headers_admin = {"Authorization": f"Bearer {utilisateur_admin['token']}"}
		response = client_catalogue.post(
			"/catalogue/admin/categories",
			json={"nom": "Téléphones"},
			headers=headers_admin
		)
		cat_id = response.json()["identifiant"]
		
		# Vendeur crée produit
		headers_vendeur = {"Authorization": f"Bearer {utilisateur_vendeur['token']}"}
		payload = {
			"categorie_identifiant": str(cat_id),
			"nom": "iPhone 15",
			"description": "Téléphone Apple dernier modèle",
			"prix_cfa": 850000,
			"stock": 50
		}
		
		response = client_catalogue.post(
			"/catalogue/vendeur/produits",
			json=payload,
			headers=headers_vendeur
		)
		
		assert response.status_code == 201
		data = response.json()
		assert data["nom"] == "iPhone 15"
		assert data["prix_cfa"] == 850000
		assert data["stock"] == 50
		assert "identifiant" in data

	def test_vendeur_lister_ses_produits(self, client_catalogue, utilisateur_vendeur, utilisateur_admin):
		"""GET /catalogue/vendeur/produits - Lister mes produits."""
		# Créer catégorie
		headers_admin = {"Authorization": f"Bearer {utilisateur_admin['token']}"}
		response = client_catalogue.post(
			"/catalogue/admin/categories",
			json={"nom": "Laptop"},
			headers=headers_admin
		)
		cat_id = response.json()["identifiant"]
		
		# Créer 2 produits
		headers_vendeur = {"Authorization": f"Bearer {utilisateur_vendeur['token']}"}
		for i in range(2):
			client_catalogue.post(
				"/catalogue/vendeur/produits",
				json={
					"categorie_identifiant": str(cat_id),
					"nom": f"Produit {i}",
					"prix_cfa": 100000 + i*10000,
					"stock": 10
				},
				headers=headers_vendeur
			)
		
		response = client_catalogue.get(
			"/catalogue/vendeur/produits",
			headers=headers_vendeur
		)
		
		assert response.status_code == 200
		assert len(response.json()) == 2

	def test_client_cannot_creer_produit(self, client_catalogue, utilisateur_client):
		"""POST /catalogue/vendeur/produits - Client ne peut pas créer."""
		headers = {"Authorization": f"Bearer {utilisateur_client['token']}"}
		payload = {
			"categorie_identifiant": str(uuid4()),
			"nom": "Test",
			"prix_cfa": 10000,
			"stock": 5
		}
		
		response = client_catalogue.post(
			"/catalogue/vendeur/produits",
			json=payload,
			headers=headers
		)
		
		assert response.status_code == 403  # Forbidden


# ============ TESTS HEALTH CHECK ============

class TestHealth:
	"""Tests de santé."""

	def test_health_public(self, client_catalogue):
		"""GET /health - Vérifier app est alive."""
		response = client_catalogue.get("/health")
		assert response.status_code == 200
		assert response.json() == {"status": "ok"}


# ============ EXÉCUTION ============

if __name__ == "__main__":
	pytest.main([__file__, "-v", "--tb=short"])
