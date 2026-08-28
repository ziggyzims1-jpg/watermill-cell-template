"""APScheduler skeleton. Jobs record every run in job_runs so a job that stops
running is visible — silence is the failure mode, so anything scheduled here
must write its outcome where a dashboard (or a human) can see it go stale."""

from datetime import datetime, UTC

from apscheduler.schedulers.background import BackgroundScheduler

import db

_scheduler = None


def _record(job_name, fn):
    started = datetime.now(UTC).isoformat()
    outcome = "ok"
    try:
        fn()
    except Exception as exc:  # noqa: BLE001 — a job must never kill the scheduler
        outcome = f"error: {exc}"
    conn = db.get_db()
    conn.execute(
        "INSERT INTO job_runs (job_name, started_at, finished_at, outcome) VALUES (?, ?, ?, ?)",
        (job_name, started, datetime.now(UTC).isoformat(), outcome),
    )
    conn.commit()
    conn.close()


def heartbeat():
    """Demo job: proves the scheduler runs and the registry records it."""


def start():
    global _scheduler
    if _scheduler is not None:
        return _scheduler
    _scheduler = BackgroundScheduler()
    _scheduler.add_job(lambda: _record("heartbeat", heartbeat), "interval", hours=1)
    _scheduler.start()
    return _scheduler
