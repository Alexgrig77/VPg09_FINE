"""Tests for catches API"""
import pytest


def test_create_catch(auth_client):
    auth_client.post('/api/permissions', json={
        'Номер_разрешения': 'C-001', 'Год': '2025', 'Лимит_кг': 100
    })
    auth_client.post('/api/fish', json={
        'Наименование_рыбы': 'Судак', 'Наименование_групповое': 'Хищные', 'Цена': 200
    })

    r = auth_client.post('/api/catches', json={
        'Разрешение': 'C-001',
        'Дата_вылова': '2025-03-20',
        'Наименование_рыбы': 'Судак',
        'Количество': 5
    })
    assert r.status_code == 201
    cid = r.get_json()['id']

    r2 = auth_client.get('/api/catches')
    assert r2.status_code == 200
    items = r2.get_json()
    assert any(c['Разрешение'] == 'C-001' and c['Наименование_рыбы'] == 'Судак' for c in items)
