"""Tests for fish API"""
import pytest


def test_create_and_list_fish(auth_client):
    r = auth_client.post('/api/fish', json={
        'Наименование_рыбы': 'Щука',
        'Наименование_групповое': 'Хищные',
        'Цена': 150.5
    })
    assert r.status_code == 201
    fid = r.get_json()['id']

    r2 = auth_client.get('/api/fish')
    assert r2.status_code == 200
    items = r2.get_json()
    assert any(f['Наименование_рыбы'] == 'Щука' for f in items)


def test_delete_fish(auth_client):
    r = auth_client.post('/api/fish', json={
        'Наименование_рыбы': 'Окунь', 'Наименование_групповое': 'Хищные', 'Цена': 80
    })
    fid = r.get_json()['id']
    r2 = auth_client.delete(f'/api/fish/{fid}')
    assert r2.status_code == 200
