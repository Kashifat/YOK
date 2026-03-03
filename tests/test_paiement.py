import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from MICROSERVICES.PAIEMENT_CLIENTS.main import app


def test_health_paiement():
	client = TestClient(app)
	response = client.get("/health")

	assert response.status_code == 200
	assert response.json() == {"status": "ok", "service": "paiement_clients"}


def test_retour_cinetpay_requires_auth():
	client = TestClient(app)
	response = client.get("/paiements/retour/cinetpay", params={"transaction_id": "TX-TEST"})

	assert response.status_code == 401
