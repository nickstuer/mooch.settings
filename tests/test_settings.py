import shutil
from pathlib import Path

import pytest

from mooch.settings import Settings

default_settings_normal_format = {
    "settings": {"name": "MyName", "mood": "MyMood"},
    "dictionary": {
        "key1": "value1",
        "key2": "value2",
        "subdictionary": {"key1": "subvalue1", "key2": "subvalue2"},
    },
}
default_settings_nested_format = {
    "settings.name": "MyName",
    "settings.mood": "MyMood",
    "dictionary.key1": "value1",
    "dictionary.key2": "value2",
    "dictionary.subdictionary.key1": "subvalue1",
    "dictionary.subdictionary.key2": "subvalue2",
}


@pytest.fixture
def settings_name():
    return "testing-1234"


@pytest.fixture
def settings_filepath(tmpdir_factory: pytest.TempdirFactory):
    temp_dir = str(tmpdir_factory.mktemp("temp"))
    temp_testing_dir = temp_dir + "/testing/settings.toml"
    yield Path(temp_testing_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def temp_home():
    name = "test-blah-blah-test-only"
    temp_dir = Path.home() / f".{name}"
    path = temp_dir / "settings.toml"
    if path.exists():
        path.unlink()

    temp_home = {}
    temp_home["dir"] = temp_dir
    temp_home["name"] = name
    temp_home["path"] = path
    yield temp_home

    if path.exists():
        path.unlink()
    if temp_dir.exists():
        temp_dir.rmdir()


def test_settings_initializes_with_empty_file(settings_name, settings_filepath):
    settings = Settings(settings_name, filepath=settings_filepath)
    assert settings.get("settings.name") is None
    assert settings.get("settings.mood") is None
    assert settings.get("dictionary.key1") is None
    assert settings.get("dictionary") is None

    # Check if metadata keys are present
    assert settings.get("metadata.notice") is not None
    assert settings.get("metadata.created") is not None
    assert settings.get("metadata.updated") is not None
    assert settings.get("metadata.NotReal") is None


def test_settings_initializes_with_default_settings_normal_format(settings_name, settings_filepath):
    settings = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)
    for k, v in default_settings_normal_format.items():
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


def test_settings_initializes_with_default_settings_nested_format(settings_name, settings_filepath):
    settings = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_nested_format)
    for k, v in default_settings_nested_format.items():
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


## Type Tests
@pytest.mark.parametrize(
    ("value"),
    [
        (523),
        (None),
        (["settings.toml"]),
        ({"settings.toml": "value"}),
    ],
)
def test_settings_name_type_fails(settings_filepath, value):
    with pytest.raises(TypeError):
        _ = Settings(value, filepath=settings_filepath)


@pytest.mark.parametrize(
    ("value"),
    [
        "blah spaces",
        "blah spaces and dashes-",
        "/n",
        ".",
        ";",
        "",
    ],
)
def test_settings_name_alphanumericish_fails(settings_filepath, value):
    with pytest.raises(ValueError):  # noqa: PT011
        Settings(value, filepath=settings_filepath)


@pytest.mark.parametrize(
    ("value"),
    [
        "blah_spaces",
        "123",
        "abc",
        "ABC",
        "ABCabc123_-",
    ],
)
def test_settings_name_alphanumericish_passes(settings_filepath, value):
    _ = Settings(value, filepath=settings_filepath)


@pytest.mark.parametrize(
    ("value"),
    [
        (523),
        ("abc"),
    ],
)
def test_settings_defaults_type_fails(settings_name, settings_filepath, value):
    with pytest.raises(TypeError):
        _ = Settings(settings_name, filepath=settings_filepath, defaults=value)


@pytest.mark.parametrize(
    ("value"),
    [
        (523),
        ("abc"),
        (["settings.toml"]),
        ({"settings.toml": "value"}),
    ],
)
def test_settings_always_reloads_type_fails(settings_name, settings_filepath, value):
    with pytest.raises(TypeError):
        _ = Settings(settings_name, filepath=settings_filepath, defaults=value, always_reload=value)


