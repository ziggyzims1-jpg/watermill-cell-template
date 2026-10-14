# SCHEMA plus append-only MIGRATIONS

Status: accepted (learned in zimmy-life-tracker, carried into every cell)

`db.py` holds a `SCHEMA` for fresh databases and an append-only `MIGRATIONS` list for existing ones; both run idempotently on every start, so a deploy self-heals on pull and restart. `MIGRATIONS` is never edited or reordered. `SCHEMA` may reference only what `SCHEMA` itself creates: a new column goes in both places, but an index over it goes in `MIGRATIONS` only, after the `ALTER`. The `SCHEMA` rule exists because the failure it prevents is severe: on an existing database `CREATE TABLE IF NOT EXISTS` is a no-op, so an index in `SCHEMA` over a not-yet-added column makes `executescript` fail as one script and the app crash-loops on boot.

## Consequences

- `db.py` is on the fence; schema changes are supervised.
- Tests and the gate must keep `DATA_DIR` overridable so nothing writes beside the live database.

Sources: `db.py` module docstring; `CLAUDE.md` "Migrations are append-only"; `watermill.yaml` fence.
