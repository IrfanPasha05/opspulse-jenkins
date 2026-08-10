import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app


def test_homepage():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"OpsPulse" in response.data


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_api_status():
    client = app.test_client()

    response = client.get("/api/status")

    assert response.status_code == 200
    assert response.json["application"] == "OpsPulse"
    assert response.json["status"] == "running"
