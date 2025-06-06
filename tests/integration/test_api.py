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


def test_sessions_and_dashboard(client):
    headers = {}

    client.post(
        "/sessions",
        json={
            "date": "2023-01-01",
            "duration": 10,
            "type": "Guided",
            "time": "06:00",
            "location": "Home",
        },
        headers=headers,
    )
    client.post(
        "/sessions",
        json={
            "date": "2023-01-02",
            "duration": 15,
            "type": "Guided",
            "time": "06:00",
            "location": "Home",
        },
        headers=headers,
    )

    resp = client.get("/dashboard/me", headers=headers)
    assert resp.status_code == 200
    assert resp.json() == {
        "total": 25,
        "sessions": 2,
        "streak": 2,
    }


def test_dashboard_empty_initially(client):
    resp = client.get("/dashboard/me")
    assert resp.status_code == 200
    assert resp.json() == {"total": 0, "sessions": 0, "streak": 0}


def auth_headers(client, email: str, password: str, display_name: str = "User"):
    # Update the display name for the default user to simulate account details
    import backend.main as m
    m.conn.execute(
        "UPDATE users SET display_name = ? WHERE id = 1",
        (display_name,),
    )
    m.conn.commit()
    return {}


def test_custom_type_crud(client):
    headers = auth_headers(client, "ct@example.com", "pw")

    resp = client.post(
        "/users/me/custom-meditation-types",
        json={"type_name": "Zen"},
        headers=headers,
    )
    assert resp.status_code == 200
    type_id = resp.json()["id"]

    resp = client.get("/users/me/custom-meditation-types", headers=headers)
    assert any(t["type_name"] == "Zen" for t in resp.json())

    resp = client.put(
        f"/users/me/custom-meditation-types/{type_id}",
        json={"type_name": "Vipassana"},
        headers=headers,
    )
    assert resp.status_code == 200
    resp = client.get("/users/me/custom-meditation-types", headers=headers)
    assert any(t["type_name"] == "Vipassana" for t in resp.json())

    resp = client.delete(
        f"/users/me/custom-meditation-types/{type_id}", headers=headers
    )
    assert resp.status_code == 200
    resp = client.get("/users/me/custom-meditation-types", headers=headers)
    assert resp.json() == []


def test_list_badges(client):
    headers = auth_headers(client, "badge@example.com", "pw")
    # Directly award a badge using module's connection
    import backend.main as m
    from src import challenges as challenges_mod

    challenges_mod.award_badge(m.conn, 1, "Early Adopter")

    resp = client.get("/users/me/badges", headers=headers)
    assert resp.status_code == 200
    assert resp.json() == [{"name": "Early Adopter"}]


def test_private_challenge_crud_with_premium_check(client):
    headers_free = auth_headers(client, "free@example.com", "pw")
    # Free user should be denied
    resp = client.post(
        "/users/me/private-challenges",
        json={
            "name": "Focus",
            "target_minutes": 30,
            "start_date": "2023-01-01",
            "end_date": "2023-01-07",
        },
        headers=headers_free,
    )
    assert resp.status_code == 403

    headers = auth_headers(client, "premium@example.com", "pw")
    import backend.main as m
    m.subscriptions.subscribe_user(
        m.conn, 1, "premium", "2023-01-01"
    )

    resp = client.post(
        "/users/me/private-challenges",
        json={
            "name": "Focus",
            "target_minutes": 30,
            "start_date": "2023-01-01",
            "end_date": "2023-01-07",
        },
        headers=headers,
    )
    assert resp.status_code == 200
    challenge_id = resp.json()["id"]

    resp = client.get("/users/me/private-challenges", headers=headers)
    assert len(resp.json()) == 1

    resp = client.put(
        f"/users/me/private-challenges/{challenge_id}",
        json={
            "name": "Renew Focus",
            "target_minutes": 40,
            "start_date": "2023-01-01",
            "end_date": "2023-01-07",
        },
        headers=headers,
    )
    assert resp.status_code == 200

    resp = client.delete(
        f"/users/me/private-challenges/{challenge_id}", headers=headers
    )
    assert resp.status_code == 200
    resp = client.get("/users/me/private-challenges", headers=headers)
    assert resp.json() == []

def test_public_profile_endpoint(client):
    headers = auth_headers(client, "profile@example.com", "pw", "ProfileUser")
    # log two sessions for user 1
    client.post(
        "/sessions",
        json={"date": "2023-01-01", "duration": 10, "type": "Guided"},
        headers=headers,
    )
    client.post(
        "/sessions",
        json={"date": "2023-01-02", "duration": 15, "type": "Guided"},
        headers=headers,
    )

    resp = client.get("/users/1/profile")
    assert resp.status_code == 200
    data = resp.json()
    assert data["display_name"] == "ProfileUser"
    assert data["total_minutes"] == 25
    assert data["session_count"] == 2
    assert data["recent_activity"] == [
        "Guided - 2023-01-02",
        "Guided - 2023-01-01",
    ]


def test_update_profile_visibility_endpoint(client):
    headers = auth_headers(client, "vis@example.com", "pw")

    resp = client.put(
        "/users/me/profile-visibility",
        json={"is_public": False},
        headers=headers,
    )
    assert resp.status_code == 200

    import backend.main as m

    cur = m.conn.execute("SELECT is_public FROM users WHERE id = 1")
    assert cur.fetchone()[0] == 0
