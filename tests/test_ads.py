import sqlite3
import pytest

from src import mindful
from src.ads import AdManager


def test_ad_rotation():
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    manager = AdManager(conn)
    manager.add_ad("Ad one")
    manager.add_ad("Ad two")
    seen = {manager.get_random_ad().text for _ in range(10)}
    assert {"Ad one", "Ad two"} == seen


def test_get_random_ad_ignores_inactive():
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    manager = AdManager(conn)
    manager.add_ad("Active", is_active=True)
    manager.add_ad("Inactive", is_active=False)
    seen = {manager.get_random_ad().text for _ in range(10)}
    assert seen == {"Active"}


def test_get_random_ad_no_active_raises():
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    manager = AdManager(conn)
    manager.add_ad("Inactive", is_active=False)
    with pytest.raises(ValueError):
        manager.get_random_ad()

