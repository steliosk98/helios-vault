from typing import Optional


class ModelStub:
    """A minimal model-loading stub. Replace with actual llama.cpp loader later.

    Behavior: returns a deterministic canned reply including the input message.
    """

    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or "models/stub-model"
        self.name = "model-stub"

    def load(self):
        # Placeholder for loading logic. No-op for stub.
        return True

    def generate(self, prompt: str) -> str:
        # Simple deterministic placeholder reply.
        safe = prompt.strip() if prompt else ""
        return f"[stub reply] I received: {safe}"
