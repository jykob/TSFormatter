from __future__ import annotations

from typing import Callable, Literal

import pytest

import tsformatter

simples = (
    pytest.param(tsformatter.img, "IMG", "https://i.imgur.com/ml09ccU.png", id="test_img"),
    pytest.param(tsformatter.bold, "B", "Test string", id="test_bold"),
    pytest.param(tsformatter.italic, "I", "Test string", id="test_italic"),
    pytest.param(tsformatter.underline, "U", "Test string", id="test_underline"),
    pytest.param(tsformatter.strike, "S", "Test string", id="test_strike"),
    pytest.param(tsformatter.center, "CENTER", "Test string", id="test_center"),
    pytest.param(tsformatter.left, "LEFT", "Test string", id="test_left"),
    pytest.param(tsformatter.right, "RIGHT", "Test string", id="test_right"),
)


@pytest.mark.parametrize(("func", "tag", "string"), simples)
def test_simples(func: Callable[[str], str], tag: str, string: str):
    results = func(string)
    assert results == f"[{tag}]{string}[/{tag}]"


@pytest.mark.parametrize(
    ("args", "expected"),
    (
        pytest.param(
            ("https://www.teamspeak.com/en/",),
            "[URL]https://www.teamspeak.com/en/[/URL]",
            id="test_url_alone",
        ),
        pytest.param(
            ("https://www.teamspeak.com/en/", "TeamSpeak"),
            "[URL=https://www.teamspeak.com/en/]TeamSpeak[/URL]",
            id="test_link_text",
        ),
    ),
)
def test_link(args: tuple[str, str | None], expected: str):
    assert tsformatter.link(*args) == expected


@pytest.mark.parametrize(
    ("args", "expected"),
    (
        pytest.param((24, "Test string"), "[SIZE=24]Test string[/SIZE]", id="test_absolute"),
        pytest.param(
            ("-4", "Test string"), "[SIZE=-4]Test string[/SIZE]", id="test_relative_negative"
        ),
        pytest.param(
            ("+2", "Test string"), "[SIZE=+2]Test string[/SIZE]", id="test_relative_positive"
        ),
    ),
)
def test_size(args: tuple[int | str, str], expected: str):
    assert tsformatter.size(*args) == expected


@pytest.mark.parametrize(
    ("args", "expected"),
    (
        pytest.param(
            ("#fff", "Test string"), "[COLOR=#fff]Test string[/COLOR]", id="test_hex_triplet_3"
        ),
        pytest.param(
            ("#686868", "Test string"),
            "[COLOR=#686868]Test string[/COLOR]",
            id="test_hex_triplet_6",
        ),
        pytest.param(
            ("Chartreuse", "Test string"),
            "[COLOR=Chartreuse]Test string[/COLOR]",
            id="test_html_name",
        ),
    ),
)
def test_color(args: tuple[str, str], expected: str):
    assert tsformatter.color(*args) == expected


@pytest.mark.parametrize(
    ("list_items", "kwargs", "expected"),
    (
        pytest.param(
            list(map(str, range(3))),
            dict(style=None),
            "[LIST]\n[*]0\n[*]1\n[*]2\n[/LIST]",
            id="test_list",
        ),
        pytest.param(
            list(map(str, range(3))),
            dict(style="A"),
            "[LIST=A]\n[*]0\n[*]1\n[*]2\n[/LIST]",
            id="test_list_style",
        ),
    ),
)
def test_list(
    list_items: list[str],
    kwargs: dict[str, Literal["1", "a", "i", "A", "I"] | None],
    expected: str,
):
    assert tsformatter.list_(list_items, **kwargs) == expected


def test_table_header_row():
    row = tsformatter.table_header_row(map(str, range(3)))
    assert row == "[TR][TH]0[/TH][TH]1[/TH][TH]2[/TH][/TR]"


def test_table_row():
    row = tsformatter.table_row(map(str, range(3)))
    assert row == "[TR][TD]0[/TD][TD]1[/TD][TD]2[/TD][/TR]"


def test_table():
    formatted_table = tsformatter.table(
        tsformatter.table_header_row(map(str, range(3))),
        tsformatter.table_row(map(str, range(3))),
        tsformatter.table_row(map(str, range(3))),
    )

    assert formatted_table == (
        "[TABLE]\n"
        "[TR][TH]0[/TH][TH]1[/TH][TH]2[/TH][/TR]\n"
        "[TR][TD]0[/TD][TD]1[/TD][TD]2[/TD][/TR]\n"
        "[TR][TD]0[/TD][TD]1[/TD][TD]2[/TD][/TR]\n"
        "[/TABLE]"
    )
