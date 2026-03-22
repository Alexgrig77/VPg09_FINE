# Промпт 14: GitHub Actions Docker

**Этап:** 7.2 CI Docker  
**Среда:** [ЛОКАЛЬНО]

## Контекст

Docker есть. Нужен workflow сборки образа при push.

## Задача

.github/workflows/docker-build.yml — build, run, curl /api/test.

## Критерии приёмки

- Push в main собирает образ
- Контейнер запускается, healthcheck проходит

## Текст промпта

```
Добавь GitHub Actions для Docker FISH-MVP:

Файл .github/workflows/docker-build.yml:
- Триггер: push на main, master
- Шаги: checkout, Docker Buildx, docker build -t fish-mvp:test .
- Запустить контейнер: docker run -d -p 5000:5000 -e SECRET_KEY=test -e DATABASE_PATH=/app/data/FISH.db fish-mvp:test
- Подождать 10 сек, curl -f http://localhost:5000/api/test
- Остановить контейнер

Опционально: создание data/ и init_db перед запуском, или использовать in-memory для теста.
"""
