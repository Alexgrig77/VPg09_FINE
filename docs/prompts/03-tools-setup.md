# Промпт 03: Стек и структура проекта

**Этап:** 2.1 Инструменты  
**Среда:** [ЛОКАЛЬНО]

## Контекст

ТЗ готово. Нужно подготовить окружение: зависимости, конфигурация, структура папок.

## Задача

Создать `requirements.txt`, структуру папок, `config.py`, `.env.example`, `.gitignore`.

## Критерии приёмки

- `pip install -r requirements.txt` выполняется без ошибок
- `config.py` загружает настройки из .env
- Есть `.env.example` с SECRET_KEY, FLASK_ENV, DATABASE_PATH

## Текст промпта

```
Создай базовую структуру Flask-проекта FISH-MVP:

1. requirements.txt: Flask, Flask-CORS, python-dotenv, Werkzeug (укажи версии)

2. Структура папок:
   - application/ models/ routes/ utils/
   - static/ css/ js/
   - templates/
   - data/ (для БД)
   - docs/

3. config.py — Config с SECRET_KEY, DATABASE_PATH, SESSION настройками, загрузка из os.environ

4. .env.example — SECRET_KEY=, FLASK_ENV=development, DATABASE_PATH=data/FISH.db

5. .gitignore — venv, __pycache__, .env, *.db, data/*.db, logs/

6. app.py — минимальный Flask app с одной route "/" возвращающей JSON или текст "FISH-MVP OK"

Создай __init__.py в application, application/models, application/routes, application/utils. Добавь версионирование в app.py если нужно (VERSION = "1.0.0").
```
