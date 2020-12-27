"""Traceroute module."""

import sys
import re
from components.helpers import (
    run_cmd_with_output,
    process_subp_output,
    list_of_nelem_lists_2dict,
)
from components.printers import ColourPrinter
from typing import Any, List, Tuple, Union

LARGE_THRESHOLD = 150
prt = ColourPrinter()


def run_traceroute() -> List[List[str]]:
    """
    Runs traceroute via subprocess.
    """

    print("\nRunning Traceroute..")

    traceroute_comm = "traceroute -q 3  8.8.8.8"

    # TODO: sort out granularity of this error by processing traceroute exit codes properly
    trace = run_cmd_with_output(comm_str=traceroute_comm)
    prt.exit_with_bye_if_none(check_var=trace, cmd_run="traceroute -q 3  8.8.8.8")

    trace_fmt = process_subp_output(
        cmd_output=trace, delimiter=" ", exclude_list=["", " ", "*", "ms"]
    )

    return trace_fmt


def get_traceroute_data_structs(
    trace_fmt: List[List[str]],
) -> Tuple[List[List[Union[str, float]]], List[float], str]:
    """
    Macro function that:
        1. Processes traceroute header (header) & main body
        2. Returns a list of list containing traceroute output data with averaged times (fmted_holder)
        3. Retrns a flat list with traceroute with averaged timings in ms
    """

    ip_addr_re = re.compile(r"^\(?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\)?$")

    fmted_holder = []
    total_times_ms = []
    for sublist in trace_fmt:
        if sublist[0] == "traceroute":
            header = " ".join(sublist)
        else:
            if len(sublist) > 1:
                hop = sublist[0]
                name = sublist[1]
                ip_addr = sublist[2]
                fmt_row = [hop, name, ip_addr]

                calc_list = [
                    float(elem) for elem in sublist[3:] if not ip_addr_re.match(elem)
                ]

                len_calc = len(calc_list)
                avg_time = round(sum(calc_list) / len_calc, 3)
                fmt_row.append(avg_time)
                fmted_holder.append(fmt_row)

                total_times_ms.append(avg_time)

    return (fmted_holder, total_times_ms, header)


def get_high_latency_hop_data(
    total_times_ms: List[float], fmted_holder: List[List[Union[str, float]]]
) -> Tuple[List[Any], List[Any]]:
    """
    Detects which averaged timings are > LARGE_THRESHOLD.
    Returns:
        large_latency_str: a list containing the treaceroute row
        large_latency_idx: a list containing traceroute indexes
    """

    large_latency_idx = []
    large_latency_str = []

    for idx, hop_time in enumerate(total_times_ms):
        if hop_time > LARGE_THRESHOLD:
            large_latency_idx.append(int(fmted_holder[idx][0]))
            large_latency_str.append(fmted_holder[idx])

    return (large_latency_idx, large_latency_str)


def gen_fmted_str_holder(
    fmted_holder: List[List[Union[str, float]]]
) -> List[List[str]]:
    """
    Converts float times in traceroute results (list of lists) into a string with units.
    """

    fmted_holder_str = []
    for row in fmted_holder:
        # print(row)
        time_str = f"{str(row[-1])} ms average"
        row[-1] = time_str
        fmted_holder_str.append(row)

    return fmted_holder_str


def is_local_latency_high(large_latency_idx):
    """
    Detects whether latency in the first few hops is high.
    """

    for idx_val in large_latency_idx:
        if idx_val <= 3:
            return True

    return False


