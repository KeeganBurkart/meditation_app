import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from ads import AdManager


def test_ad_rotation():
    manager = AdManager()
    manager.add_ad("Ad one")
    manager.add_ad("Ad two")
    seen = {manager.get_random_ad().text for _ in range(10)}
    assert {"Ad one", "Ad two"} == seen

