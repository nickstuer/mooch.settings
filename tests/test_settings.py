import shutil
from pathlib import Path

import pytest

from mooch.settings import Settings

default_settings = {
    "settings.name": "MyName",
    "settings.mood": "MyMood",
    "dictionary.key1": "value1",
    "dictionary.key2": "value2",
    "dictionary.subdictionary.key1": "subvalue1",
    "dictionary.subdictionary.key2": "subvalue2",
}

default_settings2 = {
    "settings": {"name": "MyName", "mood": "MyMood", "gui": {"theme": {"ios": "dark"}}},
}


@pytest.fixture
def settings_filepath(tmpdir_factory: pytest.TempdirFactory):
    temp_dir = str(tmpdir_factory.mktemp("temp"))
    temp_testing_dir = temp_dir + "/testing/settings.toml"
    yield Path(temp_testing_dir)
    # yield Path("settings.toml")
    shutil.rmtree(temp_dir)


def test_settings_initializes_with_default_settings(settings_filepath: Path):
    settings = Settings(settings_filepath, default_settings)
    for k, v in default_settings.items():
        assert settings.get(k) == v

    assert settings.get("settings.name") == "MyName"
    assert settings.get("settings.mood") == "MyMood"
    assert settings.get("dictionary.key1") == "value1"
    assert settings.get("dictionary") == {
        "key1": "value1",
        "key2": "value2",
        "subdictionary": {"key1": "subvalue1", "key2": "subvalue2"},
    }

    assert settings.get("foo") is None


@pytest.mark.parametrize(
    ("value"),
    [
        ("settings.toml"),
        (523),
        (None),
        (["settings.toml"]),
        ({"settings.toml": "value"}),
    ],
)
def test_settings_settings_filepath_types_fails(value):
    with pytest.raises(TypeError) as exc_info:
        Settings(value)
    assert str(exc_info.value) == "settings_filepath must be a Path object"


@pytest.mark.parametrize(
    ("value"),
    [
        ("settings.toml"),
        (523),
        (["settings.toml"]),
    ],
)
def test_settings_default_settings_types_fails(value, settings_filepath):
    with pytest.raises(TypeError) as exc_info:
        Settings(settings_filepath, value)
    assert str(exc_info.value) == "default_settings must be a dictionary or None"


def test_settings_sets_default_settings_if_not_present(settings_filepath: Path):
    settings = Settings(settings_filepath, default_settings)
    assert settings.get("foo") is None

    default_settings["foo"] = "bar"
    new_settings = Settings(settings_filepath, default_settings)

    assert new_settings.get("foo") == "bar"
    for k, v in default_settings.items():
        assert new_settings.get(k) == v


def test_settings_get_and_set_methods_success(settings_filepath: Path):
    settings = Settings(settings_filepath, default_settings)

    settings.set("string", "string_value")
    settings.set("none", None)
    settings.set("int", 42)
    settings.set("float", 3.14)
    settings.set("bool", True)  # noqa: FBT003
    settings.set("list", [1, 2, 3])
    settings.set("dict", {"key": "value"})
    settings.set("nested_dict", {"nested_key": {"sub_key": "sub_value"}})
    settings.set("empty_list", [])
    settings.set("nested_list", [[1, 2, 3], [4, 5, 6], ["a", "b", "c"]])
    settings.set("empty_dict", {})
    settings.set("complex", {"list": [1, 2, 3], "dict": {"key": "value"}})
    settings.set("complex_nested", {"outer": {"inner": {"key": "value"}}})
    settings.set("unicode", "こんにちは")  # Japanese for "Hello"
    settings.set("emoji", "😊")  # Smiling face emoji

    assert settings.get("string") == "string_value"
    assert settings.get("none") is None
    assert settings.get("int") == 42
    assert settings.get("float") == 3.14
    assert settings.get("bool") is True
    assert settings.get("list") == [1, 2, 3]
    assert settings.get("dict") == {"key": "value"}
    assert settings.get("nested_dict") == {"nested_key": {"sub_key": "sub_value"}}
    assert settings.get("empty_list") == []
    assert settings.get("nested_list") == [[1, 2, 3], [4, 5, 6], ["a", "b", "c"]]
    assert settings.get("empty_dict") == {}
    assert settings.get("complex") == {"list": [1, 2, 3], "dict": {"key": "value"}}
    assert settings.get("complex_nested") == {"outer": {"inner": {"key": "value"}}}
    assert settings.get("unicode") == "こんにちは"
    assert settings.get("emoji") == "😊"


def test_settings_overrides_existing_settings(settings_filepath: Path):
    settings = Settings(settings_filepath, default_settings)

    # Set an initial value
    settings.set("name", "InitialName")
    assert settings.get("name") == "InitialName"

    # Override the value
    settings.set("name", "NewName")
    assert settings.get("name") == "NewName"


def test_settings_handles_non_existent_keys(settings_filepath: Path):
    settings = Settings(settings_filepath, default_settings)

    assert settings.get("non_existent_key") is None


def test_settings_handles_empty_settings_file(settings_filepath: Path):
    # Create an empty settings file
    settings_filepath.parent.mkdir(parents=True, exist_ok=True)
    with Path.open(settings_filepath, "w") as f:
        f.write("")
    settings = Settings(settings_filepath, default_settings)
    # Check that default settings are applied
    for k, v in default_settings.items():
        assert settings.get(k) == v


