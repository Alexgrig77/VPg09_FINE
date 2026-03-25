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

Ниже приведён универсальный сценарий (подойдёт для развёртывания на `4pwd.ru`).

## 1) Клонирование
1. Укажите URL вашего репозитория на GitHub:
   ```
   git clone <repo-url> VPg09_FINE
   cd VPg09_FINE
   ```

## 2) Конфигурация окружения
1. Создайте файл `.env`:
   ```
   cp .env.example .env
   ```
2. Отредактируйте `.env`:
   - `SECRET_KEY` — задайте случайную строку (например, сгенерированную python `secrets.token_hex`)
   - `FLASK_ENV=production`
3. Важно: cookie сессии в production помечается как `Secure`, поэтому HTTPS обязателен.

## 3) Первый запуск (инициализация БД)
1. Создайте папку под БД:
   ```
   mkdir -p data
   ```
2. Инициализируйте SQLite:
   ```
   docker-compose run --rm fish-app python scripts/init_db.py
   ```

## 4) Запуск контейнеров
1. Запуск:
   ```
   docker-compose up -d
   ```
2. Проверка:
   - локально на сервере:
     ```
     curl http://localhost:5000/api/test
     ```
   - если Flask поднялся — получите `{"status":"ok",...}`

## 5) Проброс на домен `4pwd.ru` (Nginx + HTTPS)

Если на сервере уже есть Nginx — достаточно добавить reverse proxy.

### 5.1 Nginx конфиг (пример)
Создайте/отредактируйте файл, например: `/etc/nginx/sites-available/vpg09_fish.mvp.conf`.
Пример (замените домен при необходимости):
```
server {
    listen 80;
    server_name 4pwd.ru www.4pwd.ru;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Включите сайт и проверьте конфиг:
```
sudo ln -s /etc/nginx/sites-available/vpg09_fish.mvp.conf /etc/nginx/sites-enabled/ || true
sudo nginx -t
sudo systemctl reload nginx
```

### 5.2 HTTPS через Let’s Encrypt (Certbot)
Если Nginx уже работает:
```
sudo apt-get update
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d 4pwd.ru -d www.4pwd.ru
```

После этого приложение будет доступно по `https://4pwd.ru`.

## 6) Обновление кода
После пуша в GitHub:
```
git pull origin <branch>
docker-compose up -d --build
```

Если изменялась только фронтенд-часть — `--build` обычно достаточно, и повторная инициализация БД не требуется.
