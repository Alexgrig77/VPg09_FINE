# Промпт 13: Docker

**Этап:** 7.1 Docker  
**Среда:** [ЛОКАЛЬНО]

## Контекст

Приложение работает локально. Нужен Docker для деплоя.

## Задача

Dockerfile, docker-compose.yml, healthcheck /api/test.

## Критерии приёмки

- docker-compose up — приложение на localhost:5000
- curl localhost:5000/api/test возвращает OK

## Текст промпта

```
Добавь Docker для FISH-MVP:

1. Dockerfile:
   - FROM python:3.11-slim
   - WORKDIR /app
   - COPY requirements.txt
   - RUN pip install --no-cache-dir -r requirements.txt
   - COPY .
   - EXPOSE 5000
   - CMD ["python", "app.py"] или gunicorn если добавлен
   - Создай data/ для volume

2. docker-compose.yml:
   - service fish-app: build ., ports 5000:5000
   - volumes: ./data:/app/data
   - environment: SECRET_KEY, FLASK_ENV=production, DATABASE_PATH=/app/data/FISH.db
   - healthcheck: curl -f http://localhost:5000/api/test

3. Добавь эндпоинт GET /api/test — возвращает {"status": "ok"} (без авторизации для healthcheck)

4. .dockerignore — venv, __pycache__, .git, *.db, .env
"""
