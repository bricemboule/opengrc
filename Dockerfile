# ─────────────────────────────────────────
# Stage 1 : Build du frontend React
# ─────────────────────────────────────────
FROM node:22-alpine AS frontend-build

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# ─────────────────────────────────────────
# Stage 2 : Image finale (backend + frontend + nginx + supervisord)
# ─────────────────────────────────────────
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings.production

# Dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Dépendances Python
WORKDIR /app
COPY backend/requirements /app/requirements
RUN pip install --upgrade pip && pip install -r requirements/prod.txt

# Code backend
COPY backend/ /app/

# Frontend buildé
COPY --from=frontend-build /app/frontend/dist /usr/share/nginx/html

# Config nginx
COPY nginx-app.conf /etc/nginx/conf.d/default.conf
RUN rm -f /etc/nginx/sites-enabled/default

# Config supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Entrypoint
COPY docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
