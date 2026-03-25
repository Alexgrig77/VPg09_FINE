# FISH-MVP

База разрешений на рыболовство — учёт разрешений, видов рыбы и выловов.

## Описание

Веб-приложение для малых рыболовных хозяйств: учёт разрешений на промысел, справочник рыбы, учёт выловов, статистика и экспорт в CSV.

## Стек

- Python 3.8+
- Flask
- SQLite
- HTML, CSS, JavaScript

## Запуск

```powershell
# 0. Создайте файл .env
#    - Скопируйте: cp .env.example .env
#    - Задайте минимум:
#        SECRET_KEY (случайная строка)
#        FLASK_ENV (development | production | testing)
#    - DATABASE_PATH — путь к SQLite БД (обычно оставьте как есть)

# 1. Установка зависимостей
pip install -r requirements.txt

# 2. Инициализация БД
python scripts/init_db.py

# 3. Запуск приложения
python app.py
```

Приложение: http://localhost:5000

**Данные для входа:** admin / admin123

## API

| Метод | URL | Описание |
|-------|-----|----------|
| POST | /api/auth/login | Вход |
| POST | /api/auth/logout | Выход |
| GET | /api/test | Проверка (без авторизации) |
| GET | /api/admin/responsibles | Список ответственных (для создания сотрудников админом) |
| GET | /api/admin/users | Список сотрудников (без admin) |
| POST | /api/admin/users | Создание сотрудника (role=user) |
| PUT | /api/admin/users/<id>/password | Смена пароля сотрудника |
| PUT | /api/admin/users/<id>/status | Включить/отключить сотрудника |
| GET/POST | /api/permissions | Список / создание разрешений |
| GET/PUT/DELETE | /api/permissions/\<id\> | Разрешение по id |
| GET/POST | /api/fish | Список / создание рыбы |
| GET/PUT/DELETE | /api/fish/\<id\> | Рыба по id |
| GET/POST | /api/catches | Список / создание выловов |
| GET/PUT/DELETE | /api/catches/\<id\> | Вылов по id |
| GET | /api/statistics | Статистика |
| GET | /api/export-catches | Экспорт CSV |
| GET | /api/permission-numbers | Список номеров разрешений |
| GET | /api/fish-names | Список названий рыбы (справочник) |
| GET | /api/fish-names?permission=\<Номер_разрешения\> | Список рыбы по группе выбранного разрешения (для формы `catches.html`) |

## Права пользователей (MVP)

- Администратор (`role=admin`) видит все данные и управляет сотрудниками на странице `/admin-users.html`.
- Сотрудник (`role=user`) видит только те разрешения, где `Разрешения.Ответственный == full_name`.
- Сотрудник добавляет вылов только по своим разрешениям (серверная проверка в API).

## Скриншоты

См. [docs/screenshots/](docs/screenshots/)

## Планы

- PWA, офлайн-режим
- Расширенные отчёты
- Импорт из Excel

## Лицензия

Для внутреннего использования.
