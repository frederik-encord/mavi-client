#!/bin/bash
uv run ruff format .
uv run ruff check --fix .
uv run mypy . --check-untyped-defs --exclude=context/download.py