def eval_high_hop_latency_msg(
    large_latency_str: List[Any], large_latency_idx: List[Any]
) -> None:
    """
    Prints messages to screen identifying hops with high latency and potential causes.
    """

    if len(large_latency_str) > 0:
        largehop_dict = list_of_nelem_lists_2dict(
            list_of_nelem_lists=large_latency_str, keyn=2, valn=-1
        )

        fmt_bold_red(mystr="Hops with large latencies found:")
        print_dict_results(
            results_dict=largehop_dict,
            header=f"Hops with large latency (> {LARGE_THRESHOLD} ms)",
            fmt_func_str="fmt_keyok_valerror",
        )

        local_hop_high = is_local_latency_high(large_latency_idx=large_latency_idx)
        if local_hop_high:
            fmt_bold_red(
                mystr=(
                    "! High latencies near traceroute start.\n"
                    + "Issues are likely to be present in your local network or with your ISP"
                )
            )


def eval_final_msg(final_hop: str, len_fmted_holder_str: int) -> None:
    """
    Prints messages to screen identifying  whether the target destination was hit or not with
    potential causes. (Unfinished)
    """

    # TODO: Evaluate whether final time is *** or a number
    name_hit = True
    if final_hop == "dns.google":
        hit_str = "Managed to hit dns.google DNS name"
    elif final_hop == "8.8.8.8":
        # TODO: establish whether traceroute falls back to ip address if it fails on name (my router is flaky)
        hit_str = "Managed to hit 8.8.8.8 IP Add"  # but not dns.google DNS name"
    else:
        hit_str = "Failed to hit dns.google name or 8.8.8.8 IP."
        name_hit = False

    #########################################################
    if len_fmted_holder_str < 2:
        hit_str += "\nIssues reaching target are potentially in your local network or with your ISP"
    else:
        hit_str += (
            "\nIssues reaching target are potentially *outside* your local network"
        )

    #########################################################
    if not name_hit:
        prt.fmt_bold_red(mystr=hit_str)
    else:
        prt.fmt_bold_yellow(mystr="Successfully connected to dns.google (8.8.8.8)")


def traceroute_main() -> None:
    """
    Main routine to launch traceroute analysis

    # https://www.inmotionhosting.com/support/website/ssh/read-a-traceroute/

    Rules
        0. do we actually hit endpoint with a time?
        1. anything over 150ms is long and should raise warning
        2. high latency in 1st 3 hops indicates difficulty leaving our network & isp
        3. TODO: Increasing latency towards the target: If you see a sudden increase in a hop and it keeps increasing to the destination (if it even gets there), then this indicates an issue starting at the hop with the increase.
        4. Timeouts at the very end of the report: Possible connection problem at the target. This will affect the connection.
    """

    ### Run traceroute
    trace_fmt = run_traceroute()
    fmted_holder, total_times_ms, header = get_traceroute_data_structs(
        trace_fmt=trace_fmt
    )

    # TODO: sort out granularity of this error by processing traceroute exit codes properly
    prt.exit_with_bye_if_none(
        check_var=fmted_holder, cust_msg="Check your network cable/connection.."
    )

    #########################################################
    ### Process traceroute
    large_latency_idx, large_latency_str = get_high_latency_hop_data(
        total_times_ms=total_times_ms, fmted_holder=fmted_holder
    )

    fmted_holder_str = gen_fmted_str_holder(fmted_holder=fmted_holder)

    trace_dict = list_of_nelem_lists_2dict(
        list_of_nelem_lists=fmted_holder_str, keyn=2, valn=-1
    )

    #########################################################
    ### Print traceroute results
    prt.print_dict_results(
        results_dict=trace_dict,
        header=header,
        fmt_func_str="fmt_bold_col1",
    )

    fmt_total_time = round(sum(total_times_ms), 3)
    prt.fmt_bold_yellow(mystr=f"\n Total time: {fmt_total_time} ms")

    #########################################################
    ## Print hops with large latency
    eval_high_hop_latency_msg(
        large_latency_str=large_latency_str, large_latency_idx=large_latency_idx
    )

    #########################################################
    ### Check to see if we are hitting destination
    final_hop = fmted_holder_str[-1][1]
    len_fmted_holder_str = len(fmted_holder_str)
    eval_final_msg(final_hop=final_hop, len_fmted_holder_str=len_fmted_holder_str)
