
from flask import Flask
from controllers.home_controller import home_bp, init_jwt
from models.user_model import init_db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Initialize database
    init_db()

    # Initialize JWT
    jwt = init_jwt(app)

    # Register blueprints
    app.register_blueprint(home_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)