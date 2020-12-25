"""Traceroute module."""

import sys
import re
from components.helpers import (
    run_cmd_with_output,
    process_subp_output,
    list_of_nelem_lists_2dict,
)
from components.printers import (
    fmt_bold_yellow,
    fmt_bold_red,
    print_dict_results,
)

LARGE_THRESHOLD = 150


def run_and_process_traceroute():
    """
    Macro function that:
        1. runs traceroute
        2. Returns traceroute header (header)
        3. Returns a list of list containing traceroute output data with averaged times (fmted_holder)
        4. Retrns a flat list with traceroute with averaged timings in ms
    """

    traceroute_comm = "traceroute -q 3  8.8.8.8"

    print("Running Traceroute..")
    trace = run_cmd_with_output(comm_str=traceroute_comm)

    if not trace:
        fmt_bold_red(mystr="Check your network cable/connection..")
        sys.exit(1)

    trace_fmt = process_subp_output(
        cmd_output=trace, delimiter=" ", exclude_list=["", " ", "*", "ms"]
    )

    ip_addr_re = re.compile(r"^\(?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\)?$")

    fmted_holder = []
    total_times_ms = []
    for sublist in trace_fmt:

        if sublist[0] == "traceroute":
            header = " ".join(sublist)
        else:
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


def find_high_latency_hops(total_times_ms, fmted_holder):
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


def gen_fmted_str_holder(fmted_holder):
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


def eval_high_hop_latency_msg(large_latency_str, large_latency_idx):
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


def eval_final_msg(final_hop, len_fmted_holder_str):
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
        # name_hit = False
    else:
        hit_str = "Failed to hit dns.google name or 8.8.8.8 IP."
        name_hit = False

    ###
    if len_fmted_holder_str < 2:
        hit_str += "\nIssues reaching target are potentially in your local network or with your ISP"
    else:
        hit_str += (
            "\nIssues reaching target are potentially *outside* your local network"
        )

    ###
    if not name_hit:
        fmt_bold_red(mystr=hit_str)
    else:
        fmt_bold_yellow(mystr="Successfully connected to dns.google (8.8.8.8)")


def traceroute_main():
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
    fmted_holder, total_times_ms, header = run_and_process_traceroute()

    large_latency_idx, large_latency_str = find_high_latency_hops(
        total_times_ms=total_times_ms, fmted_holder=fmted_holder
    )

    fmted_holder_str = gen_fmted_str_holder(fmted_holder=fmted_holder)

    trace_dict = list_of_nelem_lists_2dict(
        list_of_nelem_lists=fmted_holder_str, keyn=2, valn=-1
    )

    #########################################################
    ### Print traceroute results
    print_dict_results(
        results_dict=trace_dict,
        header=header,
        fmt_func_str="fmt_bold_col1",
    )

    fmt_total_time = round(sum(total_times_ms), 3)
    fmt_bold_yellow(mystr=f"\n Total time: {fmt_total_time} ms")

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


# normal
# total_times_ms = [3.027, 20.703, 24.596, 22.152, 27.031, 27.322, 23.536]
# fmted_holder = [
#     ["1", "_gateway", "(192.168.10.1)", 3.027],
#     ["3", "hari-core-2a-xe-305-0.network.virginmedia.net", "(62.252.114.145)", 20.703],
#     ["5", "tele-ic-7-ae2-0.network.virginmedia.net", "(62.253.175.34)", 24.596],
#     ["6", "74-14-250-212.static.virginm.net", "(212.250.14.74)", 22.152],
#     ["7", "74.125.242.97", "(74.125.242.97)", 27.031],
#     ["8", "64.233.175.107", "(64.233.175.107)", 27.322],
#     ["9", "dns.google", "(8.8.8.8)", 23.536],
# ]

# high initial
# total_times_ms = [3.027, 152.703, 24.596, 22.152, 27.031, 27.322, 23.536]
# fmted_holder = [
#     ["1", "_gateway", "(192.168.10.1)", 3.027],
#     ["3", "hari-core-2a-xe-305-0.network.virginmedia.net", "(62.252.114.145)", 152.703],
#     ["5", "tele-ic-7-ae2-0.network.virginmedia.net", "(62.253.175.34)", 24.596],
#     ["6", "74-14-250-212.static.virginm.net", "(212.250.14.74)", 22.152],
#     ["7", "74.125.242.97", "(74.125.242.97)", 27.031],
#     ["8", "64.233.175.107", "(64.233.175.107)", 27.322],
#     ["9", "dns.google", "(8.8.8.8)", 23.536],
# ]

# high ascending
# total_times_ms = [3.027, 152.703, 24.596, 901, 800, 948, 999]
# fmted_holder = [
#     ["1", "_gateway", "(192.168.10.1)", 3.027],
#     ["3", "hari-core-2a-xe-305-0.network.virginmedia.net", "(62.252.114.145)", 152.703],
#     ["5", "tele-ic-7-ae2-0.network.virginmedia.net", "(62.253.175.34)", 24.596],
#     ["6", "74-14-250-212.static.virginm.net", "(212.250.14.74)", 901],
#     ["7", "74.125.242.97", "(74.125.242.97)", 800],
#     ["8", "64.233.175.107", "(64.233.175.107)", 948],
#     ["9", "dns.google", "(8.8.8.8)", 999],
# ]
