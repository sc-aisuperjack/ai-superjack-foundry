#!/usr/bin/env bash
set -euo pipefail
cp .env.example .env || true
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
echo "Bootstrap complete. Start MongoDB and Redis with docker compose up -d mongodb redis"
