#!/bin/bash

# Kidoo Preschool Production Deployment Script
set -e

echo "🚀 Starting Kidoo Preschool Production Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env.production exists
if [ ! -f "backend/.env.production" ]; then
    print_error ".env.production file not found!"
    print_warning "Please copy env.production.example to .env.production and configure it."
    exit 1
fi

# Load environment variables
export $(cat backend/.env.production | grep -v '^#' | xargs)

print_status "Environment variables loaded"

# Build frontend
print_status "Building frontend..."
cd frontend
npm ci --only=production
npm run build:prod
cd ..

# Build and deploy with Docker
print_status "Building Docker image..."
docker-compose -f docker-compose.production.yml build

print_status "Stopping existing containers..."
docker-compose -f docker-compose.production.yml down

print_status "Starting production containers..."
docker-compose -f docker-compose.production.yml up -d

# Wait for database to be ready
print_status "Waiting for database to be ready..."
sleep 10

# Run migrations
print_status "Running database migrations..."
docker-compose -f docker-compose.production.yml exec web python manage.py migrate --settings=kidoo_preschool.settings_production

# Collect static files
print_status "Collecting static files..."
docker-compose -f docker-compose.production.yml exec web python manage.py collectstatic --noinput --settings=kidoo_preschool.settings_production

# Create superuser if it doesn't exist
print_status "Creating superuser (if not exists)..."
docker-compose -f docker-compose.production.yml exec web python manage.py shell --settings=kidoo_preschool.settings_production << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@kidoopreschool.com', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
EOF

print_status "Deployment completed successfully! 🎉"
print_warning "Don't forget to:"
print_warning "1. Change the default admin password"
print_warning "2. Configure SSL certificates"
print_warning "3. Set up monitoring and backups"
print_warning "4. Update DNS records to point to your server"
