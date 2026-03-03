import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from shared.db.base import Base
from shared.db.conn import obtenir_session
from MICROSERVICES.AVIS.main import app as avis_app
from MICROSERVICES.AUTHENTIFICATION.main import app as auth_app


# Configuration de la base de test
TEST_DATABASE_URL = "postgresql+psycopg://postgres:123456@localhost:5432/yok_bd"
engine_test = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestSessionLocale = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="module", autouse=True)
def verifier_db_disponible():
	"""Skip les tests avis si la DB locale de test n'est pas disponible."""
	session = TestSessionLocale()
	try:
		session.execute(text("SELECT 1"))
	except OperationalError:
		pytest.skip("DB locale indisponible pour tests avis")
	finally:
		session.close()


@pytest.fixture(scope="function")
def db():
	"""Crée une session de base de données pour chaque test."""
	Base.metadata.create_all(bind=engine_test)
	session = TestSessionLocale()
	try:
		yield session
		session.commit()
	except Exception:
		session.rollback()
		raise
	finally:
		session.close()


@pytest.fixture(scope="function")
def app_avis(db):
	"""Application AVIS avec override de la session."""
	def override_session():
		try:
			yield db
		finally:
			pass
	
	avis_app.dependency_overrides[obtenir_session] = override_session
	yield avis_app
	avis_app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client_avis(app_avis):
	"""Client de test pour le service AVIS."""
	return TestClient(app_avis)


@pytest.fixture(scope="function")
def app_auth(db):
	"""Application AUTH avec override de la session."""
	def override_session():
		try:
			yield db
		finally:
			pass
	
	auth_app.dependency_overrides[obtenir_session] = override_session
	yield auth_app
	auth_app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client_auth(app_auth):
	"""Client de test pour le service AUTH."""
	return TestClient(app_auth)


@pytest.fixture
def utilisateur_client(client_auth):
	"""Crée un utilisateur CLIENT et retourne son token."""
	import random
	unique_id = random.randint(10000, 99999)
	response = client_auth.post("/auth/inscription", json={
		"courriel": f"client.avis{unique_id}@test.com",
		"nom_complet": "Test Client Avis",
		"mot_de_passe": "Test123456"
	})
	assert response.status_code == 201
	user_id = response.json()["identifiant"]
	
	login_response = client_auth.post("/auth/connexion", json={
		"courriel": f"client.avis{unique_id}@test.com",
		"mot_de_passe": "Test123456"
	})
	assert login_response.status_code == 200
	token = login_response.json()["access_token"]
	
	return {"id": user_id, "token": token}


@pytest.fixture
def utilisateur_client2(client_auth):
	"""Crée un deuxième utilisateur CLIENT."""
	import random
	unique_id = random.randint(10000, 99999)
	response = client_auth.post("/auth/inscription", json={
		"courriel": f"client2.avis{unique_id}@test.com",
		"nom_complet": "Test Client2 Avis",
		"mot_de_passe": "Test123456"
	})
	assert response.status_code == 201
	user_id = response.json()["identifiant"]
	
	login_response = client_auth.post("/auth/connexion", json={
		"courriel": f"client2.avis{unique_id}@test.com",
		"mot_de_passe": "Test123456"
	})
	assert login_response.status_code == 200
	token = login_response.json()["access_token"]
	
	return {"id": user_id, "token": token}


@pytest.fixture
def utilisateur_admin(client_auth, db):
	"""Crée un utilisateur ADMIN et retourne son token."""
	import random
	unique_id = random.randint(10000, 99999)
	response = client_auth.post("/auth/inscription", json={
		"courriel": f"admin.avis{unique_id}@test.com",
		"nom_complet": "Test Admin Avis",
		"mot_de_passe": "Admin123456"
	})
	assert response.status_code == 201
	user_id = response.json()["identifiant"]

	# Changer rôle en ADMIN directement en BD
	from MICROSERVICES.AUTHENTIFICATION.models.user import Utilisateur, RoleUtilisateur
	utilisateur = db.query(Utilisateur).filter(Utilisateur.identifiant == user_id).first()
	utilisateur.role = RoleUtilisateur.ADMINISTRATEUR
	db.commit()
	
	login_response = client_auth.post("/auth/connexion", json={
		"courriel": f"admin.avis{unique_id}@test.com",
		"mot_de_passe": "Admin123456"
	})
	assert login_response.status_code == 200
	token = login_response.json()["access_token"]
	
	return {"id": user_id, "token": token}