@pytest.mark.parametrize(
    ("value"),
    [
        (523),
        ("abc"),
        (["settings.toml"]),
        ({"settings.toml": "value"}),
    ],
)
def test_settings_read_only_type_fails(settings_name, settings_filepath, value):
    with pytest.raises(TypeError):
        _ = Settings(settings_name, filepath=settings_filepath, defaults=value, read_only=value)


@pytest.mark.parametrize(
    ("value"),
    [
        (523),
        ("abc"),
        (["settings.toml"]),
        ({"settings.toml": "value"}),
    ],
)
def test_settings_filepath_type_fails(settings_name, settings_filepath, value):
    with pytest.raises(TypeError):
        _ = Settings(settings_name, filepath=value)


## End Type Tests
def test_settings_sets_missing_keys_in_defaults(settings_name, settings_filepath):
    defaults = default_settings_normal_format.copy()
    settings = Settings(settings_name, filepath=settings_filepath, defaults=defaults)
    assert settings.get("foo") is None

    defaults["foo"] = "bar"
    new_settings = Settings(settings_name, filepath=settings_filepath, defaults=defaults)

    assert new_settings.get("foo") == "bar"
    for k, v in defaults.items():
        assert new_settings.get(k) == v


def test_settings_get_and_set_methods_success(settings_name, settings_filepath):
    settings = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)

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


def test_settings_overrides_existing_settings(settings_name, settings_filepath):
    settings = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)

    # Set an initial value
    settings.set("name", "InitialName")
    assert settings.get("name") == "InitialName"

    # Override the value
    settings.set("name", "NewName")
    assert settings.get("name") == "NewName"


def test_settings_handles_non_existent_keys(settings_name, settings_filepath):
    settings = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)

    assert settings.get("non_existent_key") is None


def test_settings_handles_empty_settings_file(settings_name, settings_filepath):
    # Create an empty settings file
    settings_filepath.parent.mkdir(parents=True, exist_ok=True)
    with Path.open(settings_filepath, "w") as f:
        f.write("")
    settings = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)
    # Check that default settings are applied
    for k, v in default_settings_normal_format.items():
        assert settings.get(k) == v


def test_settings_handles_creating_directories_for_new_files(settings_name, settings_filepath):
    parent_dir = settings_filepath.parent

    assert not parent_dir.exists(), "Parent directory should not exist before test"

    _ = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)
    assert parent_dir.exists(), "Parent directory should be created by Settings class"


def test_settings_saves_settings_to_file(settings_name, settings_filepath):
    settings = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)

    # Set some values
    settings.set("name", "TestName")
    settings.set("mood", "TestMood")

    # Reload the settings to check if values are saved
    new_settings = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)
    assert new_settings.get("name") == "TestName"
    assert new_settings.get("mood") == "TestMood"


def test_settings_with_different_cases_in_key(settings_name, settings_filepath):
    settings = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)
    settings["caseCheck"] = "value"

    assert settings["caseCheck"] == "value"
    assert settings["casecheck"] is None


def test_settings_no_default_settings(settings_name, settings_filepath):
    # Test with no default settings
    settings = Settings(settings_name, filepath=settings_filepath)

    # Check that no settings are set initially
    assert settings.get("name") is None
    assert settings.get("mood") is None

    # Set a value and check if it persists
    settings.set("name", "NoDefaultName")
    assert settings.get("name") == "NoDefaultName"

    # Reload the settings to check if the value is saved
    new_settings = Settings(settings_name, filepath=settings_filepath)
    assert new_settings.get("name") == "NoDefaultName"


def test_settings_with_getitem_and_setitem(settings_name, settings_filepath):
    settings = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)

    # Test __getitem__
    assert settings["settings.name"] == "MyName"
    assert settings["settings.mood"] == "MyMood"
    assert settings["dictionary.key1"] == "value1"

    # Test __setitem__
    settings["settings.name"] = "NewName"
    assert settings["settings.name"] == "NewName"

    settings["new_key"] = "new_value"
    assert settings["new_key"] == "new_value"


