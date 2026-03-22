"""Tests for auth API"""
import pytest


def test_login_success(client):
    r = client.post('/api/auth/login', json={'username': 'admin', 'password': 'admin123'})
    assert r.status_code == 200
    data = r.get_json()
    assert data.get('ok') is True
    assert data.get('username') == 'admin'


def test_login_fail(client):
    r = client.post('/api/auth/login', json={'username': 'admin', 'password': 'wrong'})
    assert r.status_code == 401


def test_api_requires_auth(client):
    r = client.get('/api/permissions')
    assert r.status_code == 401


def test_api_works_when_authenticated(auth_client):
    r = auth_client.get('/api/permissions')
    assert r.status_code == 200


def test_test_endpoint_no_auth(client):
    r = client.get('/api/test')
    assert r.status_code == 200
    assert r.get_json().get('status') == 'ok'
