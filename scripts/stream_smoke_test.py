#!/usr/bin/env python3
import os
import sys

from fastapi.testclient import TestClient

# Ensure repo root is on sys.path so `src` package is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.backend.main import app


def main() -> int:
    with TestClient(app) as client:
        health = client.get("/health").json()
        model = health.get("model", {})
        if model.get("backend") != "llama-cpp":
            print("Expected llama-cpp backend, got:", model.get("backend"))
            return 2

        with client.stream("POST", "/chat/stream", json={"message": "Hello from Helios"}) as r:
            if r.status_code != 200:
                print("Streaming request failed:", r.status_code, r.text)
                return 3
            text = "".join(list(r.iter_text()))

    if not text.strip():
        print("Empty response")
        return 4

    preview = text.strip().replace("\n", " ")[:120]
    print(f"Streaming response length={len(text)} preview={preview!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
