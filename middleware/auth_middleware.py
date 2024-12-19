from flask import request, jsonify

def auth_middleware(app):
    @app.before_request
    def check_authentication():
        # Simulate token check (replace with actual logic)
        token = request.headers.get("Authorization")
        if not token or token != "valid-token":
            return jsonify({"error": "Unauthorized"}), 401
