# Water Mill cell template — build, run, and the `make verify` merge gate.
#
# Fail on the first error, and on a failure anywhere in a pipeline: without
# `pipefail`, `cmd | tail` reports tail's exit status and a failing check
# reads as a pass.
SHELL := /bin/bash
.SHELLFLAGS := --norc -eu -o pipefail -c

.PHONY: all install build dev start clean \
        verify verify-fast guard lint lint-py lint-js typecheck \
        test test-py test-js help

VENV := .venv
PY   := $(VENV)/bin/python

all: build start

## install: create .venv and install Python + Node dependencies
install:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt
	cd frontend && npm ci

## build: build the frontend into static/dist
build:
	@echo "== build =="
	cd frontend && npm run build

## dev: Vite HMR + Flask API (run each in its own terminal)
dev:
	@echo "Terminal 1:  $(PY) app.py"
	@echo "Terminal 2:  cd frontend && npm run dev"

## start: start the Flask server
start:
	$(PY) app.py

## clean: remove build artifacts, caches and the virtualenv
clean:
	rm -rf static/dist frontend/node_modules $(VENV)
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true

# ---------------------------------------------------------------------------
# The verification gate. Ordered cheapest-first. No target may swallow a
# failure: no `-` prefixes, no `|| true`, no retries.
# ---------------------------------------------------------------------------

## verify: the full gate. Must pass before any change is merged.
verify: guard build lint test
	@echo
	@echo "verify passed"

## verify-fast: quick subset for tight iteration. NOT sufficient for merge.
verify-fast: guard build lint
	@echo
	@echo "verify-fast passed — does NOT include tests, not a merge gate"

## guard: refuse to run if the environment is not local and isolated
guard:
	@echo "== guard =="
	@test -x "$(PY)" || { \
	  echo "no virtualenv at $(VENV) — run: make install"; exit 1; }
	@test -d frontend/node_modules || { \
	  echo "frontend/node_modules missing — run: make install"; exit 1; }
	@# Tests are handed a throwaway DATA_DIR below; this proves the app
	@# honours it, so a config.py change that ignores the variable fails here
	@# rather than silently writing beside the live database.
	@DATA_DIR=/tmp/cell-verify-guard $(PY) -c \
	  "import config, sys; \
	   sys.exit(0) if config.DATA_DIR == '/tmp/cell-verify-guard' \
	   else (print('config.DATA_DIR ignores the environment:', config.DATA_DIR), sys.exit(1))"
	@for v in FLASK_ENV NODE_ENV APP_ENV ENVIRONMENT; do \
	  if [ "$$(eval echo \$${$$v:-})" = "production" ]; then \
	    echo "$$v=production: refusing to run verify"; exit 1; \
	  fi; \
	done
	@echo "environment is local and isolated"

## lint: both linters — ruff over the backend, ESLint over the frontend
lint: lint-py lint-js

lint-py:
	@echo "== lint-py =="
	$(VENV)/bin/ruff check --no-cache .
	@echo "ruff clean"

lint-js:
	@echo "== lint-js =="
	cd frontend && npx eslint . --max-warnings=0
	@echo "eslint clean"

## typecheck: NOT CONFIGURED — deliberately fails so it can never turn a
## result green. A step that always succeeds must not be part of a gate.
typecheck:
	@echo "== typecheck =="
	@echo "No type checker is configured for this cell."
	@exit 1

## test: both suites — Vitest over the frontend, pytest over the backend
test: test-js test-py

test-js:
	@echo "== test-js =="
	cd frontend && npx vitest run
	@echo "vitest passed"

test-py:
	@echo "== test-py =="
	DATA_DIR=$$(mktemp -d) $(PY) -m pytest -q tests/
	@echo "pytest passed"

## help: list targets
help:
	@grep -E '^## ' Makefile | sed 's/^## //'
