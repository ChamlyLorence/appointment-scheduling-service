from flask import Flask
from app.models import db
from app.routes import routes

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:postgres@ec2-54-81-109-229.compute-1.amazonaws.com:5432/meditrack"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "your_secret_key"

    db.init_app(app)
    app.register_blueprint(routes , url_prefix='/appointment-scheduling-service/')
    return app
