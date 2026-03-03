import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from MICROSERVICES.LIVRAISON.main import app


def test_health_livraison():
	client = TestClient(app)
	response = client.get("/health")

	assert response.status_code == 200
	assert response.json() == {"status": "ok", "service": "livraison"}


def test_ramassage_requires_auth():
	client = TestClient(app)
	response = client.patch("/livraisons/00000000-0000-0000-0000-000000000000/ramassage-vendeur", json={})

	assert response.status_code == 401
