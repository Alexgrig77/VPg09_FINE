# Промпт 11: CI GitHub Actions

**Этап:** 5.2 CI  
**Среда:** [ЛОКАЛЬНО]

## Контекст

Тесты есть. Нужен workflow для запуска pytest при push/PR.

## Задача

.github/workflows/test.yml — install deps, pytest.

## Критерии приёмки

- Push в main/PR запускает workflow
- pytest выполняется и проходит

## Текст промпта

```
Создай GitHub Actions workflow для FISH-MVP:

Файл .github/workflows/test.yml:
- Триггер: push, pull_request на main и master
- Job: Ubuntu latest
- Шаги: checkout, setup-python 3.11, pip install -r requirements.txt, pytest -v
- Опционально: установить FLASK_ENV=testing и DATABASE_PATH для тестов

Убедись что тесты не требуют реальной БД в data/ — используй in-memory или temp.
"""
