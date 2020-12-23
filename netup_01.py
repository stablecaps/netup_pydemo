import os
import sys
from scapy.all import *
from helpers import *
from printers import *
from connectivity_checker import check_connectivity_main, check_publicip_main

# Strategy:
# Start with higher level requests, then move towards more granular tests
# 1. try to service a simple web request using curl & FQDN
# 1b. try fallback urls
# 2. On failure try using known ip address
# 3. On failure assess base network connectivity
#   *  ifconfig?
#   *  check how far we can go out - traceroute
#   *  check local network saturation - (store snapshots from previous trials)
#   *
# 4. check broadband provider status
# 5. check dns servers in


if __name__ == "__main__":

    # TODO: cli-options
    # print_all_ifaces - nmcli_printer()
    #

    #################################################################
    ### 1. Simple ping-like connectivity test for a connection
    tcp_ping_commm = "nc -vz -w 5 www.google.com 8080"
    tcp_ping = run_cmd_with_errorcode(comm_str=tcp_ping_commm)

    if not tcp_ping:
        fmt_error_bold_red(mystr="TCP Ping failed. Now checking connection settings..")
        #################################################################
        ### 2. Check basic connectivity to internet
        check_connectivity_main()

        ################
        ## 3. Check whether public IP is assigned
        check_publicip_main()

        ################
        ## 4. Check traceroute