@pytest.fixture
def produit_test(db, utilisateur_client):
	"""Crée un produit pour tester les avis."""
	from MICROSERVICES.CATALOGUE.models.produit import Produit
	from MICROSERVICES.CATALOGUE.models.categorie import Categorie
	from uuid import uuid4
	
	# Créer une catégorie
	categorie = Categorie(nom=f"Test Catégorie {uuid4().hex[:8]}", est_actif=True)
	db.add(categorie)
	db.flush()
	
	# Créer un produit avec le vendeur existant
	produit = Produit(
		identifiant=uuid4(),
		vendeur_identifiant=utilisateur_client["id"],
		categorie_identifiant=categorie.identifiant,
		nom="Produit Test Avis",
		description="Description test",
		prix_cfa=5000,
		stock=10,
		est_actif=True
	)
	db.add(produit)
	db.commit()
	db.refresh(produit)
	return produit


class TestAvisPublique:
	"""Tests des routes publiques (pas d'authentification)."""
	
	def test_lister_avis_produit_vide(self, client_avis, produit_test):
		"""Lister les avis d'un produit sans avis."""
		response = client_avis.get(f"/avis/public/produits/{produit_test.identifiant}/avis")
		assert response.status_code == 200
		assert response.json() == []
	
	def test_lister_avis_produit_avec_avis(self, client_avis, produit_test, utilisateur_client, db):
		"""Lister les avis d'un produit avec des avis."""
		from MICROSERVICES.AVIS.models.avis import Avis
		
		# Créer un avis directement en BDD
		avis = Avis(
			produit_identifiant=produit_test.identifiant,
			client_identifiant=utilisateur_client["id"],
			note=5,
			titre="Excellent produit",
			commentaire="Très satisfait de mon achat"
		)
		db.add(avis)
		db.commit()
		
		response = client_avis.get(f"/avis/public/produits/{produit_test.identifiant}/avis")
		assert response.status_code == 200
		avis_list = response.json()
		assert len(avis_list) == 1
		assert avis_list[0]["note"] == 5
		assert avis_list[0]["titre"] == "Excellent produit"
	
	def test_obtenir_avis(self, client_avis, produit_test, utilisateur_client, db):
		"""Obtenir le détail d'un avis."""
		from MICROSERVICES.AVIS.models.avis import Avis
		
		avis = Avis(
			produit_identifiant=produit_test.identifiant,
			client_identifiant=utilisateur_client["id"],
			note=4,
			titre="Bon produit",
			commentaire="Rapport qualité/prix correct"
		)
		db.add(avis)
		db.commit()
		db.refresh(avis)
		
		response = client_avis.get(f"/avis/public/avis/{avis.identifiant}")
		assert response.status_code == 200
		data = response.json()
		assert data["note"] == 4
		assert data["titre"] == "Bon produit"
		assert data["commentaire"] == "Rapport qualité/prix correct"
	
	def test_obtenir_avis_inexistant(self, client_avis):
		"""Obtenir un avis qui n'existe pas."""
		from uuid import uuid4
		response = client_avis.get(f"/avis/public/avis/{uuid4()}")
		assert response.status_code == 404


