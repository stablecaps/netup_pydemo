import io
import sys
import pytest
from unittest import TestCase, mock
from unittest.mock import patch, call
from components.printers import ColourPrinter


def setup_blessings_term(mocker):
    term = mocker.patch("components.printers.Terminal").return_value

    green = mocker.PropertyMock()
    yellow = mocker.PropertyMock()
    red = mocker.PropertyMock()
    bold = mocker.PropertyMock()
    underline = mocker.PropertyMock()
    normal = mocker.PropertyMock()

    type(term).green = green
    type(term).yellow = yellow
    type(term).red = red
    type(term).bold = bold
    type(term).underline = underline
    type(term).normal = normal

    return {
        "green": green,
        "yellow": yellow,
        "red": red,
        "bold": bold,
        "underline": underline,
        "normal": normal,
    }


def test_fmt_bold_red(mocker):
    term_dict = setup_blessings_term(mocker)

    prt = ColourPrinter()
    prt.fmt_bold_red(mystr="testing fmt_bold_red...")

    assert term_dict["red"].call_count == 1
    assert term_dict["bold"].call_count == 1
    assert term_dict["normal"].call_count == 1


def test_fmt_bold_yellow(mocker):
    term_dict = setup_blessings_term(mocker)

    prt = ColourPrinter()
    prt.fmt_bold_yellow(mystr="testing fmt_bold_red...")

    assert term_dict["yellow"].call_count == 1
    assert term_dict["bold"].call_count == 1
    assert term_dict["normal"].call_count == 1


long_char_dict = {
    "jackie": "yobolo",
    "p": "dalston8910",
    "q": "dalston8910",
    "a long string with spaces": "89",
}


@pytest.mark.parametrize(
    "mydict,mode,expected",
    [
        (long_char_dict, "keys", 25),
        (long_char_dict, "values", 11),
    ],
)
def test_get_longest_str_in_dict(mydict, mode, expected):

    prt = ColourPrinter()
    assert prt.get_longest_str_in_dict(mydict, mode) == expected


ok_error_dict = {
    "key1": "OK - something",
    "key2": " OK - somethingelse",
    "key3": "diffy",
    "key4": "uboat",
}


def test_fmt_ok_error(mocker, test_dict=ok_error_dict):
    term_dict = setup_blessings_term(mocker)

    prt = ColourPrinter()
    prt.fmt_ok_error(results_dict=test_dict)

    assert term_dict["green"].call_count == 2 * 2
    assert term_dict["red"].call_count == 1 * 2
    assert term_dict["bold"].call_count == 2 * 2
    assert term_dict["normal"].call_count == 3 * 2


def test_fmt_keyok_valerror(mocker, test_dict=ok_error_dict):
    term_dict = setup_blessings_term(mocker)

    prt = ColourPrinter()
    prt.fmt_keyok_valerror(results_dict=test_dict)

    assert term_dict["green"].call_count == 1 * 4
    assert term_dict["red"].call_count == 1 * 4
    assert term_dict["bold"].call_count == 1 * 4
    assert term_dict["normal"].call_count == 2 * 4


dns_val_dict = {
    "key1": "The DNS - something",
    "key2": " The DNS - somethingelse",
    "key3": "diffy",
    "key4": "uboat",
}


def test_fmt_ok_error_dns(mocker, test_dict=dns_val_dict):
    term_dict = setup_blessings_term(mocker)

    prt = ColourPrinter()
    prt.fmt_ok_error_dns(results_dict=test_dict)

    assert term_dict["green"].call_count == 4
    assert term_dict["red"].call_count == 1
    assert term_dict["bold"].call_count == 4
    assert term_dict["normal"].call_count == 5


def test_fmt_bold_col1(mocker, test_dict=dns_val_dict):
    term_dict = setup_blessings_term(mocker)

    prt = ColourPrinter()
    prt.fmt_bold_col1(results_dict=test_dict)

    assert term_dict["green"].call_count == 4
    assert term_dict["bold"].call_count == 4
    assert term_dict["normal"].call_count == 4


def test_print_dict_results(mocker, test_dict=dns_val_dict):
    term_dict = setup_blessings_term(mocker)

    prt = ColourPrinter()
    prt.print_dict_results(
        results_dict=test_dict, header="test header", fmt_func_str="fmt_ok_error"
    )

    assert prt.fmt_ok_error.call_count == 1
    assert term_dict["bold"].call_count == 5
    assert term_dict["underline"].call_count == 4
    assert term_dict["normal"].call_count == 4