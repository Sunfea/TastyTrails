#!/bin/bash
# This script handles starting the application with the correct port for Railway

if [ -z "$PORT" ]; then
  # Default to port 8000 if PORT is not set (for local development)
  PORT=8000
fi

echo "Starting application on port $PORT"
exec gunicorn tastytrails.wsgi:application --bind 0.0.0.0:$PORT