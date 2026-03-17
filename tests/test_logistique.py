import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from MICROSERVICES.LOGISTIQUE.main import app



def test_health_logistique():
	client = TestClient(app)
	response = client.get("/health")

	assert response.status_code == 200
	assert response.json() == {"status": "ok", "service": "logistique"}



def test_logistique_ping():
	client = TestClient(app)
	response = client.get("/logistique/health/ping")

	assert response.status_code == 200
	assert response.json()["message"] == "service logistique actif"
