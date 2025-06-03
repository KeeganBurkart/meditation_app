import sys
from pathlib import Path
import sqlite3

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import mindful


def test_add_and_retrieve_custom_type():
    # use an in-memory database for isolation
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    # create a user to satisfy foreign key constraint
    conn.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        ("user@example.com", "hash"),
    )
    mindful.add_custom_meditation_type(conn, 1, "Zen")
    assert mindful.get_custom_meditation_types(conn, 1) == ["Zen"]
