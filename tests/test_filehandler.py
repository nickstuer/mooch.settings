import shutil
from pathlib import Path

import pytest

from mooch.settings.filehandler import FileHandler


@pytest.fixture
def temp_settings_file(tmp_path):
    file_path = tmp_path / "settings.toml"
    yield file_path
    if file_path.exists():
        file_path.unlink()
    shutil.rmtree(tmp_path, ignore_errors=True)


def test_load_returns_correct_data(temp_settings_file):
    file = FileHandler(temp_settings_file)
    # Write some data
    data = {"foo": {"bar": 123}}
    file.save(data)
    loaded = file.load()
    assert loaded["foo"]["bar"] == 123


def test_save_and_load_roundtrip(temp_settings_file):
    file = FileHandler(temp_settings_file)
    data = {"alpha": 1, "beta": {"gamma": 2}}
    file.save(data)
    loaded = file.load()
    assert loaded["alpha"] == 1
    assert loaded["beta"]["gamma"] == 2


def test_create_file_if_not_exists_does_not_overwrite_existing(temp_settings_file):
    # Create file manually
    with Path.open(temp_settings_file, "w", encoding="utf-8") as f:
        f.write('[custom]\nkey="value"\n')
    file = FileHandler(temp_settings_file)
    data = file.load()
    assert "custom" in data
    assert data["custom"]["key"] == "value"
