import sys
from blessings import Terminal


def fmt_bold_yellow(mystr):
    """
    Return a string formatted in bold yellow.
    """
    term = Terminal()

    print(f"\n{term.yellow}{term.bold}{mystr}{term.normal}")


# class ColourPrinter:
#     def __init__(self):
#         self.term = Terminal()

#     def fmt_bold_yellow(self, mystr):
#         """
#         Return a string formatted in bold yellow.
#         """

#         print(f"\n{self.term.yellow}{self.term.bold}{mystr}{self.term.normal}")


# if __name__ == "__main__":
#     print("Running print in class")
#     prt = ColourPrinter()

#     prt.fmt_bold_yellow(mystr="This is the class version")

#     fmt_bold_yellow(mystr="This is the function version")


# # Installaltion
# python3.8 -m venv venv
# source venv/bin/activate
# pip install blessings  # (Terminal) version 1.7

### Ideally I need:
# 1. to be able to write tests for noth the class and function versions
# 2. I need to be able to check how many times term is called,
# 3. example term.yellow, term.bold, etc

### My effort so far:
from unittest.mock import patch, call


# @patch("builtins.print")
# def test_fmt_bold_yellow(mocked_print):
#     fmt_bold_yellow(mystr="testing fmt_bold_yellow...")

#     assert mocked_print.mock_calls == [call("\ntesting fmt_bold_yellow...")]
#     assert mocked_print.mock_calls == [call("\ntesting fmt_bold_yellow...")]


## Using pytest:
# pip install pytest pytest-mock

# from components.printers import *
# from components.printers import ColourPrinter
import pytest
from unittest import TestCase, mock

# prt = ColourPrinter()


def test_fmt_bold_yellow(mocker):
    term = mocker.patch("tests.test_help.Terminal").return_value
    yellow = mocker.PropertyMock()
    type(term).yellow = yellow

    fmt_bold_yellow(mystr="testing fmt_bold_yellow...")

    assert yellow.call_count == 1
