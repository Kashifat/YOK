import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from MICROSERVICES.PAIEMENT_VENDEURS.main import app


def test_health_paiement_vendeurs():
	client = TestClient(app)
	response = client.get("/health")

	assert response.status_code == 200
	assert response.json() == {"status": "ok", "service": "paiement_vendeurs"}


def test_wallet_me_requires_auth():
	client = TestClient(app)
	response = client.get("/wallet-vendeurs/moi")

	assert response.status_code == 401
