import sqlite3

from src import mindful


def test_add_and_retrieve_custom_type():
    # use an in-memory database for isolation
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    # create a user to satisfy foreign key constraint
    conn.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        ("user@example.com", "hash"),
    )
    type_id = mindful.add_custom_meditation_type(conn, 1, "Zen")
    assert mindful.get_custom_meditation_types(conn, 1) == [(type_id, "Zen")]
