# National-3CPERS

**National-3CPERS** is a web application built with a Django REST backend and a React frontend.

The project uses PostgreSQL for data storage, Redis for caching and task queues, Celery for asynchronous processing, Django Channels for WebSockets, and Nginx as the HTTP entry point when running with Docker.

## Technology Stack

### Backend

- Python 3.12+
- Django 6
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Django Channels
- Gunicorn
- Uvicorn

### Frontend

- React 19
- Vite 8
- Redux Toolkit
- TanStack Query
- React Router
- Tailwind CSS
- Leaflet / React Leaflet
- Recharts

### Development Infrastructure

- Docker
- Docker Compose
- Nginx
- PostgreSQL 16
- Redis 7

---

# Quick Start with Docker

Using Docker is the recommended way to run National-3CPERS in development.

## Prerequisites

Install:

- Docker Desktop on Windows/macOS, or Docker Engine on Linux
- Docker Compose v2

Verify your installation:

```bash
docker --version
docker compose version
```

## 1. Clone the Project

```bash
git clone -b develop <REPOSITORY_URL> National-3CPERS
cd National-3CPERS
```

Replace `<REPOSITORY_URL>` with the actual Git repository URL.

## 2. Backend Configuration

Docker Compose uses:

```text
backend/.env
```

If this file does not exist, create `backend/.env` from:

```text
backend/.env.example
```

The development configuration expects values similar to:

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,backend

DB_NAME=relief_db
DB_USER=relief_user
DB_PASSWORD=relief_pass
DB_HOST=db
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost,http://127.0.0.1,http://localhost:5173,http://localhost:8080

ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=7

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

REDIS_URL=redis://redis:6379/1
CELERY_BROKER_URL=redis://redis:6379/2
CELERY_RESULT_BACKEND=redis://redis:6379/3
CHANNEL_REDIS_URL=redis://redis:6379/4
```

These values are intended for the Docker development environment.

They must not be reused unchanged in production.

## 3. Build and Start the Application

From the project root:

```bash
docker compose up --build -d db redis backend celery_worker flower frontend nginx
```

This starts:

- PostgreSQL
- Redis
- Django backend
- Celery worker
- Flower
- React frontend
- Nginx

Check the status of the services:

```bash
docker compose ps
```

The backend entrypoint automatically executes the following operations during startup:

```bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py seed_rbac
```

Therefore, during a normal Docker startup, you do not need to manually run `migrate` or `seed_rbac`.

## 4. Load Demo Data

Once the backend is running:

```bash
docker compose exec backend python manage.py seed_demo
```

This command loads demonstration data for several application modules and creates an administrator account.

On a fresh database:

```text
Email: admin@eden.local
Password: Password123!
```

> `seed_demo` does not reset the password if the `admin@eden.local` user already exists. These credentials therefore primarily apply to a fresh database initialization.

## 5. Open the Application

Application:

```text
http://localhost:8080
```

Swagger API documentation:

```text
http://localhost:8080/api/docs/
```

Django Admin:

```text
http://localhost:8080/admin/
```

Health check:

```text
http://localhost:8080/api/health/
```

Flower, if the service is running:

```text
http://localhost:5555
```

---

# Useful Docker Commands

Check container status:

```bash
docker compose ps
```

View backend logs:

```bash
docker compose logs -f backend
```

View frontend logs:

```bash
docker compose logs -f frontend
```

View Celery worker logs:

```bash
docker compose logs -f celery_worker
```

Stop the application:

```bash
docker compose down
```

Rebuild the images after changing dependencies:

```bash
docker compose up --build -d db redis backend celery_worker flower frontend nginx
```

To remove the containers and Docker volumes and start again with an empty PostgreSQL database:

```bash
docker compose down -v
```

> Warning: `docker compose down -v` deletes PostgreSQL data stored in Docker volumes.

---

# Celery Beat Note

The current `docker-compose.yml` also contains a `celery_beat` service.

Its current command is:

```bash
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

However, `django-celery-beat` is not currently declared as a Python dependency in the project.

For this reason, the recommended Docker startup command above intentionally does not start the `celery_beat` service.

Celery tasks executed through the worker remain available.

Periodic tasks that depend on Celery Beat should only be enabled after either:

- adding and configuring the `django-celery-beat` dependency; or
- changing the Beat scheduler used by the development environment.

---

# Local Installation Without Docker

The backend and frontend can also be run directly on the host machine.

This setup requires additional configuration.

## Prerequisites

Install:

- Python 3.12 or later
- Node.js 20.19+ or Node.js 22.12+
- PostgreSQL
- Redis

> Vite 8 requires Node.js `^20.19.0` or `>=22.12.0`.

---

# Django Backend — Local Setup

