from flask import Flask
from models.user_model import db
from controllers.home_controller import home_bp
from middleware.auth_middleware import auth_middleware


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create database tables for our data models

    # Register middleware
    auth_middleware(app)

    # Register blueprints
    app.register_blueprint(home_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
