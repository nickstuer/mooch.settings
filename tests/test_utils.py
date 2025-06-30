import pytest

from mooch.settings.utils import get_nested, set_nested


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
