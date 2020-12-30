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


@patch("components.traceroute.run_cmd_with_output")
@patch("components.traceroute.process_subp_output")
def test_run_traceroute(mrun_cmd_with_output, mprocess_subp_output):
    mrun_cmd_with_output.return_value = b"some bytes string\n"

    mprocess_subp_output.return_value = [["some", "bytes", "bytes"]]

    yabba = trace.run_traceroute()

    assert mrun_cmd_with_output.call_count == 1
    assert mprocess_subp_output.call_count == 1


# class MyTest(TestCase):
#     @patch("components.helpers.run_cmd_with_output")
#     def test_f2_2(self, some_func):
#         some_func.return_value = (20, False)
#         yabba = trace.run_traceroute()
#         self.assertEqual((num, stat), (40, False))