class TestAvisClient:
	"""Tests des routes client (création, modification, suppression d'avis)."""
	
	def test_creer_avis(self, client_avis, produit_test, utilisateur_client):
		"""Client crée un avis."""
		headers = {"Authorization": f"Bearer {utilisateur_client['token']}"}
		response = client_avis.post(
			"/avis/client/avis",
			json={
				"produit_identifiant": str(produit_test.identifiant),
				"note": 5,
				"titre": "Super produit !",
				"commentaire": "Je recommande vivement"
			},
			headers=headers
		)
		assert response.status_code == 201
		data = response.json()
		assert data["note"] == 5
		assert data["titre"] == "Super produit !"
		assert data["commentaire"] == "Je recommande vivement"
		assert data["produit_identifiant"] == str(produit_test.identifiant)
		assert data["client_identifiant"] == utilisateur_client["id"]
	
	def test_creer_avis_doublon(self, client_avis, produit_test, utilisateur_client):
		"""Client ne peut pas créer deux avis pour le même produit."""
		headers = {"Authorization": f"Bearer {utilisateur_client['token']}"}
		
		# Premier avis
		response1 = client_avis.post(
			"/avis/client/avis",
			json={
				"produit_identifiant": str(produit_test.identifiant),
				"note": 5,
				"titre": "Premier avis"
			},
			headers=headers
		)
		assert response1.status_code == 201
		
		# Deuxième avis (devrait échouer)
		response2 = client_avis.post(
			"/avis/client/avis",
			json={
				"produit_identifiant": str(produit_test.identifiant),
				"note": 4,
				"titre": "Deuxième avis"
			},
			headers=headers
		)
		assert response2.status_code == 400
		assert "déjà laissé un avis" in response2.json()["detail"]
	
	def test_creer_avis_note_invalide(self, client_avis, produit_test, utilisateur_client):
		"""Note doit être entre 1 et 5."""
		headers = {"Authorization": f"Bearer {utilisateur_client['token']}"}
		
		# Note trop basse
		response = client_avis.post(
			"/avis/client/avis",
			json={
				"produit_identifiant": str(produit_test.identifiant),
				"note": 0,
				"titre": "Test"
			},
			headers=headers
		)
		assert response.status_code == 422
		
		# Note trop haute
		response = client_avis.post(
			"/avis/client/avis",
			json={
				"produit_identifiant": str(produit_test.identifiant),
				"note": 6,
				"titre": "Test"
			},
			headers=headers
		)
		assert response.status_code == 422
	
	def test_modifier_son_avis(self, client_avis, produit_test, utilisateur_client, db):
		"""Client modifie son propre avis."""
		from MICROSERVICES.AVIS.models.avis import Avis
		
		# Créer un avis
		avis = Avis(
			produit_identifiant=produit_test.identifiant,
			client_identifiant=utilisateur_client["id"],
			note=3,
			titre="Moyen",
			commentaire="Pas terrible"
		)
		db.add(avis)
		db.commit()
		db.refresh(avis)
		
		# Modifier l'avis
		headers = {"Authorization": f"Bearer {utilisateur_client['token']}"}
		response = client_avis.patch(
			f"/avis/client/avis/{avis.identifiant}",
			json={
				"note": 5,
				"titre": "Finalement excellent !",
				"commentaire": "Après utilisation, je change d'avis"
			},
			headers=headers
		)
		assert response.status_code == 200
		data = response.json()
		assert data["note"] == 5
		assert data["titre"] == "Finalement excellent !"
	
	def test_modifier_avis_autre_client(self, client_avis, produit_test, utilisateur_client, utilisateur_client2, db):
		"""Client ne peut pas modifier l'avis d'un autre client."""
		from MICROSERVICES.AVIS.models.avis import Avis
		
		# Créer un avis par client1
		avis = Avis(
			produit_identifiant=produit_test.identifiant,
			client_identifiant=utilisateur_client["id"],
			note=4,
			titre="Avis client 1"
		)
		db.add(avis)
		db.commit()
		db.refresh(avis)
		
		# Client 2 tente de modifier
		headers = {"Authorization": f"Bearer {utilisateur_client2['token']}"}
		response = client_avis.patch(
			f"/avis/client/avis/{avis.identifiant}",
			json={"note": 1},
			headers=headers
		)
		assert response.status_code == 403
	
	def test_supprimer_son_avis(self, client_avis, produit_test, utilisateur_client, db):
		"""Client supprime son propre avis."""
		from MICROSERVICES.AVIS.models.avis import Avis
		
		avis = Avis(
			produit_identifiant=produit_test.identifiant,
			client_identifiant=utilisateur_client["id"],
			note=2,
			titre="Je veux supprimer"
		)
		db.add(avis)
		db.commit()
		db.refresh(avis)
		
		headers = {"Authorization": f"Bearer {utilisateur_client['token']}"}
		response = client_avis.delete(f"/avis/client/avis/{avis.identifiant}", headers=headers)
		assert response.status_code == 200
		assert "supprimé" in response.json()["message"]
	
	def test_ajouter_image_avis(self, client_avis, produit_test, utilisateur_client, db):
		"""Client ajoute une image à son avis."""
		from MICROSERVICES.AVIS.models.avis import Avis
		
		avis = Avis(
			produit_identifiant=produit_test.identifiant,
			client_identifiant=utilisateur_client["id"],
			note=5,
			titre="Avec photo"
		)
		db.add(avis)
		db.commit()
		db.refresh(avis)
		
		headers = {"Authorization": f"Bearer {utilisateur_client['token']}"}
		response = client_avis.post(
			f"/avis/client/avis/{avis.identifiant}/images",
			json={
				"url_image": "https://example.com/photo.jpg",
				"position": 1
			},
			headers=headers
		)
		assert response.status_code == 201
		data = response.json()
		assert data["url_image"] == "https://example.com/photo.jpg"
		assert data["position"] == 1
		assert data["avis_identifiant"] == str(avis.identifiant)
	
	def test_creer_avis_sans_auth(self, client_avis, produit_test):
		"""Créer un avis sans token doit échouer."""
		response = client_avis.post(
			"/avis/client/avis",
			json={
				"produit_identifiant": str(produit_test.identifiant),
				"note": 5,
				"titre": "Test",
			}
		)
		assert response.status_code == 401


