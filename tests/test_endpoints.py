import os
import sys

from fastapi.testclient import TestClient

# Ensure repo root is on sys.path so `src` package is importable during tests
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.backend.main import app




def test_root():
    with TestClient(app) as client:
        r = client.get("/")
        assert r.status_code == 200
        body = r.json()
        assert body.get("status") == "ok"
        assert "version" in body


def test_health():
    with TestClient(app) as client:
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json() == {"healthy": True}


def test_chat():
    with TestClient(app) as client:
        r = client.post("/chat", json={"message": "Test message"})
        assert r.status_code == 200
        body = r.json()
        assert "reply" in body
        assert "model" in body
        assert body["model"] == "model-stub"
        assert "Test message" in body["reply"]
