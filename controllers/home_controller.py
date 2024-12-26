
from flask import Blueprint, request, jsonify, send_file, render_template, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models.user_model import User, Library, Book
import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import blue
import asyncio
from pyppeteer import launch
import pdfkit

home_bp = Blueprint('home', __name__)


# Initialize JWT
def init_jwt(app):
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    jwt = JWTManager(app)
    return jwt

@home_bp.route('/')
def home():
    return jsonify({"message": "Welcome to the home page"})

@home_bp.route('/index')
def index():
    return render_template('index.html')

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

@home_bp.route('/generate_pdf', methods=['GET', 'POST'])
@jwt_required()
def generate_pdf():
    if request.method == 'POST':
        data = request.form
        name = data.get('name')
        paragraph = data.get('paragraph')
        rendered = render_template('temp.html', name=name, paragraph=paragraph)
        pdf = pdfkit.from_string(rendered, False)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
        return response
    return render_template('form.html')


"""
@home_bp.route('/generate_pdf', methods=['POST'])
@jwt_required()
async def generate_pdf():
    html_content = render_template('temp.html',message="JOIN US TO WATCH ONE PIECE")
    pdf_bytes = await html_to_pdf(html_content)
    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response

async def html_to_pdf(html_content):
    browser = await launch()
    page = await browser.newPage()
    await page.setContent(html_content)
    pdf_bytes = await page.pdf({
        'format': 'A4',
        'printBackground': True
    })
    await browser.close()
    return pdf_bytes
    


@home_bp.route('/generate_pdf', methods=['GET'])
@jwt_required()
def generate_pdf():
    if request.method == 'POST':
        data = request.form
        name = data.get('name')
        paragraph = data.get('paragraph')
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        p.drawString(100, height - 100, f"Name: {name}")
        p.drawString(100, height - 150, "Paragraph:")
        p.drawString(100, height - 200, paragraph)
        
        p.setFillColor(blue)
        p.linkURL("http://127.0.0.1:5000/index.html", (100, height - 250, 200, height - 300), thickness=1, color=blue,relative=1)
        p.drawString(100, height - 250, "Click here to visit our website")
        p.linkURL("https://corp.toei-anim.co.jp/en/index.html", (100, height - 250, 300, height - 240), relative=0)
        p.showPage()
        p.save()
        

        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='output.pdf', mimetype='application/pdf')
    return render_template('form.html')
"""

