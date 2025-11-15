# Railway Deployment Guide

This guide explains how to deploy the TastyTrails application to Railway.

## Prerequisites

1. A Railway account (https://railway.app)
2. A PostgreSQL database service on Railway
3. A Redis service on Railway (optional, for Celery)

## Deployment Steps

### 1. Create a New Project on Railway

1. Go to https://railway.app/new
2. Select "Deploy from GitHub repo"
3. Connect your GitHub account and select this repository

### 2. Configure Environment Variables

Set the following environment variables in your Railway project:

```bash
# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-railway-app-url.railway.app,localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@host:port/database

# Redis settings (if using Celery)
REDIS_URL=redis://user:password@host:port/database

# CORS settings
CORS_ALLOWED_ORIGINS=https://your-frontend-url.com,http://localhost:3000
```

### 3. Configure Services

The application consists of multiple services:

1. **Main Django Web Service** - Uses `Dockerfile.railway`
2. **FastAPI Service** - Uses `Dockerfile.fastapi.railway` (optional)
3. **PostgreSQL Database** - Provided by Railway
4. **Redis** - Provided by Railway (optional)

### 4. Deploy Commands

Railway will automatically use the appropriate Dockerfile based on your configuration.

For the main Django service:
```bash
gunicorn tastytrails.wsgi:application --bind 0.0.0.0:$PORT
```

For the FastAPI service:
```bash
uvicorn fastapi_app:app --host 0.0.0.0 --port $PORT
```

### 5. Post-Deployment Steps

1. Run migrations:
   ```bash
   railway run python manage.py migrate
   ```

2. Create a superuser (optional):
   ```bash
   railway run python manage.py createsuperuser
   ```

3. Collect static files:
   ```bash
   railway run python manage.py collectstatic --noinput
   ```

## Health Checks

The application includes health check endpoints:

- Django: `/health/`
- FastAPI: `/health`

Railway will automatically use these for health checks.

## Scaling

Railway automatically scales your application based on traffic. You can manually configure scaling settings in the Railway dashboard.

## Monitoring

Railway provides built-in logging and monitoring. You can view logs in the Railway dashboard or using the CLI:

```bash
railway logs
```