# Промпт 12: README и документация

**Этап:** 6.1 Документация  
**Среда:** [ЛОКАЛЬНО]

## Контекст

Проект готов. Нужен README по правилам пользователя.

## Задача

README.md: название, описание, стек, инструкция запуска, API/команды, скриншоты (placeholder).

## Критерии приёмки

- Название, краткое описание, стек (Flask, SQLite и т.д.)
- Инструкция: pip install, init_db, app.py
- Список API endpoints
- Упоминание docs/screenshots/

## Текст промпта

```
Обнови README.md для FISH-MVP по правилам:

1. Название проекта
2. Краткое описание — что делает, зачем нужен
3. Стек: Flask, SQLite, Python 3.8+
4. Инструкция по запуску:
   - pip install -r requirements.txt
   - python scripts/init_db.py
   - python app.py
   - Открыть http://localhost:5000
5. API — таблица эндпоинтов: /api/auth/login, /api/permissions, /api/fish, /api/catches, /api/statistics, /api/export-catches
6. Скриншоты: см. docs/screenshots/
7. Планы на будущее (опционально)

Также добавь в README информацию:
- Админские эндпоинты для управления сотрудниками: `/api/admin/responsibles`, `/api/admin/users`, смена пароля/статуса.
- Что сотрудники видят только свои разрешения и добавляют выловы только по своим разрешениям.
- Что список рыбы в форме вылова зависит от выбранного номера разрешения (`/api/fish-names?permission=...`).
"""
