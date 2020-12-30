"""Test traceroute module."""

from unittest.mock import patch
import pytest
import components.traceroute as trace
import tests.data_for_traceroute as dat


@patch("components.traceroute.run_cmd_with_output")
@patch("components.traceroute.process_subp_output")
def test_run_traceroute(mrun_cmd_with_output, mprocess_subp_output):
    mrun_cmd_with_output.return_value = b"some bytes string\n"

    mprocess_subp_output.return_value = [["some", "bytes", "bytes"]]

    trace.run_traceroute()

    assert mrun_cmd_with_output.call_count == 1
    assert mprocess_subp_output.call_count == 1


@patch("components.traceroute.run_cmd_with_output")
@patch("components.traceroute.ColourPrinter")
def test_run_traceroute_none(mrun_cmd_with_output, mprt):
    mrun_cmd_with_output.return_value = None

    trace.run_traceroute()

    assert mprt.call_count == 1


@pytest.mark.parametrize(
    "mylist,expected",
    [
        (
            [
                "44",
                "192.168.0.33",
                "44",
                "-0.479867456341684",
                "228.75.92.210",
                "208.204.117.25",
                "8909678",
                "73.222.12.250",
                "-0.364563346546",
                "170.157.252.103",
                "96564676135.364",
                "91.237.77.113",
                "45787",
            ],
            [
                44.0,
                44.0,
                -0.479867456341684,
                8909678.0,
                -0.364563346546,
                96564676135.364,
                45787.0,
            ],
        ),
        (["8.8.8.8", "(8.8.8.8)", "42"], [42.0]),
        (["192.168.10.25", "67", "(192.168.10.25)", "42"], [67.0, 42.0]),
        (["10.1.10.25", "67", "(92.18.1.255)", "42"], [67.0, 42.0]),
    ],
)
def test_rm_ipaddr_from_list_of_floats(mylist, expected):
    assert trace.rm_ipaddr_from_list_of_floats(mylist=mylist) == expected


def test_rm_ipaddr_from_list_of_floats_exception():
    mylist = [9, 64.0]
    with pytest.raises(Exception):
        trace.rm_ipaddr_from_list_of_floats(mylist=mylist)


@pytest.mark.parametrize(
    "trace_fmt,expected",
    [
        (
            dat.sample_trace_fmt1,
            (dat.sample_fmted_holder, dat.sample_trace_times, dat.sample_trace_head1),
        ),
        (
            dat.sample_calc_avgs1,
            (
                dat.sample_calc_avgs1_result,
                dat.sample_calc_avgs1_times,
                dat.sample_calc_avgs1_header,
            ),
        ),
    ],
)
def test_get_traceroute_data_structs(trace_fmt, expected):

    assert trace.get_traceroute_data_structs(trace_fmt=trace_fmt) == expected


@pytest.mark.parametrize(
    "total_times_ms,fmted_holder,expected",
    [
        (
            dat.total_times_ms1,
            dat.fmted_holder1,
            (dat.large_latency_idx1, dat.large_latency_str1),
        ),
        (
            dat.total_times_ms2,
            dat.fmted_holder2,
            (dat.large_latency_idx2, dat.large_latency_str2),
        ),
        (
            dat.total_times_ms3,
            dat.fmted_holder3,
            (dat.large_latency_idx3, dat.large_latency_str3),
        ),
        ([], [[]], ([], [])),
    ],
)
def test_get_high_latency_hop_data(total_times_ms, fmted_holder, expected):

    assert (
        trace.get_high_latency_hop_data(
            total_times_ms=total_times_ms, fmted_holder=fmted_holder
        )
        == expected
    )


@pytest.mark.parametrize(
    "large_latency_idx,expected",
    [
        ([1, 3, 5, 6, 9], True),
        ([9, 4, 6, 3, 8], True),
        ([62, 7, 87, 9], False),
        ([], False),
        ([-5], True),
    ],
)
def test_is_local_latency_high(large_latency_idx, expected):
    assert trace.is_local_latency_high(large_latency_idx=large_latency_idx) == expected


# def test_eval_high_hop_latency_msg():
