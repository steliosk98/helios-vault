#!/usr/bin/env bash
set -euo pipefail

# Simple run script for development
PYTHON=${PYTHON:-python3}
PORT=${PORT:-8000}

echo "Starting Helios Vault backend on http://0.0.0.0:${PORT}"
${PYTHON} -m uvicorn src.backend.main:app --host 0.0.0.0 --port ${PORT} --reload