class TestAvisAdmin:
	"""Tests des routes admin (modération)."""
	
	def test_admin_supprime_avis(self, client_avis, produit_test, utilisateur_client, utilisateur_admin, db):
		"""Admin peut supprimer n'importe quel avis."""
		from MICROSERVICES.AVIS.models.avis import Avis
		
		# Client crée un avis
		avis = Avis(
			produit_identifiant=produit_test.identifiant,
			client_identifiant=utilisateur_client["id"],
			note=1,
			titre="Contenu inapproprié",
			commentaire="À modérer"
		)
		db.add(avis)
		db.commit()
		db.refresh(avis)
		
		# Admin supprime
		headers = {"Authorization": f"Bearer {utilisateur_admin['token']}"}
		response = client_avis.delete(f"/avis/admin/avis/{avis.identifiant}", headers=headers)
		assert response.status_code == 200
		assert "supprimé" in response.json()["message"]
	
	def test_client_ne_peut_pas_moderer(self, client_avis, produit_test, utilisateur_client, utilisateur_client2, db):
		"""Client ne peut pas utiliser la route admin."""
		from MICROSERVICES.AVIS.models.avis import Avis
		
		avis = Avis(
			produit_identifiant=produit_test.identifiant,
			client_identifiant=utilisateur_client["id"],
			note=3
		)
		db.add(avis)
		db.commit()
		db.refresh(avis)
		
		# Client 2 tente d'utiliser la route admin
		headers = {"Authorization": f"Bearer {utilisateur_client2['token']}"}
		response = client_avis.delete(f"/avis/admin/avis/{avis.identifiant}", headers=headers)
		assert response.status_code == 403


class TestHealth:
	"""Test du endpoint de santé."""
	
	def test_health(self, client_avis):
		response = client_avis.get("/health")
		assert response.status_code == 200
		assert response.json() == {"status": "ok"}
