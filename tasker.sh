#!/bin/bash
set -euo pipefail

VENV_DIR=".venv"

# 1. Ensure uv is available
if ! command -v uv &> /dev/null; then
  pip install uv
fi

# 2. Force everything inside the venv
if [ ! -d "$VENV_DIR" ]; then
    uv venv "$VENV_DIR"
fi

# Direct uv to use the venv explicitly for the install
uv pip install --python "$VENV_DIR/bin/python" -r reqs.txt

# 3. Execute zensical directly out of the venv bin directory
exec "$VENV_DIR/bin/zensical" "$@"
