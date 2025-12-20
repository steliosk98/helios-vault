# AGENTS.md — Helios Vault

## Purpose
This document exists to provide AI collaborators with persistent context, architectural goals, project direction, constraints, and development philosophy for Helios Vault. It ensures continuity across interactions and prevents loss of intent or momentum.

---

## Project Description
Helios Vault is an open-source, offline-first survival AI platform designed to preserve and deliver critical human knowledge and reasoning in a world without internet access or external infrastructure. It combines local LLM inference with a self-contained knowledge archive to support survival, rebuilding, education, engineering, medicine, agriculture, mechanics, and long-term self-reliance.

Helios Vault is designed to operate across a wide range of hardware profiles and remain functional even in extreme operational environments.

---

## Core Principles
1. Entirely offline — no internet dependency.
2. Hardware scalable — from low-power boards to high-end systems.
3. Open-source — transparent, forkable, and community-driven.
4. Modular — every component replaceable or upgradable.
5. Simple first — minimal dependencies, minimal assumptions.
6. Durable — future-proof, resilient, self-contained.
7. Human-centric — supports survival, not convenience.

---

## Tech Stack (Current Intent)
- Python
- llama.cpp backend (via llama-cpp-python)
- FastAPI backend API
- Local browser UI (HTML/CSS/JS)
- FAISS vector search engine
- SQLite + filesystem for storage
- Multiple GGUF model options
- Embedding + retrieval pipeline (future)

---

## Roadmap
### MVP (current target)
- Local model inference
- Basic chat interface (browser-based)
- Python backend + FastAPI streaming
- Model selection based on hardware tier
- Fully offline execution

### Future Milestones
- Knowledge ingestion + embedding
- Vector database search
- Extended knowledge domains
- Multi-model support
- GPU acceleration
- Local packaging + installers
- Tauri desktop UI option

---

## AI Collaboration Guidelines
- Maintain project philosophy and boundaries.
- Assume zero internet access at runtime.
- Prefer simplicity → reduce dependencies where possible.
- Protect cross-platform compatibility.
- Avoid introducing assumptions of cloud services or APIs.
- Keep code clean, modular, documented, and extensible.
- Provide reasoning for structural decisions.
- When unclear, propose options rather than guessing.

---

## Status Log Pointer
More dynamic development status is maintained in `AGENTS_LOCAL.md`, which is intentionally excluded from version control to allow evolving context during development.

---

## Closing Note
Helios Vault is intended to be a digital seed for humanity — a durable knowledge engine capable of providing guidance in extreme or future scenarios.

All AI collaborators should treat contributions as part of a long-term human knowledge preservation effort.
