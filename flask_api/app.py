import os
import django
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eDiary_ManagementSystem.settings')
django.setup()

# Import Django models after setup
from eDiary.models import Signup, Category, Notes, Noteshistory
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Authentication decorator
def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            # Here you would validate the token
            # For now, we'll just check if it exists
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401
    return decorated

# User Management
@app.route('/api/auth/signup/', methods=['POST'])
def signup():
    data = request.get_json()
    try:
        # Create Django User
        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data.get('email', ''),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        
        # Create Signup record
        signup = Signup.objects.create(
            user=user,
            mobileNumber=data.get('mobileNumber', '')
        )
        
        return jsonify({
            'message': 'User created successfully',
            'user_id': user.id,
            'signup_id': signup.id
        }), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/api/auth/login/', methods=['POST'])
def login():
    data = request.get_json()
    user = authenticate(username=data['username'], password=data['password'])
    if user:
        # In a real application, you would generate a JWT token here
        return jsonify({
            'message': 'Login successful',
            'user_id': user.id,
            'username': user.username
        })
    return jsonify({'message': 'Invalid credentials'}), 401

# Category Management
@app.route('/api/categories/', methods=['GET'])
@token_required
def get_categories():
    categories = Category.objects.all()
    return jsonify([{
        'id': category.id,
        'name': category.categoryName,
        'created_at': category.CreationDate,
        'user': category.signup.user.username
    } for category in categories])

@app.route('/api/categories/', methods=['POST'])
@token_required
def create_category():
    data = request.get_json()
    try:
        signup = Signup.objects.get(user_id=data['user_id'])
        category = Category.objects.create(
            signup=signup,
            categoryName=data['name']
        )
        return jsonify({
            'id': category.id,
            'name': category.categoryName,
            'created_at': category.CreationDate
        }), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Notes Management
@app.route('/api/notes/', methods=['GET'])
@token_required
def get_notes():
    notes = Notes.objects.all()
    return jsonify([{
        'id': note.id,
        'title': note.noteTitle,
        'description': note.noteDescription,
        'category': note.category.categoryName,
        'created_at': note.CreationDate,
        'user': note.signup.user.username
    } for note in notes])

@app.route('/api/notes/', methods=['POST'])
@token_required
def create_note():
    data = request.get_json()
    try:
        signup = Signup.objects.get(user_id=data['user_id'])
        category = Category.objects.get(id=data['category_id'])
        note = Notes.objects.create(
            signup=signup,
            category=category,
            noteTitle=data['title'],
            noteDescription=data['description']
        )
        return jsonify({
            'id': note.id,
            'title': note.noteTitle,
            'description': note.noteDescription,
            'category': note.category.categoryName,
            'created_at': note.CreationDate
        }), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Notes History
@app.route('/api/notes/<int:note_id>/history/', methods=['GET'])
@token_required
def get_note_history(note_id):
    history = Noteshistory.objects.filter(note_id=note_id)
    return jsonify([{
        'id': entry.id,
        'details': entry.noteDetails,
        'created_at': entry.postingDate,
        'user': entry.signup.user.username
    } for entry in history])

@app.route('/api/notes/<int:note_id>/history/', methods=['POST'])
@token_required
def add_note_history(note_id):
    data = request.get_json()
    try:
        note = Notes.objects.get(id=note_id)
        signup = Signup.objects.get(user_id=data['user_id'])
        history = Noteshistory.objects.create(
            note=note,
            signup=signup,
            noteDetails=data['details']
        )
        return jsonify({
            'id': history.id,
            'details': history.noteDetails,
            'created_at': history.postingDate
        }), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000) 