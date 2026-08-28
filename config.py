"""App configuration.

DATA_DIR is the isolation seam the gate depends on: `make guard` sets it to a
sentinel and refuses to run if this module reports anything else, and the test
suite is handed a throwaway directory through it. Everything that touches disk
(the database, the secret key) must derive its path from DATA_DIR — a path
built any other way escapes the tests' sandbox.
"""

import os
import secrets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATA_DIR") or os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "app.db")
STATIC_DIST = os.path.join(BASE_DIR, "static", "dist")

PORT = int(os.environ.get("PORT", "5000"))

APP_NAME = "watermill-cell-template"

with open(os.path.join(BASE_DIR, "VERSION")) as _f:
    APP_VERSION = _f.read().strip()


def load_secret_key():
    """Persist the Flask session key under DATA_DIR so sessions survive restarts."""
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, "secret_key")
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    key = secrets.token_hex(32)
    with open(path, "w") as f:
        f.write(key)
    os.chmod(path, 0o600)
    return key
