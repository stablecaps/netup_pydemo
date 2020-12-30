import io
import sys
import pytest
import unittest
from unittest import TestCase, mock
from unittest.mock import patch, call, Mock
from parameterized import parameterized
import components.helpers as helpo
import components.traceroute as trace
from tests.data_for_traceroute import *


# def test_run_traceroute(mocker):
#     mock_run_cmd_with_output = mocker.patch("components.helpers.run_cmd_with_output")
#     mock_run_cmd_with_output.return_value = b"some bytes string\n"
#     #
#     mock_process_subp_output = mocker.patch("components.helpers.process_subp_output")
#     mock_process_subp_output.return_value = [["some", "bytes", "bytes"]]

#     trace = mocker.patch("components.traceroute.run_traceroute")
#     trace.return_value = b"some bytes string\n"

#     trace.run_traceroute()

#     assert mock_run_cmd_with_output.call_count == 1
#     assert mock_process_subp_output.call_count == 1


# @patch("components.traceroute.run_traceroute")
@patch("components.traceroute.run_cmd_with_output")
@patch("components.traceroute.process_subp_output")
def test_run_traceroute(mrun_cmd_with_output, mprocess_subp_output):
    mrun_cmd_with_output.return_value = b"some bytes string\n"

    yabba = trace.run_traceroute()

    # assert mrun_traceroute.call_count == 1
    assert mrun_cmd_with_output.call_count == 1


# class MyTest(TestCase):
#     @patch("components.helpers.run_cmd_with_output")
#     def test_f2_2(self, some_func):
#         some_func.return_value = (20, False)
#         yabba = trace.run_traceroute()
#         self.assertEqual((num, stat), (40, False))