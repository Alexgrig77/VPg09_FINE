"""Проверка ограничений доступа сотрудника по полю Разрешения.Ответственный."""

from uuid import uuid4


def login(client, username, password):
    r = client.post('/api/auth/login', json={'username': username, 'password': password})
    assert r.status_code == 200
    return r.get_json()


def test_employee_can_add_catches_only_for_his_permissions(app):
    admin_client = app.test_client()
    login(admin_client, 'admin', 'admin123')

    worker_username = f'worker_{uuid4().hex[:6]}'
    worker_password = 'worker123'
    responsible_a = f'ТестИванов_{uuid4().hex[:4]}'
    responsible_b = f'ТестПетров_{uuid4().hex[:4]}'

    perm_a = f'EMP-A-{uuid4().hex[:4]}'
    perm_b = f'EMP-B-{uuid4().hex[:4]}'

    # Разрешения (только админ может создавать)
    r1 = admin_client.post('/api/permissions', json={
        'Номер_разрешения': perm_a,
        'Год': '2026',
        'Район_промысла': 'РайонA',
        'Ответственный': responsible_a,
        'Наименование_групповое': 'Щука',
        'Лимит_кг': 100,
    })
    assert r1.status_code == 201

    r2 = admin_client.post('/api/permissions', json={
        'Номер_разрешения': perm_b,
        'Год': '2026',
        'Район_промысла': 'РайонB',
        'Ответственный': responsible_b,
        'Наименование_групповое': 'Лещ',
        'Лимит_кг': 200,
    })
    assert r2.status_code == 201

    # Рыба
    rf = admin_client.post('/api/fish', json={
        'Наименование_рыбы': 'Судак',
        'Наименование_групповое': 'Хищные',
        'Цена': 250,
    })
    assert rf.status_code == 201

    # Создаём сотрудника через админ API (поле full_name должно совпасть с Ответственный)
    ru = admin_client.post('/api/admin/users', json={
        'username': worker_username,
        'full_name': responsible_a,
        'password': worker_password
    })
    assert ru.status_code == 201

    worker_client = app.test_client()
    login(worker_client, worker_username, worker_password)

    # Сотрудник видит только свои разрешения
    perms = worker_client.get('/api/permissions').get_json()
    assert perms, 'Ожидали список разрешений'
    assert all(p['Ответственный'] == responsible_a for p in perms)

    # Сотрудник не может создавать разрешения
    rcreate_perm = worker_client.post('/api/permissions', json={
        'Номер_разрешения': 'X',
        'Год': '2026',
        'Район_промысла': 'R',
        'Ответственный': responsible_a,
        'Лимит_кг': 1,
    })
    assert rcreate_perm.status_code == 403

    # Сотрудник может добавить вылов по своему разрешению
    rc_a = worker_client.post('/api/catches', json={
        'Разрешение': perm_a,
        'Дата_вылова': '2026-03-20',
        'Наименование_рыбы': 'Судак',
        'Количество': 2,
    })
    assert rc_a.status_code == 201

    # Сотрудник не может добавить вылов по чужому разрешению
    rc_b = worker_client.post('/api/catches', json={
        'Разрешение': perm_b,
        'Дата_вылова': '2026-03-20',
        'Наименование_рыбы': 'Судак',
        'Количество': 2,
    })
    assert rc_b.status_code == 403

    # Список выловов и статистика — только по своим разрешениям
    catches = worker_client.get('/api/catches').get_json()
    assert all(c['Разрешение'] == perm_a for c in catches)
    assert len(catches) == 1

    stats = worker_client.get('/api/statistics').get_json()
    assert stats['total_catches'] == 1
    assert all(x['Разрешение'] == perm_a for x in stats['by_permission'])

