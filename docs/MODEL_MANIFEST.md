# Model Manifest Guide

This document explains how `models_manifest.json` is structured and how to keep it up to date.

## Purpose
The manifest defines recommended GGUF models for each hardware tier and provides download metadata
for `scripts/fetch_models.py`.
URLs are public by default to avoid authentication requirements.

## Manifest fields
- `id`: Short unique identifier (used by scripts).
- `tier`: Hardware tier (0–3).
- `name`: Human-friendly name.
- `repo`: Hugging Face repo (for default download URLs).
- `file`: GGUF filename in the repo.
- `revision`: Optional branch/tag/commit (default: `main`).
- `url`: Optional full URL override (bypasses `repo` + `file`).
- `size_gb`: Approximate size in GB.
- `sha256`: Optional checksum for verification.
- `optional`: Whether to skip unless `--include-optional` is provided.
- `notes`: Any extra context.

## Add or update a model
1) Choose a model and verify licensing.
2) Add an entry with `repo` + `file` (or a direct `url`).
3) Download the file with `scripts/fetch_models.py`.
4) Update checksums:

```bash
python3 scripts/update_manifest_checksums.py --model <id>
```

Use `--all` to update all locally downloaded models.

## Offline workflow
If you need a fully offline process, download models on a connected machine and transfer them to
`models/`. Then run `scripts/update_manifest_checksums.py` locally to populate `sha256`.
