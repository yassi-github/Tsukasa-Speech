#!/bin/bash

set -e

if [[ ! -e pyproject.toml ]]; then
    printf 'ERROR: pyproject.toml not found on current directory. CWD: %s\n' "$(pwd)"
    exit 1
fi

uv python install
uv sync

exec uv run python app_tsuka.py
