import os
import sys
from components.helpers import run_cmd_with_errorcode
from components.printers import fmt_error_bold_red
from components.connectivity_checker import check_connectivity_main, check_publicip_main
from components.dnserver_check import dns_check_main

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
        active_nmcli_dict = check_connectivity_main()

        ################
        ## 3. Check whether public IP is assigned
        check_publicip_main()

        ################
        ## 4. Check traceroute

        ################
        ## 5. Check DNS servers
        dns_check_main(active_nmcli_dict=active_nmcli_dict)