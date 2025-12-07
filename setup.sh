#!/bin/bash

# Family Planner Setup Script

echo "================================"
echo "Family Planner Setup"
echo "================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  Please update .env with your actual configuration values!"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Run migrations
echo "Running database migrations..."
python manage.py migrate
echo "✓ Migrations applied"
echo ""

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "✓ Static files collected"
echo ""

echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Create a superuser: python manage.py createsuperuser"
echo "2. Start the development server: python manage.py runserver"
echo "3. Visit http://localhost:8000/admin to access the admin panel"
echo ""
echo "For Docker setup, run: docker-compose up --build"
echo ""
