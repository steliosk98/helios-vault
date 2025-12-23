from src.backend.model import ModelStub, get_model_status


def test_model_status_stub_loaded():
    stub = ModelStub()
    stub.load()
    status = get_model_status(stub)

    assert status["backend"] == "stub"
    assert status["name"] == "model-stub"
    assert status["loaded"] is True
    assert status["error"] in (None, "")
