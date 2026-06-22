import os
from flask import Flask, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from config import config

db = SQLAlchemy()
jwt = JWTManager()

FRONTEND_DIST = os.path.join(os.path.dirname(__file__), "frontend_dist")


def create_app(env="default"):
    app = Flask(__name__, static_folder=None)
    app.config.from_object(config[env])

    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from routes.auth import auth_bp
    from routes.freezers import freezers_bp
    from routes.compartments import compartments_bp
    from routes.items import items_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(freezers_bp, url_prefix="/api/freezers")
    app.register_blueprint(compartments_bp, url_prefix="/api/compartments")
    app.register_blueprint(items_bp, url_prefix="/api/items")

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        if path and os.path.exists(os.path.join(FRONTEND_DIST, path)):
            return send_from_directory(FRONTEND_DIST, path)
        return send_file(os.path.join(FRONTEND_DIST, "index.html"))

    with app.app_context():
        db.create_all()

    return app
