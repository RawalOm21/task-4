
from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models.user_model import User, Library, Book
import datetime

home_bp = Blueprint('home', __name__)

# Initialize JWT
def init_jwt(app):
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    jwt = JWTManager(app)
    return jwt

@home_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.get_by_username(username)
    if user and user['password'] == password:  # Replace with hashed password check
        access_token = create_access_token(identity=user['username'], expires_delta=datetime.timedelta(minutes=30))
        return jsonify({"token": access_token})
    return jsonify({"error": "Invalid credentials"}), 401

@home_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = User.create(username=data['username'], email=data['email'], password=data['password'])
    return jsonify({"message": "User created successfully", "user_id": user_id}), 201

@home_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.get_all()
    return jsonify([{"id": user['id'], "username": user['username'], "email": user['email']} for user in users])

@home_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    User.update(user_id, username=data.get('username'), email=data.get('email'))
    return jsonify({"message": "User updated successfully"})

@home_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    User.delete(user_id)
    return jsonify({"message": "User deleted successfully"})

@home_bp.route('/books', methods=['POST'])
@jwt_required()
def create_book():
    data = request.get_json()
    book_id = Book.create(title=data['title'], author=data['author'], library_id=data['library_id'])
    return jsonify({"message": "Book created successfully", "book_id": book_id}), 201

@home_bp.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    books = Book.get_all()
    return jsonify([{"id": book['id'], "title": book['title'], "author": book['author'], "library_id": book['library_id']} for book in books])

@home_bp.route('/books/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    data = request.get_json()
    Book.update(book_id, title=data.get('title'), author=data.get('author'))
    return jsonify({"message": "Book updated successfully"})

@home_bp.route('/books/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    Book.delete(book_id)
    return jsonify({"message": "Book deleted successfully"})

"""from flask import Blueprint, request, jsonify, current_app
from models.user_model import db, User, Library, Book
import jwt
import datetime
from functools import wraps

home_bp = Blueprint('home', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(username=data['user']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@home_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:  # Replace with hashed password check
        token = jwt.encode({
            'user': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401

@home_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'], password=data['password'])  # Add password field
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@home_bp.route('/users', methods=['GET'])
@token_required
def get_users(current_user):
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users])

@home_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({"message": "User updated successfully"})

@home_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

@home_bp.route('/books', methods=['POST'])
@token_required
def create_book(current_user):
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], library_id=data['library_id'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book created successfully"}), 201

@home_bp.route('/books', methods=['GET'])
@token_required
def get_books(current_user):
    books = Book.query.all()
    return jsonify([{"id": book.id, "title": book.title, "author": book.author, "library_id": book.library_id} for book in books])

@home_bp.route('/books/<int:book_id>', methods=['PUT'])
@token_required
def update_book(current_user, book_id):
    data = request.get_json()
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    db.session.commit()
    return jsonify({"message": "Book updated successfully"})

@home_bp.route('/books/<int:book_id>', methods=['DELETE'])
@token_required
def delete_book(current_user, book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"})"""