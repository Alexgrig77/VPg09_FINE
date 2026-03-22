# Промпт 15: Деплой на сервер

**Этап:** 7.3 Деплой  
**Среда:** [СЕРВЕР]

## Контекст

Docker работает локально. Пользователь имеет сервер с SSH. Нужна инструкция/скрипт деплоя.

## Задача

docs/DEPLOYMENT.md — полная инструкция: clone, .env, docker-compose up, nginx (опционально).

## Критерии приёмки

- Чёткие шаги для деплоя
- Указаны переменные окружения
- Инструкция по первому запуску (init_db внутри контейнера)

## Текст промпта

```
Дополни docs/DEPLOYMENT.md разделом «Деплой на VPS/сервер»:

1. Требования: Docker, Docker Compose на сервере
2. Шаги (каждая команда отдельно):
   - git clone <URL-репозитория>
   - cd VPg09_FINE
   - cp .env.example .env
   - Отредактировать .env: SECRET_KEY (сгенерировать), FLASK_ENV=production
   - Создать data/
   - docker-compose build
   - docker-compose run --rm fish-app python scripts/init_db.py
   - docker-compose up -d
3. Проверка: curl http://localhost:5000/api/test
4. Опционально: nginx reverse proxy, HTTPS (certbot)
5. Обновление: git pull; docker-compose up -d --build

Пометь: [СЕРВЕР] — выполнять на целевой машине.
"""
