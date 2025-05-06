# eDiary Management System

A web application that combines Django front-end with Flask RESTful APIs for diary management.

## Features

- Django-based web interface
- Flask RESTful APIs
- User authentication
- Note management with categories
- Note history tracking
- Database management using Django ORM

## Setup Instructions

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run Django migrations:
```bash
python manage.py migrate
```

4. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

## Running the Application

1. Start the Django development server:
```bash
python manage.py runserver
```

2. In a separate terminal, start the Flask API server:
```bash
python flask_api/app.py
```

The Django application will be available at http://localhost:8000
The Flask API will be available at http://localhost:5000

## API Endpoints

### Authentication
- POST /api/auth/signup/ - Register new user
- POST /api/auth/login/ - User login

### Categories
- GET /api/categories/ - List all categories
- POST /api/categories/ - Create new category

### Notes
- GET /api/notes/ - List all notes
- POST /api/notes/ - Create new note
- GET /api/notes/<id>/history/ - Get note history
- POST /api/notes/<id>/history/ - Add note history entry

## API Usage Examples

### User Registration
```json
POST /api/auth/signup/
{
    "username": "user123",
    "password": "securepass",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "mobileNumber": "1234567890"
}
```

### Create Category
```json
POST /api/categories/
{
    "user_id": 1,
    "name": "Work"
}
```

### Create Note
```json
POST /api/notes/
{
    "user_id": 1,
    "category_id": 1,
    "title": "Meeting Notes",
    "description": "Discussion points from team meeting"
}
```

### Add Note History
```json
POST /api/notes/1/history/
{
    "user_id": 1,
    "details": "Updated meeting notes with action items"
}
```

## Deployment

For production deployment:

1. Set DEBUG=False in settings.py
2. Configure ALLOWED_HOSTS
3. Set up a production database
4. Use Gunicorn for Django:
```bash
gunicorn eDiary_ManagementSystem.wsgi:application
```
5. Use Waitress for Flask:
```bash
waitress-serve --port=5000 flask_api.app:app
```

## Security Notes

- Keep SECRET_KEY secure
- Use environment variables for sensitive data
- Enable HTTPS in production
- Implement proper token validation 