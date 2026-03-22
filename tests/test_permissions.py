"""Tests for permissions API"""
import pytest


def test_create_and_list_permission(auth_client):
    r = auth_client.post('/api/permissions', json={
        'Номер_разрешения': 'TEST-001',
        'Год': '2025',
        'Район_промысла': 'Район',
        'Ответственный': 'Иванов',
        'Наименование_групповое': 'Щука',
        'Лимит_кг': 100
    })
    assert r.status_code == 201
    data = r.get_json()
    assert 'id' in data

    r2 = auth_client.get('/api/permissions')
    assert r2.status_code == 200
    items = r2.get_json()
    assert any(p['Номер_разрешения'] == 'TEST-001' for p in items)


def test_update_permission(auth_client):
    r = auth_client.post('/api/permissions', json={
        'Номер_разрешения': 'UPD-001', 'Год': '2025', 'Лимит_кг': 50
    })
    pid = r.get_json()['id']
    r2 = auth_client.put(f'/api/permissions/{pid}', json={
        'Номер_разрешения': 'UPD-002', 'Год': '2025', 'Лимит_кг': 75
    })
    assert r2.status_code == 200
    r3 = auth_client.get(f'/api/permissions/{pid}')
    assert r3.get_json()['Номер_разрешения'] == 'UPD-002'


def test_delete_permission(auth_client):
    r = auth_client.post('/api/permissions', json={
        'Номер_разрешения': 'DEL-001', 'Год': '2025'
    })
    pid = r.get_json()['id']
    r2 = auth_client.delete(f'/api/permissions/{pid}')
    assert r2.status_code == 200
    r3 = auth_client.get(f'/api/permissions/{pid}')
    assert r3.status_code == 404
