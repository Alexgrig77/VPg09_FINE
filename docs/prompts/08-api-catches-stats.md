# Промпт 08: API выловов и статистики

**Этап:** 4.2 API  
**Среда:** [ЛОКАЛЬНО]

## Контекст

API разрешений и рыбы готовы. Нужны выловы и простая статистика, экспорт CSV.

## Задача

CRUD для выловов, GET /api/statistics, GET /api/export-catches (CSV).

## Критерии приёмки

- CRUD выловов работает
- Статистика: общее количество выловов, сумма, по разрешениям
- Экспорт возвращает CSV-файл

## Текст промпта

```
Добавь API выловов и статистики в FISH-MVP:

1. Эндпоинты выловов:
   - GET /api/catches — список (опционально ?permission=, ?fish=)
   - GET /api/catches/<id>
   - POST /api/catches — создание (Разрешение, Дата_вылова, Наименование_рыбы, Количество; Сумма = Количество * Цена из Рыба)
   - PUT /api/catches/<id>
   - DELETE /api/catches/<id>

2. GET /api/statistics — JSON: total_catches, total_sum, by_permission (массив {permission, count, sum})

3. GET /api/export-catches — возврат CSV (Content-Disposition: attachment). Поля: Разрешение, Дата, Рыба, Количество, Сумма.

4. Добавь методы в FishDatabase для работы с Выловы и статистикой.

Все эндпоинты под @login_required.
"""
