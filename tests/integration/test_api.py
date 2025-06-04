import os
import sys
import importlib

from fastapi.testclient import TestClient


def create_client(db_path):
    """Return a TestClient using a temporary SQLite database."""
    os.environ["DB_FILE"] = str(db_path)
    if "backend.main" in sys.modules:
        del sys.modules["backend.main"]
    app_module = importlib.import_module("backend.main")
    client = TestClient(app_module.app)
    return client, app_module


def setup_client(tmp_path):
    client, module = create_client(tmp_path / "test.db")
    yield client
    module.conn.close()



import pytest


@pytest.fixture
def client(tmp_path):
    yield from setup_client(tmp_path)


def test_signup_and_login(client):
    resp = client.post('/auth/signup', json={
        'email': 'user@example.com',
        'password': 'secret',
        'display_name': 'User'
    })
    assert resp.status_code == 200
    user_id = resp.json()['user_id']

    resp = client.post('/auth/login', json={
        'email': 'user@example.com',
        'password': 'secret'
    })
    assert resp.status_code == 200
    assert resp.json()['user_id'] == user_id


def test_login_failure(client):
    client.post('/auth/signup', json={
        'email': 'user2@example.com',
        'password': 'secret'
    })
    resp = client.post('/auth/login', json={
        'email': 'user2@example.com',
        'password': 'wrong'
    })
    assert resp.status_code == 401


def test_sessions_and_dashboard(client):
    resp = client.post('/auth/signup', json={
        'email': 'dash@example.com',
        'password': 'pass'
    })
    user_id = resp.json()['user_id']

    client.post('/sessions', json={
        'user_id': user_id,
        'date': '2023-01-01',
        'duration': 10,
        'type': 'Guided',
        'time': '06:00',
        'location': 'Home'
    })
    client.post('/sessions', json={
        'user_id': user_id,
        'date': '2023-01-02',
        'duration': 15,
        'type': 'Guided',
        'time': '06:00',
        'location': 'Home'
    })

    resp = client.get(f'/dashboard/{user_id}')
    assert resp.status_code == 200
    data = resp.json()
    assert data['total'] == 25
    assert data['sessions'] == 2
    assert data['streak'] == 2
