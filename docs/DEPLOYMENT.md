# Руководство по развёртыванию FISH-MVP

## Подключение к GitHub [ЛОКАЛЬНО]

После создания репозитория на GitHub выполните:

```
git remote add origin <URL-репозитория>
git branch -M main
git push -u origin main
```

## Деплой на VPS/сервер [СЕРВЕР]

### Требования

- Docker и Docker Compose на сервере
- Git

### Шаги

1. Клонирование:
   ```
   git clone <repo-url> fish-mvp
   cd fish-mvp
   ```

2. Конфигурация:
   ```
   cp .env.example .env
   # Отредактировать .env: SECRET_KEY (сгенерировать), FLASK_ENV=production
   ```

3. Первый запуск (инициализация БД):
   ```
   mkdir -p data
   docker-compose run --rm fish-app python scripts/init_db.py
   ```

4. Запуск:
   ```
   docker-compose up -d
   ```

5. Проверка: `curl http://localhost:5000/api/test`

### Обновление

```
git pull origin main
docker-compose up -d --build
```
