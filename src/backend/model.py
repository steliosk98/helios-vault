from typing import Optional
import os


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


# Optional llama-cpp-python wrapper. If the package is available at runtime,
# `get_model` will return a wrapper around it; otherwise it returns `ModelStub`.
try:
    from llama_cpp import Llama  # type: ignore

    class LlamaCppModel:
        def __init__(self, model_path: Optional[str] = None, **kwargs):
            self.model_path = model_path or os.getenv("MODEL_PATH")
            self.name = f"llama-cpp:{os.path.basename(self.model_path) if self.model_path else 'unknown'}"
            self._kwargs = kwargs
            self._llama = None

        def load(self):
            if not self.model_path:
                raise ValueError("MODEL_PATH not provided for LlamaCppModel")
            # Instantiate the underlying Llama model. This may require native libs.
            self._llama = Llama(model_path=self.model_path)
            return True

        def generate(self, prompt: str) -> str:
            if self._llama is None:
                # Lazy load
                self.load()
            # Use the simple call API — tweak as needed when integrating for real
            out = self._llama(prompt)
            # `out` structure depends on llama-cpp-python version; handle common case
            generated = getattr(out, "generations", None)
            if generated:
                # join texts from first generation if present
                try:
                    texts = [g[0].text for g in generated]
                    return "".join(texts)
                except Exception:
                    pass
            # Fallback to string representation
            return str(out)

except Exception:
    LlamaCppModel = None  # type: ignore


def get_model(model_path: Optional[str] = None):
    """Return a model instance. Prefers LlamaCppModel when available, otherwise ModelStub."""
    # Prefer explicit env selection if provided
    preferred = os.getenv("MODEL_BACKEND", "auto").lower()
    if preferred == "stub":
        return ModelStub(model_path=model_path)

    if LlamaCppModel is not None and preferred in ("auto", "llama"):
        try:
            return LlamaCppModel(model_path=model_path)
        except Exception:
            # Fall through to stub on any instantiation error
            return ModelStub(model_path=model_path)

    return ModelStub(model_path=model_path)
