import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from MICROSERVICES.FACTURE.main import app


def test_health_facture():
	client = TestClient(app)
	response = client.get("/health")

	assert response.status_code == 200
	assert response.json() == {"status": "ok", "service": "facture"}
