# Промпт 06: Модель авторизации

**Этап:** 3.2 Авторизация  
**Среда:** [ЛОКАЛЬНО]

## Контекст

БД создана. Нужно добавить таблицу Пользователи и логику логина (admin/user).

## Задача

auth_database.py: create_auth_tables, create_user, get_user_by_username, verify_password. Роли admin и user.

## Критерии приёмки

- Таблица Пользователи: id, username, password_hash, full_name, role, is_active
- Скрипт создаёт admin/admin123 при init
- verify_password работает с Werkzeug hashing

## Текст промпта

```
Добавь авторизацию в FISH-MVP:

1. application/models/auth_database.py:
   - AuthDatabase с методами get_connection(), create_auth_tables(), create_user(), get_user_by_username(), verify_password()
   - create_auth_tables() — таблица Пользователи: id, username, password_hash, full_name, role (admin/user), is_active, created_at, updated_at
   - Используй werkzeug.security.generate_password_hash, check_password_hash

2. Обнови scripts/init_db.py:
   - Вызвать create_auth_tables()
   - Создать пользователя admin / admin123 с ролью admin если его нет

Путь к БД из config.py или DATABASE_PATH в окружении.
```
