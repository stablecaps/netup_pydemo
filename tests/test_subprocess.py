# import pytest
# import unittest
# from unittest import TestCase, mock
# from unittest.mock import patch, call, Mock
# from parameterized import parameterized
# from requests.exceptions import HTTPError, Timeout

# import components.helpers as helpo
# from tests.data_for_subprocess import *

# data_shlex_convert = []


# @pytest.mark.parametrize(
#     "comm_str,expected",
#     [
#         ("ls    -lha", ["ls", "-lha"]),
#         ("route -n", ["route", "-n"]),
#         (" ls", ["ls"]),
#         (
#             "ls -a  --colour  -k  --group-directories-first    *.py",
#             ["ls", "-a", "--colour", "-k", "--group-directories-first", "*.py"],
#         ),
#     ],
# )
# def test_shlex_convert_str_2list(comm_str, expected):
#     assert helpo.shlex_convert_str_2list(comm_str=comm_str) == expected


# def test_run_cmd_with_output():
#     assert helpo.run_cmd_with_output(comm_str="lsfakecommand") == None
#     assert isinstance(str(helpo.run_cmd_with_output(comm_str="ls")), str) == True
#     assert helpo.run_cmd_with_output(comm_str="echo cheese") == b"cheese\n"


# def test_run_cmd_with_errorcode():
#     assert helpo.run_cmd_with_errorcode(comm_str="lsfakecommand") == False
#     assert helpo.run_cmd_with_errorcode(comm_str="ls") == True
#     assert helpo.run_cmd_with_errorcode(comm_str="echo cheese") == True


# # (comm_output1, "\t", ["", " "], comm_expected1)
# @pytest.mark.parametrize(
#     "cmd_output,delimiter,exclude_list,expected",
#     [
#         (b"hello i love you\n", " ", ["", " "], [["hello", "i", "love", "you"]]),
#         (b"hello i love you\n", "\t", ["", " "], [["hello i love you"]]),
#         (b"hello i love you\n", "i", ["", " "], [["hello", "love you"]]),
#         (b"hello i love you\n", "i", ["", " ", "hello"], [["hello", "love you"]]),
#         (b"hello i love you\n", "i", ["", " ", "hello"], [["hello", "love you"]]),
#         (b"hello i love you\n", " ", ["", " ", "hello", "i", "love", "you"], []),
#         (
#             b"hello    i love you\n",
#             "o",
#             ["", " "],
#             [["hell", "i l", "ve y", "u"]],
#         ),
#         (b"hello     i love you\n", "\t", ["", " "], [["hello     i love you"]]),
#         (b"hello i     love \tyou\n", "\t", ["", " "], [["hello i     love", "you"]]),
#         (comm_output1, ": ", ["", " "], comm_expected1),
#     ],
# )
# def test_process_subp_output(cmd_output, delimiter, exclude_list, expected):
#     assert helpo.process_subp_output(cmd_output, delimiter, exclude_list) == expected