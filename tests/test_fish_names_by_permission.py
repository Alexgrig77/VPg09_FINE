"""Проверка фильтрации списка рыбы по выбранному разрешению."""


def test_fish_names_filtered_by_permission(auth_client):
    # Рыба: 1 и 2 в разных группах
    r1 = auth_client.post('/api/fish', json={
        'Наименование_рыбы': 'РыбаХищная1',
        'Наименование_групповое': 'ГруппаХищные',
        'Цена': 100
    })
    assert r1.status_code == 201

    r2 = auth_client.post('/api/fish', json={
        'Наименование_рыбы': 'РыбаКарповая1',
        'Наименование_групповое': 'ГруппаКарповые',
        'Цена': 120
    })
    assert r2.status_code == 201

    responsible = 'Иванов Иван'

    # Разрешение с группой "ГруппаХищные"
    p1 = auth_client.post('/api/permissions', json={
        'Номер_разрешения': 'PERM-1',
        'Год': '2026',
        'Район_промысла': 'Район',
        'Ответственный': responsible,
        'Наименование_групповое': 'ГруппаХищные',
        'Лимит_кг': 10
    })
    assert p1.status_code == 201

    # Смотрим рыбу для PERM-1
    fish_list = auth_client.get('/api/fish-names?permission=PERM-1').get_json()
    assert 'РыбаХищная1' in fish_list
    assert 'РыбаКарповая1' not in fish_list

