import io
import sys
import pytest
from unittest import TestCase, mock
from unittest.mock import patch, call
from components.printers import ColourPrinter, Terminal


def test_fmt_bold_red(mocker):
    ### Parch terminal
    term = mocker.patch("tests.test_printers.Terminal").return_value
    # term = mocker.patch("tests.test_printers.prt.__self__.term").return_value

    red = mocker.PropertyMock()

    type(term).red = red
    prt = ColourPrinter()
    prt.fmt_bold_red(mystr="testing fmt_bold_red...")

    assert red.call_count == 1
    # assert normal.call_count == 1

    # assert mocker.mock_calls == [call("\ntesting fmt_bold_red...")]


# @patch("builtins.print")
# @mock.patch.object(prt.ColourPrinter, "fmt_bold_yellow")
# def test_fmt_bold_yellow(mocked_print):

#     cpr = prt.ColourPrinter

#     cpr.fmt_bold_yellow(mystr="testing fmt_bold_yellow...")
#     mock.assert_called()

# assert mocked_print.mock_calls == [call("\ntesting fmt_bold_yellow...")]
