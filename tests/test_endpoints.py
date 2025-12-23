import os
import sys

from fastapi.testclient import TestClient

# Ensure repo root is on sys.path so `src` package is importable during tests
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.backend.main import app




def test_root(monkeypatch):
    monkeypatch.setenv("MODEL_BACKEND", "stub")
    monkeypatch.delenv("MODEL_PATH", raising=False)
    with TestClient(app) as client:
        r = client.get("/")
        assert r.status_code == 200
        assert "text/html" in r.headers.get("content-type", "")


def test_status(monkeypatch):
    monkeypatch.setenv("MODEL_BACKEND", "stub")
    monkeypatch.delenv("MODEL_PATH", raising=False)
    with TestClient(app) as client:
        r = client.get("/status")
        assert r.status_code == 200
        body = r.json()
        assert body.get("status") == "ok"
        assert "version" in body


def test_health(monkeypatch):
    monkeypatch.setenv("MODEL_BACKEND", "stub")
    monkeypatch.delenv("MODEL_PATH", raising=False)
    with TestClient(app) as client:
        r = client.get("/health")
        assert r.status_code == 200
        body = r.json()
        assert body["healthy"] is True
        assert "model" in body
        assert body["model"]["name"] == "model-stub"


def test_chat(monkeypatch):
    monkeypatch.setenv("MODEL_BACKEND", "stub")
    monkeypatch.delenv("MODEL_PATH", raising=False)
    with TestClient(app) as client:
        r = client.post("/chat", json={"message": "Test message"})
        assert r.status_code == 200
        body = r.json()
        assert "reply" in body
        assert "model" in body
        assert body["model"] == "model-stub"
        assert "Test message" in body["reply"]


def test_chat_stream(monkeypatch):
    monkeypatch.setenv("MODEL_BACKEND", "stub")
    monkeypatch.delenv("MODEL_PATH", raising=False)
    with TestClient(app) as client:
        with client.stream("POST", "/chat/stream", json={"message": "Stream message"}) as r:
            assert r.status_code == 200
            text = "".join(list(r.iter_text()))
        assert "Stream message" in text