def test_settings_handles_creating_directories_for_new_files(settings_filepath: Path):
    parent_dir = settings_filepath.parent

    assert not parent_dir.exists(), "Parent directory should not exist before test"

    settings = Settings(settings_filepath, default_settings)
    assert parent_dir.exists(), "Parent directory should be created by Settings class"


def test_settings_saves_settings_to_file(settings_filepath: Path):
    settings = Settings(settings_filepath, default_settings)

    # Set some values
    settings.set("name", "TestName")
    settings.set("mood", "TestMood")

    # Reload the settings to check if values are saved
    new_settings = Settings(settings_filepath, default_settings)
    assert new_settings.get("name") == "TestName"
    assert new_settings.get("mood") == "TestMood"


def test_settings_no_default_settings(settings_filepath: Path):
    # Test with no default settings
    settings = Settings(settings_filepath)

    # Check that no settings are set initially
    assert settings.get("name") is None
    assert settings.get("mood") is None

    # Set a value and check if it persists
    settings.set("name", "NoDefaultName")
    assert settings.get("name") == "NoDefaultName"

    # Reload the settings to check if the value is saved
    new_settings = Settings(settings_filepath)
    assert new_settings.get("name") == "NoDefaultName"


def test_settings_with_getitem_and_setitem(settings_filepath: Path):
    settings = Settings(settings_filepath, default_settings)

    # Test __getitem__
    assert settings["settings.name"] == "MyName"
    assert settings["settings.mood"] == "MyMood"
    assert settings["dictionary.key1"] == "value1"

    # Test __setitem__
    settings["settings.name"] = "NewName"
    assert settings["settings.name"] == "NewName"

    settings["new_key"] = "new_value"
    assert settings["new_key"] == "new_value"


def test_settings_updates_defaults_with_nested_dict(settings_filepath: Path):
    settings = Settings(settings_filepath, default_settings)
    assert settings.get("dictionary.subdictionary.key3") is None
    assert settings["dictionary.subdictionary.key3"] is None

    default_settings["dictionary.subdictionary.key3"] = "subvalue3"

    # Access a nested value
    new_settings = Settings(settings_filepath, default_settings)
    assert new_settings.get("dictionary.subdictionary.key3") == "subvalue3"
    assert new_settings["dictionary"]["subdictionary"]["key3"] == "subvalue3"


def test_settings_initializes_defaults_with_nested_dict(settings_filepath: Path):
    settings = Settings(settings_filepath, default_settings2)
    assert settings.get("settings.name") == "MyName"
    assert settings.get("settings.mood") == "MyMood"
    assert settings["settings"]["name"] == "MyName"
    assert settings["settings"]["mood"] == "MyMood"
    assert settings["settings"] == {"gui": {"theme": {"ios": "dark"}}, "mood": "MyMood", "name": "MyName"}
    assert settings["settings"]["gui"]["theme"] == {"ios": "dark"}
    assert settings["settings"]["gui"]["theme"]["ios"] == "dark"
    assert settings.get("dictionary") is None
    assert settings.get("dictionary.key1") is None
    assert settings.get("dictionary.subdictionary") is None
    assert settings.get("dictionary.subdictionary.key1") is None
    assert settings.get("settings.gui.theme.ios") == "dark"
    assert settings.get("settings") == {"gui": {"theme": {"ios": "dark"}}, "mood": "MyMood", "name": "MyName"}


def test_settings_sets_default_settings_of_nested_dictionaries_if_not_present(settings_filepath: Path):
    settings = Settings(settings_filepath, default_settings2)
    assert settings.get("settings.gui.theme.ios") == "dark"
    assert settings.get("settings.gui.theme.android") is None

    settings.set("settings.gui.theme.ios", "light")  # change from default dark to light

    new_default_settings = {
        "settings": {"name": "MyName", "mood": "MyMood", "gui": {"theme": {"ios": "dark", "android": "light"}}},
    }

    new_settings = Settings(settings_filepath, new_default_settings)

    assert new_settings.get("settings.gui.theme.ios") == "light"  # verify that this is not overwritten by the default
    assert new_settings.get("settings.gui.theme.android") == "light"


def test_settings_dynamic_reload_true(settings_filepath: Path):
    settings = Settings(settings_filepath, default_settings)

    assert settings.get("settings.name") == "MyName"

    # Change the settings file seperatrely
    settings2 = Settings(settings_filepath, default_settings)
    settings2.set("settings.name", "NewName")

    # Verify that the change is reflected in the original settings object
    assert settings.get("settings.name") == "NewName"


def test_settings_dynamic_reload_false(settings_filepath: Path):
    settings = Settings(settings_filepath, default_settings)
    settings.dynamic_reload = False

    assert settings.get("settings.name") == "MyName"

    # Change the settings file seperatrely
    settings2 = Settings(settings_filepath, default_settings)
    settings2.set("settings.name", "NewName")


# Verify that the change is reflected in the original settings object
def test_settings_repr_returns_expected_string(settings_filepath: Path):
    settings = Settings(settings_filepath, default_settings)
    expected = f"Settings Stored at: {settings_filepath}"
    assert repr(settings) == expected
