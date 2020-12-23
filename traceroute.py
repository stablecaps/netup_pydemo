import re
from helpers import *
from printers import *


traceroute_comm = "traceroute -q 3  8.8.8.8"

print("Running Traceroute..")
trace = run_cmd_with_output(comm_str=traceroute_comm)

if not trace:
    fmt_error_bold_red(mystr="Check your network cable/connection..")
    sys.exit(1)

trace_fmt = preprocess_subp_output(
    cmd_output=trace, delimiter=" ", exclude_list=["", " ", "*", "ms"]
)

print("\n\n")


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

        calc_list = [float(elem) for elem in sublist[3:] if not ip_addr_re.match(elem)]

        len_calc = len(calc_list)
        avg_time = round(sum(calc_list) / len_calc, 3)
        fmt_row.append(avg_time)
        fmted_holder.append(fmt_row)

        total_times_ms.append(avg_time)

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

print("total_times_ms", total_times_ms)
for row in fmted_holder:
    print(row)
    # print(" ".join(row))

large_latency_idx = []
large_latency_str = []
large_threshold = 150
for idx, hop_time in enumerate(total_times_ms):
    if hop_time > large_threshold:
        large_latency_idx.append(int(fmted_holder[idx][0]))
        large_latency_str.append(fmted_holder[idx])


print("\n\n")


fmted_holder_str = []
for row in fmted_holder:
    print(row)
    time_str = f"{str(row[-1])} ms average"
    row[-1] = time_str
    fmted_holder_str.append(row)


trace_dict = gen_dict_from_list_of_nelem_lists(
    list_of_nelem_lists=fmted_holder_str, keyn=2, valn=-1
)

header = "delme-test"
print_results_from_dict(
    results_dict=trace_dict,
    header=header,
    fmt_func_str="fmt_bold_col1",
)

fmt_highlight_bold_yellow(mystr=f"\n Total time: {sum(total_times_ms)} ms")


## Print hops with large latency
if len(large_latency_str) > 0:
    largehop_dict = gen_dict_from_list_of_nelem_lists(
        list_of_nelem_lists=large_latency_str, keyn=2, valn=-1
    )
    print()
    fmt_error_bold_red(mystr="Hops with large latencies found:")
    # for hop in large_latency_str:
    print_results_from_dict(
        results_dict=largehop_dict,
        header=f"Hops with large latency (> {large_threshold} ms)",
        fmt_func_str="fmt_keyok_valerror",
    )

    local_hop_high = False
    rising_hop_list = []
    high_asc_hop_start = None
    for idx_val in large_latency_idx:
        print("u", idx_val)
        if idx_val <= 3:
            local_hop_high = True
            break

    if local_hop_high:
        fmt_error_bold_red(
            mystr=(
                "! High latencies near traceroute start.\n"
                + "Issues are likely to be present in your local network or with your ISP"
            )
        )

### Check to see if we are hitting destination
if (len(fmted_holder_str) < 2) and (fmted_holder_str[-1][1] != "dns.google"):
    fmt_error_bold_red(
        mystr=(
            "!! Did not hit dns.google (8.8.8.8).\n"
            + "Issues reaching target are likely to be in your local network or with your ISP"
        )
    )
elif (len(fmted_holder_str) > 2) and (fmted_holder_str[-1][1] != "dns.google"):
    fmt_error_bold_red(
        mystr=(
            "!! Did not hit dns.google (8.8.8.8).\n"
            + "Issues reaching target are likely to be *outside* your local network"
        )
    )


# https://www.inmotionhosting.com/support/website/ssh/read-a-traceroute/

### Rules

# 0. do we actually hit endpoint with a time?
# 1. anything over 150ms is long and should raise warning
# 2. high latency in 1st 3 hops indicates difficulty leaving our network & isp
# 3. TODO: Increasing latency towards the target: If you see a sudden increase in a hop and it keeps increasing to the destination (if it even gets there), then this indicates an issue starting at the hop with the increase.
# 4. Timeouts at the very end of the report: Possible connection problem at the target. This will affect the connection.