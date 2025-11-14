from pathlib import Path

import pytest
from pytest import MonkeyPatch


@pytest.fixture
def temp_cwd(tmp_path: Path, monkeypatch: MonkeyPatch) -> Path:
    """
    Run each test from a temporary directory so logs are created
    under <tmp>/logs instead of your real project root.
    """
    monkeypatch.chdir(tmp_path)
    return tmp_path
