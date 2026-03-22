# Библиотека промптов FISH-MVP

Документ содержит перечень промптов, использованных при разработке FISH-MVP в Cursor.

| № | Название | Файл | Этап | Среда | Описание | Результат |
|---|----------|------|------|-------|----------|-----------|
| 01 | Идея | 01-idea.md | 1.1 | ЛОКАЛЬНО | Определение идеи и формата | docs/IDEA.md |
| 02 | ТЗ | 02-spec.md | 1.2 | ЛОКАЛЬНО | Техническое задание | docs/SPECIFICATION.md |
| 03 | Инструменты | 03-tools-setup.md | 2.1 | ЛОКАЛЬНО | Стек, конфигурация | requirements.txt, config.py, структура |
| 04 | Git | 04-git-init.md | 2.2 | ЛОКАЛЬНО | Инициализация репозитория | git init, docs/DEPLOYMENT.md |
| 05 | Схема БД | 05-database-schema.md | 3.1 | ЛОКАЛЬНО | Таблицы Разрешения, Рыба, Выловы | fish_database.py, init_db.py |
| 06 | Auth | 06-auth-model.md | 3.2 | ЛОКАЛЬНО | Авторизация | auth_database.py |
| 07 | API Permissions/Fish | 07-api-permissions-fish.md | 4.1 | ЛОКАЛЬНО | CRUD разрешений и рыбы | Эндпоинты в app.py |
| 08 | API Catches/Stats | 08-api-catches-stats.md | 4.2 | ЛОКАЛЬНО | Выловы, статистика, экспорт | Эндпоинты в app.py |
| 09 | Веб-страницы | 09-web-pages.md | 4.3 | ЛОКАЛЬНО | HTML-страницы | templates/, static/ |
| 10 | Unit-тесты | 10-unit-tests.md | 5.1 | ЛОКАЛЬНО | pytest-тесты | tests/ |
| 11 | CI | 11-ci-workflow.md | 5.2 | ЛОКАЛЬНО | GitHub Actions | .github/workflows/test.yml |
| 12 | README | 12-readme-docs.md | 6.1 | ЛОКАЛЬНО | Документация | README.md |
| 13 | Docker | 13-docker-build.md | 7.1 | ЛОКАЛЬНО | Контейнеризация | Dockerfile, docker-compose.yml |
| 14 | GitHub Docker | 14-github-docker.md | 7.2 | ЛОКАЛЬНО | Сборка образа в CI | .github/workflows/docker-build.yml |
| 15 | Деплой | 15-deploy-server.md | 7.3 | СЕРВЕР | Инструкция деплоя на VPS | docs/DEPLOYMENT.md |
| 16 | Скриншоты | 16-screenshots.md | 8.1 | ЛОКАЛЬНО | Визуальные материалы | docs/screenshots/ |
| 17 | Библиотека | 17-prompts-library.md | 8.2 | ЛОКАЛЬНО | Сводный документ | docs/PROMPTS_LIBRARY.md |

Полные тексты промптов: [docs/prompts/](prompts/README.md)
