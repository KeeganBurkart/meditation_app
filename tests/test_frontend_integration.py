import os
import subprocess
import shutil
from pathlib import Path
import pytest

frontend_dir = Path(__file__).resolve().parents[1] / "web" / "frontend"
skip_reason = "node modules or npm missing"


@pytest.mark.skipif(
    not (frontend_dir / "node_modules").exists() or shutil.which("npm") is None,
    reason=skip_reason,
)
def test_frontend_tests():
    result = subprocess.run(["npm", "test", "--", "--run"], cwd=frontend_dir)
    assert result.returncode == 0