## 1. Create a Virtual Environment

From the project root:

```bash
cd backend
python -m venv .venv
```

### Linux / macOS / WSL

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
.venv\Scripts\activate.bat
```

## 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements/dev.txt
```

## 3. Configure PostgreSQL

Create a PostgreSQL database and user matching your local configuration.

The development values used by Docker are:

```text
Database: relief_db
User: relief_user
Password: relief_pass
Port: 5432
```

For a local installation, use `127.0.0.1` as the database host.

Example:

```env
DB_NAME=relief_db
DB_USER=relief_user
DB_PASSWORD=relief_pass
DB_HOST=127.0.0.1
DB_PORT=5432
```

## 4. Configure Redis

Redis must be running locally on port `6379`.

Example configuration:

```env
REDIS_URL=redis://127.0.0.1:6379/1
CELERY_BROKER_URL=redis://127.0.0.1:6379/2
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/3
CHANNEL_REDIS_URL=redis://127.0.0.1:6379/4
```

## 5. Initialize Django

From the `backend` directory:

```bash
python manage.py migrate
python manage.py seed_rbac
python manage.py seed_demo
```

## 6. Start the Backend

```bash
python manage.py runserver
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/api/docs/
```

Health check:

```text
http://127.0.0.1:8000/api/health/
```

## 7. Start the Celery Worker

In another terminal, with the Python virtual environment activated:

```bash
cd backend
celery -A config worker -l info
```

---

# React Frontend — Local Setup

The frontend uses Vite.

From the project root:

```bash
cd frontend
npm ci
```

Then start the development server:

```bash
npm run dev
```

The frontend is available by default at:

```text
http://localhost:5173
```

The file:

```text
frontend/.env
```

uses:

```env
VITE_API_URL=/api
```

During development, Vite proxies `/api` and `/ws` requests to the local backend.

The default backend target is:

```text
http://127.0.0.1:8000
```

It can be changed using:

```env
VITE_BACKEND_TARGET=http://127.0.0.1:8000
```

---

# Demo Account

After running:

```bash
python manage.py seed_demo
```

or, when using Docker:

```bash
docker compose exec backend python manage.py seed_demo
```

the following account is created on a fresh database:

```text
Email: admin@eden.local
Password: Password123!
```

The command also loads demonstration data for several areas of the application, including organizations, people, human resources, projects, and CyberGRC-related modules.

---

# Recommended Test Flow

After signing in with `admin@eden.local`:

1. Open `Organizations` and verify the existing records.
2. Create or edit an organization.
3. Open `Sites` and create a site.
4. Open `Facilities` and create a facility linked to a site.
5. Open `People` and create a person.
6. Open `Contacts` and create a contact linked to a person.
7. Open `Identities` and create an identity document.
8. Open `Projects` and create a project.
9. Open `Activities` and create an activity linked to the project.
10. Open `Tasks` and create a task linked to the activity.

---

# Backend Tests

The project uses `pytest` and `pytest-django`.

From the backend directory:

```bash
cd backend
pytest
```

Some of the tests available in the project include:

- [`backend/apps/accounts/tests/test_auth_api.py`](backend/apps/accounts/tests/test_auth_api.py)
- [`backend/apps/core/tests/test_healthcheck.py`](backend/apps/core/tests/test_healthcheck.py)
- [`backend/apps/org/tests/test_organization_api.py`](backend/apps/org/tests/test_organization_api.py)
- [`backend/apps/org/tests/test_site_facility_api.py`](backend/apps/org/tests/test_site_facility_api.py)
- [`backend/apps/people/tests.py`](backend/apps/people/tests.py)
- [`backend/apps/projects/tests/test_project_api.py`](backend/apps/projects/tests/test_project_api.py)
- [`backend/apps/projects/tests/test_activity_task_api.py`](backend/apps/projects/tests/test_activity_task_api.py)

To run a specific test file:

```bash
cd backend
pytest apps/org/tests/test_site_facility_api.py
```

---

# Project Structure

```text
National-3CPERS/
├── backend/
│   ├── apps/
│   ├── config/
│   ├── requirements/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── manage.py
│
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.js
│
├── nginx/
│   └── default.conf
│
├── docker-compose.yml
├── docker-compose.prod.yml
├── Dockerfile
└── README.md
```

---

# Development

After changing Python or Node.js dependencies, rebuild the Docker images:

```bash
docker compose up --build -d db redis backend celery_worker flower frontend nginx
```

The backend source directories are mounted into the development container, allowing developers to work directly on the local source code.

To quickly verify that the application, PostgreSQL, and Redis are working:

```text
http://localhost:8080/api/health/
```

A healthy response should indicate that the application, database, and Redis services are available.
