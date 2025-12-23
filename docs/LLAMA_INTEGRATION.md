# Llama-cpp-python Integration (Optional)

This document explains how to enable a real local model backend using `llama-cpp-python`. This is optional — the codebase includes a `ModelStub` and a safe `get_model()` factory that falls back to the stub when `llama-cpp-python` or native requirements are not present.

Prerequisites
- A Linux/macOS environment (or compatible build target)
- A supported C/C++ toolchain for building native wheels (gcc/clang, make, etc.)
- Sufficient RAM and disk for the model you intend to run (models can be many GB)

Install (recommended in a virtualenv)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
# Install optional package (may require system packages)
python -m pip install "llama-cpp-python"
```

Model files
- Place your GGUF or compatible model in the `models/` directory or any path you choose.
- Do NOT commit model binaries to the repository; add them to `.gitignore` if placed under `models/`.

Environment variables
- `MODEL_PATH` — full path to model file (e.g. `/data/models/llama-7b.gguf`)
- `MODEL_BACKEND` — backend selection: `auto` (default), `stub`, or `llama`
- `MODEL_N_CTX` — context window size (default `2048`)
- `MODEL_THREADS` — CPU threads for inference (default `4`)
- `MODEL_TEMPERATURE` — sampling temperature (default `0.7`)
- `MODEL_MAX_TOKENS` — max tokens per response (default `256`)

Run the server with the real backend

```bash
export MODEL_PATH=/path/to/your/model.gguf
export MODEL_BACKEND=llama
./scripts/run.sh
```

Download models with the manifest

```bash
python3 scripts/fetch_models.py --list
python3 scripts/fetch_models.py --tier 0 --tier 1 --tier 2
```

Test the `/chat` endpoint

```bash
curl -sS -X POST http://127.0.0.1:8000/chat -H 'Content-Type: application/json' -d '{"message":"Hello"}'
```

Notes and troubleshooting
- If `llama-cpp-python` fails to import, the app will automatically fall back to `ModelStub` and tests will continue to pass.
- Building `llama-cpp-python` may require system dependencies like `cmake`, `gcc`, and additional libraries depending on your platform.
- For production use, test memory and CPU/GPU requirements, and consider using a machine with sufficient RAM or swap configured.

Security
- All models run locally; ensure model files come from trusted sources. Models can contain unexpected content.
