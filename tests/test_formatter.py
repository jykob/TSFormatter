from typing import Any, Callable

import pytest
from tsformatter import formatter

simples = (
    pytest.param(formatter.img, "IMG", "https://i.imgur.com/ml09ccU.png", id="test_img"),
    pytest.param(formatter.bold, "B", "Test string", id="test_bold"),
    pytest.param(formatter.italic, "I", "Test string", id="test_italic"),
    pytest.param(formatter.underline, "U", "Test string", id="test_underline"),
    pytest.param(formatter.strike, "S", "Test string", id="test_strike"),
    pytest.param(formatter.center, "CENTER", "Test string", id="test_center"),
    pytest.param(formatter.left, "LEFT", "Test string", id="test_left"),
    pytest.param(formatter.right, "RIGHT", "Test string", id="test_right"),
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
    assert formatter.link(*args) == expected


@pytest.mark.parametrize(
    ("args", "expected"),
    (
        pytest.param((24, "Test string"), "[SIZE=24]Test string[/SIZE]", id="test_absolute"),
        pytest.param(("-4", "Test string"), "[SIZE=-4]Test string[/SIZE]", id="test_relative_negative"),
        pytest.param(("+2", "Test string"), "[SIZE=+2]Test string[/SIZE]", id="test_relative_positive"),
    ),
)
def test_size(args: tuple[int | str, str], expected: str):
    assert formatter.size(*args) == expected


@pytest.mark.parametrize(
    ("args", "expected"),
    (
        pytest.param(("#fff", "Test string"), "[COLOR=#fff]Test string[/COLOR]", id="test_hex_triplet_3"),
        pytest.param(("#686868", "Test string"), "[COLOR=#686868]Test string[/COLOR]", id="test_hex_triplet_6"),
        pytest.param(("Chartreuse", "Test string"), "[COLOR=Chartreuse]Test string[/COLOR]", id="test_html_name"),
    ),
)
def test_color(args: tuple[str, str], expected: str):
    assert formatter.color(*args) == expected


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
def test_list(list_items: list[str], kwargs: dict[str, str | None], expected: str):
    assert formatter.list_(list_items, **kwargs) == expected


def test_table_header_row():
    row = formatter.table_header_row(map(str, range(3)))
    assert row == "[TR][TH]0[/TH][TH]1[/TH][TH]2[/TH][/TR]"


def test_table_row():
    row = formatter.table_row(map(str, range(3)))
    assert row == "[TR][TD]0[/TD][TD]1[/TD][TD]2[/TD][/TR]"


def test_table():
    formatted_table = formatter.table(
        formatter.table_header_row(map(str, range(3))),
        formatter.table_row(map(str, range(3))),
        formatter.table_row(map(str, range(3))),
    )

    assert formatted_table == (
        "[TABLE]\n"
        "[TR][TH]0[/TH][TH]1[/TH][TH]2[/TH][/TR]\n"
        "[TR][TD]0[/TD][TD]1[/TD][TD]2[/TD][/TR]\n"
        "[TR][TD]0[/TD][TD]1[/TD][TD]2[/TD][/TR]\n"
        "[/TABLE]"
    )
