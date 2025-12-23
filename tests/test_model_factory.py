import os
import sys

import importlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.backend import model as model_mod
from src.backend.main import app
from fastapi.testclient import TestClient


def test_get_model_with_stub_env(monkeypatch):
    monkeypatch.setenv("MODEL_BACKEND", "stub")
    m = model_mod.get_model()
    assert isinstance(m, model_mod.ModelStub)
    assert m.generate("x").startswith("[stub reply]")


def test_get_model_with_llama_env_fallback(monkeypatch):
    # If llama backend isn't available at runtime, get_model should fall back to stub
    monkeypatch.setenv("MODEL_BACKEND", "llama")
    monkeypatch.delenv("MODEL_PATH", raising=False)
    m = model_mod.get_model()
    # If LlamaCppModel is not available, this must be ModelStub; otherwise ensure it has generate
    if getattr(model_mod, "LlamaCppModel", None) is None:
        assert isinstance(m, model_mod.ModelStub)
    else:
        assert isinstance(m, model_mod.ModelStub)


def test_app_startup_initializes_model(monkeypatch):
    # Ensure that when the app starts, `app.state.model` exists and provides `generate`.
    monkeypatch.setenv("MODEL_BACKEND", "stub")
    monkeypatch.delenv("MODEL_PATH", raising=False)
    with TestClient(app) as client:
        assert hasattr(client.app.state, "model")
        m = client.app.state.model
        assert hasattr(m, "generate")
        # exercise generate with a short input
        out = m.generate("hello")
        assert isinstance(out, str)
