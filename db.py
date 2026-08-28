"""Database: SCHEMA + append-only MIGRATIONS.

Two rules, both learned the hard way in zimmy-life-tracker and carried into
every cell:

1. MIGRATIONS is append-only. Add to the end; never edit or reorder existing
   entries. Both SCHEMA and MIGRATIONS run idempotently on every start, so
   deploys self-heal on pull + restart.

2. SCHEMA may only reference what SCHEMA itself is guaranteed to create. A new
   column goes in BOTH places — in the CREATE TABLE for a fresh database and
   as an ALTER TABLE in MIGRATIONS for an existing one — but an index over
   that column goes in MIGRATIONS ONLY, after the ALTER. On an existing
   database every CREATE TABLE IF NOT EXISTS is a no-op, so at the moment
   SCHEMA runs the new column does not exist yet; and unlike the MIGRATIONS
   loop, which tolerates each statement failing, executescript is one script —
   a single bad statement crash-loops the app on boot.
"""

import sqlite3
import os

import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'employee',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS app_config (
    key TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS job_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_name TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    outcome TEXT
);
"""

# Append-only. Each entry runs on every start inside a try/except so an
# already-applied statement is a no-op.
MIGRATIONS = [
    "CREATE INDEX IF NOT EXISTS idx_job_runs_name ON job_runs(job_name, started_at)",
]


def get_db():
    os.makedirs(config.DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript(SCHEMA)
    for stmt in MIGRATIONS:
        try:
            conn.execute(stmt)
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()