def test_settings_updates_defaults_with_nested_dict(settings_name, settings_filepath: Path):
    defaults = default_settings_nested_format.copy()
    settings = Settings(settings_name, filepath=settings_filepath, defaults=defaults)
    assert settings.get("dictionary.subdictionary.key3") is None
    assert settings["dictionary.subdictionary.key3"] is None

    defaults["dictionary.subdictionary.key3"] = "subvalue3"

    # Access a nested value
    new_settings = Settings(settings_name, filepath=settings_filepath, defaults=defaults)
    assert new_settings.get("dictionary.subdictionary.key3") == "subvalue3"
    assert new_settings["dictionary"]["subdictionary"]["key3"] == "subvalue3"


def test_settings_initializes_defaults_with_nested_dict(settings_name, settings_filepath):
    settings = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_nested_format)
    assert settings.get("settings.name") == "MyName"
    assert settings.get("settings.mood") == "MyMood"
    assert settings["settings"]["name"] == "MyName"
    assert settings["settings"]["mood"] == "MyMood"
    assert settings.get("dictionary") is not None
    assert settings.get("dictionary.key1") == "value1"
    assert settings.get("dictionary.subdictionary") is not None
    assert settings.get("dictionary.subdictionary.key1") == "subvalue1"


def test_settings_sets_default_settings_of_nested_dictionaries_if_not_present(settings_name, settings_filepath):
    settings = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_nested_format)
    assert settings.get("settings.mood") == "MyMood"
    assert settings.get("settings.face") is None

    new_default_settings = default_settings_nested_format.copy()
    new_default_settings["settings.face"] = "round"

    new_settings = Settings(settings_name, filepath=settings_filepath, defaults=new_default_settings)

    assert settings.get("settings.face") == "round"
    assert new_settings.get("settings.face") == "round"


def test_settings_always_reload_true(settings_name, settings_filepath):
    settings = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)

    assert settings.get("settings.name") == "MyName"

    # Change the settings file seperatrely
    settings2 = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)
    settings2.set("settings.name", "NewName")

    # Verify that the change is reflected in the original settings object
    assert settings.get("settings.name") == "NewName"


def test_settings_always_reload_false(settings_name, settings_filepath):
    settings = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)
    settings.always_reload = False

    assert settings.get("settings.name") == "MyName"

    # Change the settings file seperatrely
    settings2 = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)
    settings2.set("settings.name", "NewName")


def test_settings_dynamic_reload_true_set(settings_name, settings_filepath):
    settings = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)

    assert settings.get("settings.name") == "MyName"

    # Change the settings file seperatrely
    settings2 = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)
    settings2.set("settings.name", "NewName3")

    # Verify that the change is reflected in the original settings object
    settings2.set("settings.mood", "MyMood")
    assert settings.get("settings.name") == "NewName3"


def test_settings_dynamic_reload_false_set(settings_name, settings_filepath):
    settings = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)
    settings.always_reload = False

    assert settings.get("settings.name") == "MyName"

    # Change the settings file seperatrely
    settings2 = Settings(settings_name, filepath=settings_filepath, defaults=default_settings_normal_format)
    settings2.set("settings.name", "NewName3")

    # Verify that the change is reflected in the original settings object
    settings2.set("settings.mood", "MyMood")
    assert settings.get("settings.name") == "MyName"

    settings.set("settings.name", "NewName4")
    assert settings.get("settings.name") == "NewName4"


def test_settings_read_only_true(settings_name, settings_filepath):
    settings = Settings(
        settings_name,
        filepath=settings_filepath,
        defaults=default_settings_normal_format,
        read_only=True,
    )

    assert settings.read_only is True
    with pytest.raises(PermissionError):
        settings.set("settings.name", "NewName")


# Verify that the change is reflected in the original settings object
def test_settings_repr_returns_expected_string(settings_name, settings_filepath):
    settings = Settings(
        settings_name,
        filepath=settings_filepath,
        defaults=default_settings_normal_format,
    )
    expected = f"Settings stored at: {settings_filepath}"
    assert repr(settings) == expected


def test_settings_stores_in_home_directory_if_no_filepath(temp_home):
    settings = Settings(temp_home["name"])
    assert temp_home["path"].exists() is True
