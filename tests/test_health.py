import os
import tempfile
import unittest

# The suite must never touch a real data directory. Set DATA_DIR before any
# app import — config reads it at import time, and `make guard` proves it does.
os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="cell-test-")

import app  # noqa: E402


class HealthTest(unittest.TestCase):
    def setUp(self):
        self.client = app.create_app().test_client()

    def test_health(self):
        resp = self.client.get("/api/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["status"], "ok")

    def test_version(self):
        resp = self.client.get("/api/version")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.get_json()["version"])
