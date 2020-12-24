"""Main entrpoint to run code taht checks and evaluates reasons for loss in internet connectivity."""

import sys
import argparse
from components.helpers import run_cmd_with_errorcode
from components.printers import fmt_error_bold_red
from components.connectivity_checker import check_connectivity_main, check_publicip_main
from components.dnserver_check import dns_check_main
from components.traceroute import traceroute_main

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


class NetupLauncher:
    """
    Parse command line options and select netup launch mode.
    """

    def __init__(self):
        help_banner = "Available command options: <all|connx|publicip|dns|traceroute>"

        parser = argparse.ArgumentParser(
            description="AWS MP Framework launcher",
            usage="python netup_luncher.py <command> <options>",
        )

        parser.add_argument("command", help=help_banner)

        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:4])
        if not hasattr(NetupLauncher, args.command):
            print("Unrecognized command")
            parser.print_help()
            sys.exit(1)

        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    @staticmethod
    def connx():
        """Launch subroutine to check connection details using route & nmcli"""

        print("\nLaunching route & nmcli subroutine...\n")
        check_connectivity_main()
        print("\nExiting.")

    @staticmethod
    def publicip():
        """Launch subroutine to check publicip"""

        print("\nLaunching publicip subroutine...\n")
        check_publicip_main()

        print("\nExiting.")

    @staticmethod
    def dns():
        """Launch subroutine to check DNS Servers"""

        print("\nLaunching DNS Server check subroutine...\n")
        active_nmcli_dict = check_connectivity_main()
        dns_check_main(active_nmcli_dict=active_nmcli_dict)

        print("\nExiting.")

    @staticmethod
    def traceroute():
        """Launch subroutine to perform traceroute"""

        print("\nLaunching traceroute check subroutine...\n")
        traceroute_main()

        print("\nExiting.")

    @staticmethod
    def all():
        """Launch all routines to detect internet connectivity issues"""

        print("\nLaunch all routines\n")
        #################################################################
        ### 1. Simple ping-like connectivity test for a connection
        # TODO: this can be set to use port 8080 to delibrately fail for testing purposes
        tcp_ping_commm = "nc -vz -w 5 www.google.com 8080"
        tcp_ping = run_cmd_with_errorcode(comm_str=tcp_ping_commm)

        if not tcp_ping:
            fmt_error_bold_red(
                mystr="TCP Ping failed. Now checking connection settings.."
            )
            #################################################################
            ### 2. Check basic connectivity to internet
            active_nmcli_dict = check_connectivity_main()

            ################
            ## 3. Check whether public IP is assigned
            check_publicip_main()

            ################
            ## 4. Check traceroute
            traceroute_main()

            ################
            ## 5. Check DNS servers
            dns_check_main(active_nmcli_dict=active_nmcli_dict)

            print("\nExiting.")


if __name__ == "__main__":

    NetupLauncher()
