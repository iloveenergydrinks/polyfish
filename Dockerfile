FROM node:20-bookworm-slim AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build


FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    FLASK_DEBUG=false \
    PORT=8080

WORKDIR /app

COPY backend/requirements.txt ./backend/requirements.txt

RUN pip install --upgrade pip \
    && pip install -r backend/requirements.txt

COPY backend/ ./backend/
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

RUN mkdir -p /app/backend/uploads/reports /app/backend/uploads/simulations

EXPOSE 8080

CMD ["sh", "-c", "gunicorn --workers=${GUNICORN_WORKERS:-2} --threads=${GUNICORN_THREADS:-4} --timeout=${GUNICORN_TIMEOUT:-300} --bind 0.0.0.0:${PORT} backend.wsgi:app"]
