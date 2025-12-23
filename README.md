# 🌑 Helios Vault

**Helios Vault is an open-source, offline-first survival AI system designed to preserve and deliver essential human knowledge without internet access.**

It combines local language model inference with a self-contained knowledge archive to enable reasoning, learning, and critical problem-solving — even in extreme scenarios where global infrastructure is gone.

Helios Vault is a digital seed for humanity: a durable, portable, local knowledge engine capable of guiding survival, rebuilding, and self-reliance across medicine, engineering, agriculture, energy, mechanics, education, and more.

---

## 🌞 Why Helios Vault?
Modern AI depends on cloud servers and constant connectivity — but in a world without the internet, that intelligence vanishes.

Helios Vault is designed for the opposite world:
- unreliable power
- isolated devices
- limited hardware resources
- no external services
- total offline operation

A survival brain in a dark age.

---

## 🌑 Project Goals
Helios Vault aims to:

- Run locally on a wide range of hardware
- Preserve essential survival and technical knowledge
- Remain open, transparent, and modifiable
- Provide long-term durability and resilience
- Offer guidance through reasoning, not static text
- Function without internet, forever

---

## 🌱 Current Status
🚧 Early development phase  
- Repository structure forming  
- Tech stack defined  
- UI, backend, and knowledge architecture planning in progress  

---

## 🧪 Development (Local)
Run the backend locally (stub model by default):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
./scripts/run.sh
```

Backend endpoints:
- `GET /` (serves local chat UI)
- `GET /status` (status)
- `GET /health` (includes model status)
- `POST /chat`
- `POST /chat/stream` (plain-text streaming)

Runtime configuration (copy `.env.example` to `.env` or export manually):
- `MODEL_BACKEND` = `auto` | `stub` | `llama`
- `MODEL_PATH` = path to a GGUF model
- `MODEL_N_CTX`, `MODEL_THREADS`, `MODEL_TEMPERATURE`, `MODEL_MAX_TOKENS`

---

## 📦 Model Downloads (Optional)
Helios Vault includes a manifest of recommended GGUF models for different hardware tiers.
Download them after cloning (kept out of git):

```bash
python3 scripts/fetch_models.py --list
python3 scripts/fetch_models.py --tier 0 --tier 1 --tier 2
```

Optional Tier 3 model (very large):

```bash
python3 scripts/fetch_models.py --tier 3 --include-optional
```

Notes:
- The manifest lives at `models_manifest.json`.
- Some GGUF filenames can change; if a download fails, update the manifest entry.
- Add `sha256` values to enable checksum verification.
- The manifest uses public URLs; no auth tokens are required.

Update checksums after downloads:

```bash
python3 scripts/update_manifest_checksums.py --all
```

---

## 🧠 Technology Overview
Helios Vault will be built on a foundation of:

- **Python** – core runtime
- **llama.cpp** – efficient local model inference
- **FastAPI** – API + streaming backend
- **Local browser UI** – platform-agnostic interface
- **FAISS** – future vector search for localized knowledge
- **SQLite + filesystem data** – durable offline storage

This architecture ensures accessible deployment across Linux, Windows, macOS, and ARM systems.

---

## 🔧 Hardware Tiers
Helios Vault will support multiple model sizes depending on available computing power:

- **Low power tier** – 1B–7B models
- **Balanced tier** – 7B–13B models
- **High power tier** – 30B+ models

Users select based on capability, not cloud restrictions.

---

## 📚 Knowledge System
Helios Vault will integrate a growing offline knowledge archive containing practical, reliable information across:

- medicine
- agriculture
- energy
- mechanics
- construction
- chemistry
- education
- survival skills

Coupled with LLM reasoning, this makes the system more than a chatbot — it becomes a synthetic mentor.

---

## 🎯 Development Philosophy
Helios Vault follows core principles:

- **Offline-first** — never dependent on cloud
- **Open-source** — transparent and community-driven
- **Hardware flexible** — efficient across devices
- **Simplicity first** — minimal dependencies
- **Resilient** — built for the long term
- **Human-centered** — safety and survival oriented

---

## 🚀 Roadmap (High-level)

### 🟢 MVP
- Local model inference
- Browser-based chat UI
- Basic backend + streaming
- Hardware tier selection
- Fully offline execution

### 🔶 v1.0
- Knowledge ingestion + embedding
- Vector search + recall
- Expanded knowledge base
- Model switching
- GPU acceleration

### 🔷 Future
- Education system
- Multilingual support
- Audio I/O
- Extended skill libraries
- Desktop build option

More detailed planning will be added to `/docs` as development progresses.

---

## 📝 Contributing
Helios Vault welcomes collaboration.  
Guidelines and structure will evolve as the project does.

AI assistance is intentionally integrated into development — persistent project context can be found in:

- `AGENTS.md` (committed reference)

---

## 📄 License
Helios Vault is fully open-source under the MIT License.  
See the `LICENSE` file for details.

---

## 🌑 Vision Closing
Helios Vault is not just another app — it is a repository of human knowledge and reasoning built to survive collapse and spark renewal.

A vault of light in dark times.  
A seed for humanity.
