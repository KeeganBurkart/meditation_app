import sqlite3

from src import mindful, auth


def test_register_user():
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    user_id = auth.register_user(conn, "user@example.com", "secret", display_name="User")
    cur = conn.execute(
        "SELECT email, display_name, bio, photo_url, is_public FROM users WHERE id = ?",
        (user_id,),
    )
    row = cur.fetchone()
    assert row == ("user@example.com", "User", "", None, 1)


def test_register_social_user():
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    user_id = auth.register_social_user(
        conn,
        "google",
        "g123",
        email="social@example.com",
        display_name="Social",
    )
    cur = conn.execute(
        "SELECT email, password_hash, display_name, bio, photo_url, is_public FROM users WHERE id = ?",
        (user_id,),
    )
    row = cur.fetchone()
    assert row == ("social@example.com", None, "Social", "", None, 1)
    cur = conn.execute(
        "SELECT provider, provider_user_id FROM social_accounts WHERE user_id = ?",
        (user_id,),
    )
    row = cur.fetchone()
    assert row == ("google", "g123")
