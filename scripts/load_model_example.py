#!/usr/bin/env python3
"""Example script to demonstrate model factory behavior.

This script attempts to instantiate the model via `get_model()` and call `load()` if supported.
It is safe to run without `llama-cpp-python` — it will use the `ModelStub`.
"""
import os
from src.backend.model import get_model


def main():
    model_path = os.getenv("MODEL_PATH")
    m = get_model(model_path=model_path)
    print(f"Using model backend: {m.__class__.__name__} (name={getattr(m, 'name', None)})")
    try:
        ok = m.load()
        print("Loaded model:", ok)
    except Exception as e:
        print("Model load failed:", e)
    print("Generate example:", m.generate("Hello from example"))


if __name__ == "__main__":
    main()
