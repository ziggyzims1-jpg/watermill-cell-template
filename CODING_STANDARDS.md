# Coding standards

What this cell enforces or states today, gathered in one place so the bolter reviewer has a document to cite. Nothing here is new policy: each rule names where it is enforced (**gate** = `make verify` fails, **fence** = path in `watermill.yaml`, **doc** = stated in `CLAUDE.md`, an ADR or a docstring, checked by review only). When a rule is only a doc rule and keeps being broken, mechanise it. A stamped cell appends its own rules under "This cell" and leaves the rest.

## Gate and tooling

- `make verify` must be green before merge; CI runs exactly it. No target may swallow a failure (no `-` prefix, no `|| true`, no `continue-on-error`). [gate; ADR-0005]
- Python: ruff with `E4, E7, E9, F, B, C4, UP`, target `py311`, zero findings across the repository. [gate: `ruff.toml`]
- Frontend: ESLint at `--max-warnings=0` (recommended + react-hooks + react-refresh); unused variables are errors except names starting with a capital or underscore. [gate: `frontend/eslint.config.js`]
- Tests: pytest over `tests/`, Vitest over the frontend. Backend tests run under a throwaway `DATA_DIR`. [gate]
- There is no type checker; `make typecheck` fails on purpose. Do not add a step that always succeeds to a gate. [gate]

## Backend (Flask, SQLite)

- `routes/` holds blueprints registered in `app.py`; business logic lives in `services/`. [doc: `CLAUDE.md` architecture table]
- Migrations are append-only; `SCHEMA` references only what it creates; new columns go in both `SCHEMA` and `MIGRATIONS`; indexes go in `MIGRATIONS` only. [doc, fence: `db.py`; ADR-0006]
- One definition of today: `services/clock.py`. Never a second local definition. [doc: `CLAUDE.md`]
- All paths come from `config.py`; the data directory honours `DATA_DIR`. [gate: `make guard`]
- Never send secrets to the client. Secret config keys are write-only in any settings UI and redacted from any config read endpoint. [doc]
- Scheduled jobs record every run and outcome in `job_runs`; a job whose success is invisible needs a heartbeat and an alert on staleness. [doc]
- Verification never runs against a production environment: `make guard` refuses when `FLASK_ENV`, `NODE_ENV`, `APP_ENV` or `ENVIRONMENT` is `production`, and the contract forbids `FLASK_ENV`/`APP_ENV` production for a run. [gate: `make guard`; contract: `watermill.yaml` `environment`]

## Frontend (React, Vite)

- One definition of today: `utils.localDate`. Never `toISOString().slice(0,10)`, which is UTC. [doc]
- Design tokens live in `frontend/src/index.css`; components read tokens and never hard-code colors. Text meets 4.5:1 contrast in both themes. [doc]
- No emojis in anything the user reads. [doc]
- Client branding lives in `assets/branding/` and is not restyled by a task. [fence]

## Integrations

- Provider code lives in `services/integrations/`, which is fenced. A new provider module is added to the fence in the change that creates it once the fence is enumerated. [fence, doc; ADR-0001]
- A provider leaves the fence only with a wiring record in `docs/integrations/<provider>.md` and live proof. Beads that need a live provider are created `--defer`. [doc; ADR-0001]
- Mock data, not network calls, backs any skeleton built before ungating.

## Process

- Update `CLAUDE.md` in the same change that changes a table, route, config key or convention; a change is incomplete until its docs are. (`CLAUDE.md` is fenced: a human, or a bead that directs it, makes the edit.) [doc]
- Tests are written at seams (a route, a public function, a CLI command), not against private helpers. Expected values come from an independent source, not recomputed as the code does. A new test is shown failing without the change; docs-only changes say so. [doc: millstone role, ADR-0003]
- Commits use conventional-commit style, matching `git log`, and name the bead id in the PR. [doc]
- Never use `git stash` in a mill worktree; use a patch file. Never run `npm ci` in a directory other worktrees link to. [hook, ADR-0004]
- Beads: commit and push `.beads/issues.jsonl` after any `bd` write. [doc; ADR-0002]
- Terms in code, commits and docs follow `CONTEXT.md`; an architectural decision that is hard to reverse, surprising and a real trade-off gets an ADR in `docs/adr/`. [doc]

## This cell

> Fill in on stamping: naming, layout and testing rules specific to this client's domain. Delete this note when the first rule is added.
