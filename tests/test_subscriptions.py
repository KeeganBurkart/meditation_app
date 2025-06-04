import sys
from pathlib import Path
import sqlite3

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import mindful
from subscriptions import subscribe_user, get_user_tier, is_premium, has_feature_access


def setup_db():
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    conn.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        ("user@example.com", "hash"),
    )
    return conn


def test_subscribe_and_check_tier():
    conn = setup_db()
    subscribe_user(conn, 1, "premium", "2023-01-01")
    assert get_user_tier(conn, 1) == "premium"
    assert is_premium(conn, 1) is True


def test_has_feature_access():
    conn = setup_db()
    assert has_feature_access(conn, 1, "advanced_stats") is False
    subscribe_user(conn, 1, "premium", "2023-01-01")
    assert has_feature_access(conn, 1, "advanced_stats") is True

