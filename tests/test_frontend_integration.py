import os
import subprocess
from pathlib import Path
import pytest

frontend_dir = Path(__file__).resolve().parents[1] / 'web' / 'frontend'

@pytest.mark.skipif(not (frontend_dir / 'node_modules').exists(), reason='node modules not installed')
def test_frontend_tests():
    result = subprocess.run(['npm', 'test', '--', '--run'], cwd=frontend_dir)
    assert result.returncode == 0
