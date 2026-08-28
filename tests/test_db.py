import os
import tempfile
import unittest

os.environ.setdefault("DATA_DIR", tempfile.mkdtemp(prefix="cell-test-"))

import db  # noqa: E402


class DbTest(unittest.TestCase):
    def test_init_is_idempotent(self):
        # SCHEMA and MIGRATIONS both run on every start; running twice must
        # be a no-op, or deploys stop self-healing.
        db.init_db()
        db.init_db()
        conn = db.get_db()
        tables = {
            r["name"]
            for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        conn.close()
        self.assertLessEqual({"users", "app_config", "job_runs"}, tables)

    def test_no_bare_index_in_schema(self):
        # An index belongs in MIGRATIONS, not SCHEMA: on an existing database
        # SCHEMA's CREATE TABLE is a no-op, so an index over a migrated column
        # crash-loops the deploy. This is the one deploy-breaking bug in
        # zimmy-life-tracker's history; the template pins the rule.
        self.assertNotIn("CREATE INDEX", db.SCHEMA.upper())
