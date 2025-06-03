import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import mindful


def test_add_numbers():
    assert mindful.add_numbers(1, 2) == 3
