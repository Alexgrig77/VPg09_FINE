"""Pytest fixtures for FISH-MVP"""
import os
import sys
import tempfile

import pytest

# Ensure app is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use temp DB for tests
TEST_DB = os.path.join(tempfile.gettempdir(), 'fish_mvp_test.db')
os.environ['DATABASE_PATH'] = TEST_DB
os.environ['SECRET_KEY'] = 'test-secret-key'
os.environ['FLASK_ENV'] = 'testing'


@pytest.fixture(scope='session')
def app():
    """Create app and init DB once per session"""
    from application.models.fish_database import FishDatabase
    from application.models.auth_database import AuthDatabase

    os.makedirs(os.path.dirname(TEST_DB) or '.', exist_ok=True)
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    fd = FishDatabase(TEST_DB)
    fd.create_tables()
    ad = AuthDatabase(TEST_DB)
    ad.create_auth_tables()
    ad.create_user('admin', 'admin123', 'Admin', 'admin')

    from app import app as flask_app
    flask_app.config['TESTING'] = True
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_client(client):
    """Client with logged-in admin"""
    client.post('/api/auth/login', json={'username': 'admin', 'password': 'admin123'})
    return client
