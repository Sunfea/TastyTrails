#!/bin/bash

# Don't wait for PostgreSQL in production (Railway handles this)
if [ "$RAILWAY_ENVIRONMENT" = "" ]; then
    # Wait for PostgreSQL to be ready (development only)
    echo "Waiting for PostgreSQL to be ready..."
    while ! pg_isready -h db -p 5432 -U tastytrails_user > /dev/null 2> /dev/null; do
        sleep 1
    done
    echo "PostgreSQL is ready!"
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist (development only)
if [ "$RAILWAY_ENVIRONMENT" = "" ]; then
    echo "Creating superuser if it doesn't exist..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123');
    print('Superuser created.');
else:
    print('Superuser already exists.');
"
fi

exec "$@"