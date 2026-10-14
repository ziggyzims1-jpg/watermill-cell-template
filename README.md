# Water Mill cell template

The starting point for every new Water Mill cell, so cell N+1 starts where
zimmy-life-tracker ended, not where it began. A cell stamped from this repo
has, on day one:

- Flask + SQLite backend with the SCHEMA / append-only MIGRATIONS discipline
  (`db.py` — read its docstring before touching it)
- Vite + React frontend built to `static/dist/`, design tokens in
  `frontend/src/index.css`, one `localDate` and one `clock.today()`
- A `make verify` merge gate (guard, build, ruff, ESLint at
  `--max-warnings=0`, Vitest, pytest) mirrored **exactly** by CI
- An in-repo `watermill.yaml` contract with night-one caps and a fence that
  gates integrations by default (`docs/integrations/README.md`)
- An APScheduler skeleton whose jobs record every run in `job_runs`

## Stamping a new cell

Repo naming: `<project>-cell-<cell#>`.

1. `gh repo create <owner>/<project>-cell-<n> --template <owner>/watermill-cell-template --private --clone`
   (or clone this repo and re-init git).
2. Find and replace `watermill-cell-template` (config.py `APP_NAME`,
   `watermill.yaml` `name`, `frontend/index.html` title, this README).
3. Drop the client's logo in `assets/branding/` and set `--brand-primary` /
   `--brand-accent` in `frontend/src/index.css`.
4. `make install && make verify` — must be green before anything else.
5. `bd init`, file the cell's beads. Beads needing a live external provider
   are created `--defer` (see `docs/integrations/README.md`).
6. Rewrite `CLAUDE.md`'s project sections for the client's domain. The
   conventions section stays. Fill in the "this cell" sections of
   `CONTEXT.md` and `CODING_STANDARDS.md`; `docs/adr/` ADR-0001 to 0006 are
   inherited, the cell's own decisions start at ADR-0007.
7. Push, confirm CI is green, and only then point the mill at it —
   supervised first; caps rise after a clean night.

## The gate

`make verify` is the merge gate; `make help` lists everything. CI runs
exactly `make verify` and nothing else, so local and CI cannot diverge.

## Integrations

Gated by default, ungated per provider by human proof plus a wiring record.
Policy: `water-mill/docs/policies/INTEGRATIONS.md`; procedure and record template:
`docs/integrations/`.

## Shared language, decisions and standards

`CONTEXT.md` (glossary), `docs/adr/` (decisions every cell inherits) and
`CODING_STANDARDS.md` (what the gate, the fence and `CLAUDE.md` already
require) are what the bolter reviewer checks a PR against.
