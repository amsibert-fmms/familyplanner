# Family Planner

A personalized custom planner built with Django.

## Features

- Django 5.0 with Django REST Framework
- PostgreSQL database support
- Docker and Docker Compose setup
- Whitenoise for static file serving
- CORS and CSRF configuration
- Media file upload handling
- Environment-based configuration (dev/staging/prod)
- Pre-configured apps: accounts, visibility, locations, tasks

## Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/amsibert-fmms/familyplanner.git
cd familyplanner
```

2. Create a `.env` file from the example:
```bash
cp .env.example .env
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

4. Run migrations (in a new terminal):
```bash
docker-compose exec web python manage.py migrate
```

5. Create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

6. Access the application:
- Web: http://localhost:8000
- Admin: http://localhost:8000/admin

### Local Development (Without Docker)

1. Clone the repository:
```bash
git clone https://github.com/amsibert-fmms/familyplanner.git
cd familyplanner
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example:
```bash
cp .env.example .env
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Collect static files:
```bash
python manage.py collectstatic --noinput
```

8. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
familyplanner/
├── accounts/           # User accounts and authentication
├── visibility/         # Visibility and permissions management
├── locations/          # Location management
├── tasks/              # Task management
├── familyplanner/      # Main project settings
├── media/              # User uploaded files
├── staticfiles/        # Collected static files
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
└── manage.py           # Django management script
```

## Planning Documentation

Roadmap, data-model plans, and enrichment strategies live under [`docs/planning`](./docs/planning/README.md) for easy navigation.

## Environment Variables

Key environment variables (see `.env.example` for full list):

- `SECRET_KEY`: Django secret key (change in production!)
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DB_*`: Database configuration
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins

## Apps

### accounts
User accounts and authentication management.

### visibility
Visibility and permission controls for family members.

### locations
Location and place management.

### tasks
Task and reminder management.

## Technology Stack

- **Backend**: Django 5.0
- **API**: Django REST Framework
- **Database**: PostgreSQL (with SQLite fallback for development)
- **Static Files**: Whitenoise
- **WSGI Server**: Gunicorn
- **Containerization**: Docker & Docker Compose

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
```

### Applying Migrations
```bash
python manage.py migrate
```

## License

This project is private and proprietary.
