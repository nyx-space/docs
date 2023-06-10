#!/bin/bash

# Define a function
setup() {
  pip install pipenv
  pipenv install
}

if [ -z "$VIRTUAL_ENV" ]; then
  # Not in a VENV
  if [ ! -d ".venv" ]; then
    # Build the new venv
    python3 -m venv .venv
  fi
  # Jump into it
  source .venv/bin/activate
fi

setup

pipenv run mkdocs $1
