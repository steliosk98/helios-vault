from typing import Optional, Dict, Any, Iterable
import os


class ModelStub:
    """A minimal model-loading stub. Replace with actual llama.cpp loader later.

    Behavior: returns a deterministic canned reply including the input message.
    """

    def __init__(self, model_path: Optional[str] = None, last_error: Optional[str] = None):
        self.model_path = model_path or "models/stub-model"
        self.name = "model-stub"
        self.backend = "stub"
        self.loaded = False
        self.last_error = last_error

    def load(self):
        # Placeholder for loading logic. No-op for stub.
        self.loaded = True
        return True

    def generate(self, prompt: str) -> str:
        # Simple deterministic placeholder reply.
        if not self.loaded:
            self.load()
        safe = prompt.strip() if prompt else ""
        return f"[stub reply] I received: {safe}"

    def generate_stream(self, prompt: str) -> Iterable[str]:
        reply = self.generate(prompt)
        chunk_size = 24
        for idx in range(0, len(reply), chunk_size):
            yield reply[idx : idx + chunk_size]


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _default_model_kwargs() -> Dict[str, Any]:
    return {
        "n_ctx": _env_int("MODEL_N_CTX", 2048),
        "n_threads": _env_int("MODEL_THREADS", 4),
    }


def _default_gen_kwargs() -> Dict[str, Any]:
    return {
        "temperature": _env_float("MODEL_TEMPERATURE", 0.7),
        "max_tokens": _env_int("MODEL_MAX_TOKENS", 256),
    }


# Optional llama-cpp-python wrapper. If the package is available at runtime,
# `get_model` will return a wrapper around it; otherwise it returns `ModelStub`.
try:
    from llama_cpp import Llama  # type: ignore

    class LlamaCppModel:
        def __init__(
            self,
            model_path: Optional[str] = None,
            model_kwargs: Optional[Dict[str, Any]] = None,
            gen_kwargs: Optional[Dict[str, Any]] = None,
            **kwargs: Any,
        ):
            self.model_path = model_path or os.getenv("MODEL_PATH")
            self.name = f"llama-cpp:{os.path.basename(self.model_path) if self.model_path else 'unknown'}"
            self.backend = "llama-cpp"
            merged_model_kwargs = _default_model_kwargs()
            if model_kwargs:
                merged_model_kwargs.update(model_kwargs)
            if kwargs:
                merged_model_kwargs.update(kwargs)
            self._model_kwargs = merged_model_kwargs
            merged_gen_kwargs = _default_gen_kwargs()
            if gen_kwargs:
                merged_gen_kwargs.update(gen_kwargs)
            self._gen_kwargs = merged_gen_kwargs
            self._llama = None
            self.loaded = False
            self.last_error = None

        def load(self):
            if not self.model_path:
                err = "MODEL_PATH not provided for LlamaCppModel"
                self.last_error = err
                raise ValueError(err)
            try:
                # Instantiate the underlying Llama model. This may require native libs.
                self._llama = Llama(model_path=self.model_path, **self._model_kwargs)
                self.loaded = True
                return True
            except Exception as exc:
                self.last_error = str(exc)
                raise

        def generate(self, prompt: str) -> str:
            if self._llama is None:
                # Lazy load
                self.load()
            # Use the simple call API — tweak as needed when integrating for real
            out = self._llama(prompt, **self._gen_kwargs)
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

        def generate_stream(self, prompt: str) -> Iterable[str]:
            if self._llama is None:
                self.load()
            try:
                stream = self._llama(prompt, stream=True, **self._gen_kwargs)
                for chunk in stream:
                    if isinstance(chunk, dict):
                        choices = chunk.get("choices") or []
                        if choices and isinstance(choices[0], dict):
                            text = choices[0].get("text")
                            if text:
                                yield text
                                continue
                    text = str(chunk)
                    if text:
                        yield text
            except Exception:
                yield self.generate(prompt)

except Exception:
    LlamaCppModel = None  # type: ignore


def get_model(model_path: Optional[str] = None):
    """Return a model instance. Prefers LlamaCppModel when available, otherwise ModelStub."""
    # Prefer explicit env selection if provided
    preferred = os.getenv("MODEL_BACKEND", "auto").lower()
    if preferred == "stub":
        stub = ModelStub(model_path=model_path)
        stub.load()
        return stub

    resolved_path = model_path or os.getenv("MODEL_PATH")
    if LlamaCppModel is not None and preferred in ("auto", "llama"):
        if not resolved_path:
            stub = ModelStub(model_path=model_path, last_error="MODEL_PATH not provided")
            stub.load()
            return stub
        try:
            return LlamaCppModel(model_path=resolved_path)
        except Exception:
            # Fall through to stub on any instantiation error
            stub = ModelStub(model_path=model_path, last_error="Failed to initialize llama backend")
            stub.load()
            return stub

    stub_error = None
    if preferred == "llama" and LlamaCppModel is None:
        stub_error = "llama-cpp-python not available"
    stub = ModelStub(model_path=model_path, last_error=stub_error)
    stub.load()
    return stub


def get_model_status(model: Any) -> Dict[str, Any]:
    if model is None:
        return {"backend": None, "name": None, "loaded": False, "error": "Model not initialized"}

    return {
        "backend": getattr(model, "backend", model.__class__.__name__),
        "name": getattr(model, "name", model.__class__.__name__),
        "loaded": bool(getattr(model, "loaded", False)),
        "error": getattr(model, "last_error", None),
        "model_path": getattr(model, "model_path", None),
    }
