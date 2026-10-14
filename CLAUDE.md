# <Cell name — rewrite on stamping>

> Keep this file up to date: whenever you change the project — a table, a
> route, a config key, a convention — update this file in the same change.
> Treat a change as incomplete until its docs are updated.

# Goal

<What this cell is for, who the client is, what the app does. Rewrite.>

# Architecture

Python/Flask backend + React (Vite) frontend built to `static/dist/` and
served by Flask. Single SQLite DB under `data/` (`DATA_DIR` overrides — the
gate and the tests depend on that override working).

| Path | Purpose |
|------|---------|
| `app.py` | Flask entrypoint; registers blueprints |
| `db.py` | `SCHEMA` DDL + append-only `MIGRATIONS`, `get_db()`, `init_db()` |
| `config.py` | Paths, port, `DATA_DIR` seam |
| `routes/` | Flask blueprints |
| `services/` | Business logic; `services/integrations/` is fenced (see below) |
| `scheduler.py` | APScheduler jobs; every run recorded in `job_runs` |
| `frontend/` | React app; design tokens in `src/index.css` |
| `tests/` | Backend suite (pytest) |
| `docs/integrations/` | Integration wiring records and the ungating procedure |
| `watermill.yaml` | The Water Mill contract for this cell |

# Conventions (every cell inherits these)

- **Migrations are append-only.** Add to the end of `MIGRATIONS`; never edit
  or reorder. `SCHEMA` may only reference what `SCHEMA` itself creates: a new
  column goes in both places, an index goes in `MIGRATIONS` only.
- **One definition of "today".** Backend: `services/clock.py`. Frontend:
  `utils.localDate`. Never `toISOString().slice(0,10)` (UTC) or a second
  local definition.
- **Verify with `make verify`.** It is the merge gate and CI runs exactly it.
  No target may swallow a failure; a step that cannot fail must not be part
  of a green result.
- **Design tokens live in `frontend/src/index.css`.** Components read tokens,
  never hardcode colors. 4.5:1 contrast in both themes. No emojis in
  anything the user reads.
- **Never send secrets to the client.** Secret config keys are write-only in
  any settings UI and redacted from any config read endpoint.
- **Integrations are gated by default.** `services/integrations/` is on the
  fence in `watermill.yaml`; beads needing a live provider are created
  deferred. A provider is ungated only through the procedure in
  `docs/integrations/README.md`: a human wires it, proves it live, files the
  wiring record, and narrows the fence in the same PR.
- **Scheduled jobs must be visible in failure.** Every job records its run
  and outcome in `job_runs`; a job whose success is invisible needs a
  heartbeat and something that alerts when the heartbeat goes stale.

## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Use `bd` for ALL task
tracking; run `bd prime` for workflow context. Do not commit, push, or sync
unless explicitly asked.
__Override: after any bead write, commit and push .beads/issues.jsonl (workshop rule 2026-09-03). In the cloud, never bd dolt push.__
