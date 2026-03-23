# Промпт 10: Unit-тесты

**Этап:** 5.1 Тестирование  
**Среда:** [ЛОКАЛЬНО]

## Контекст

Приложение работает. Нужны pytest-тесты для моделей и API.

## Задача

tests/ с тестами auth, permissions, fish, catches. Использовать тестовую БД (in-memory или temp file).

## Критерии приёмки

- `pytest` проходит
- Покрытие: логин, CRUD разрешений, рыбы, выловов

## Текст промпта

```
Добавь pytest-тесты для FISH-MVP:

1. tests/conftest.py — фикстуры:
   - app — Flask test client
   - db — тестовая SQLite in-memory или temp
   - client с залогиненным admin (session)

2. tests/test_auth.py — тесты логина, logout, недоступность /api/permissions без авторизации

3. tests/test_permissions.py — CRUD разрешений через API

4. tests/test_fish.py — CRUD рыбы

5. tests/test_catches.py — создание вылова (с валидным разрешением и рыбой), получение списка

6. requirements.txt — добавь pytest

Запуск: pytest -v. Используй app.test_client(), тестовая конфигурация с отдельной БД.
"""
