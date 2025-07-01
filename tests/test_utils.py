import pytest

from mooch.settings.utils import get_nested, is_valid_key, set_nested


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        ("DEBUG", True),
        ("debug-mode", True),
        ("db.host", False),
        ('"db.host"', False),
        ("db host", False),
        ("'db host'", False),
        ('"bad"key"', False),
        ("'bad'key'", False),
        ("simple_key", True),
        ("123key", True),
        ("key-with-dash", True),
        ("key with space", False),
        ('"key with space in nested quotes"', False),
        ('"key with \n newline"', False),
        ("'single'quote'", False),
        ("'valid key'", False),
        ('"valid key"', False),
        ('""', False),
        ("", False),
    ],
)
def test_is_valid_key(key, expected):
    assert is_valid_key(key) == expected


def test_get_nested_invalid_key():
    d = {"a": {"b": {"c": 1}}}
    with pytest.raises(ValueError):  # noqa: PT011
        get_nested(d, "a.b ")
    with pytest.raises(ValueError):  # noqa: PT011
        get_nested(d, "b ")
    with pytest.raises(ValueError):  # noqa: PT011
        get_nested(d, "b .c.d.a")


def test_set_nested_invalid_key():
    d = {"a": {"b": {"c": 1}}}
    with pytest.raises(ValueError):
        set_nested(d, "a.b .c", 2)
    with pytest.raises(ValueError):
        set_nested(d, "b ", 2)
    with pytest.raises(ValueError):
        set_nested(d, "b .c.d.a", 2)
    with pytest.raises(ValueError):
        set_nested(d, "a.b.c ", 2)


@pytest.mark.parametrize(
    "initial, key, value, expected",
    [
        ({}, "a.b.c", 1, {"a": {"b": {"c": 1}}}),
        ({"a": {}}, "a.b", 2, {"a": {"b": 2}}),
        ({"a": {"b": 3}}, "a.b", 4, {"a": {"b": 4}}),
        ({}, "x", 5, {"x": 5}),
        ({"a": {"b": {"c": 1}}}, "a.b.d", 6, {"a": {"b": {"c": 1, "d": 6}}}),
    ],
)
def test_set_nested(initial, key, value, expected):
    d = initial.copy()
    set_nested(d, key, value)
    assert d == expected


@pytest.mark.parametrize(
    "d, key, expected",
    [
        ({"a": {"b": {"c": 1}}}, "a.b.c", 1),
        ({"a": {"b": 2}}, "a.b", 2),
        ({"x": 5}, "x", 5),
        ({"a": {"b": {"c": 1}}}, "a.b", {"c": 1}),
        ({"a": {"b": {"c": 1}}}, "a.b.c.d", None),
        ({}, "foo.bar", None),
        ({"a": 1}, "a.b", None),
    ],
)
def test_get_nested(d, key, expected):
    assert get_nested(d, key) == expected


def test_set_nested_with_custom_separator():
    d = {}
    set_nested(d, "a|b|c", 10, sep="|")
    assert d == {"a": {"b": {"c": 10}}}


def test_get_nested_with_custom_separator():
    d = {"a": {"b": {"c": 42}}}
    assert get_nested(d, "a|b|c", sep="|") == 42


def test_set_nested_overwrites_non_dict():
    d = {"a": 1}
    set_nested(d, "a.b", 2)
    assert d == {"a": {"b": 2}}


def test_get_nested_returns_none_for_non_dict():
    d = {"a": 1}
    assert get_nested(d, "a.b") is None
