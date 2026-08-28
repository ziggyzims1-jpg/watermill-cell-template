"""Flask entrypoint. Serves the built frontend from static/dist and the API
under /api. Keep route registration here; feature blueprints go in routes/."""

from flask import Flask, jsonify, send_from_directory

import config
import db


def create_app():
    app = Flask(__name__, static_folder=None)
    app.secret_key = config.load_secret_key()
    db.init_db()

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "app": config.APP_NAME})

    @app.get("/api/version")
    def version():
        return jsonify({"version": config.APP_VERSION})

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def frontend(path):
        import os

        full = os.path.join(config.STATIC_DIST, path)
        if path and os.path.isfile(full):
            return send_from_directory(config.STATIC_DIST, path)
        return send_from_directory(config.STATIC_DIST, "index.html")

    return app


if __name__ == "__main__":
    application = create_app()
    import scheduler

    scheduler.start()
    application.run(host="0.0.0.0", port=config.PORT)
