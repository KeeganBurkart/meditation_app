import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from profiles import ProfileManager


def test_profile_visibility():
    manager = ProfileManager()
    manager.create_profile(1, "alice")
    manager.create_profile(2, "bob", is_public=False)

    # public profile visible to others
    assert manager.can_view(2, 1) is True

    # private profile hidden from others
    assert manager.can_view(1, 2) is False

    # owner can always view their own profile
    assert manager.can_view(2, 2) is True

    # changing visibility updates access
    manager.set_visibility(2, True)
    assert manager.can_view(1, 2) is True
