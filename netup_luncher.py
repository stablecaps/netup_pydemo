"""
Main entrpoint to run code taht checks and evaluates reasons for loss in internet connectivity.
"""

import sys
import argparse
from typing import Optional
from components.helpers import run_cmd_with_errorcode, check_url_dict
from components.printers import ColourPrinter
from components.connectivity_checker import check_connx_main, run_publicip_routine

from components.dnserver_check import DNSServers

from components.traceroute import traceroute_main


class NetupLauncher:
    """
    Parse command line options and select netup launch mode.
    """

    def __init__(self) -> None:

        self.prt = ColourPrinter()

        help_banner = "Available command options: <all|connx|publicip|dns|traceroute>"

        parser = argparse.ArgumentParser(
            description="AWS MP Framework launcher",
            usage="python netup_luncher.py <command> <options>",
        )

        parser.add_argument("command", help=help_banner)

        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(NetupLauncher, args.command):
            print("Unrecognized command")
            parser.print_help()
            sys.exit(1)

        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    @staticmethod
    def _str2bool(putative_cli_bool: str) -> Optional[bool]:
        if isinstance(putative_cli_bool, bool):
            return putative_cli_bool

        if putative_cli_bool.lower() in ("yes", "true", "t", "y", "1"):
            return True
        elif putative_cli_bool.lower() in ("no", "false", "f", "n", "0"):
            return False
        else:
            print("putative_cli_bool arg not processed")

        raise argparse.ArgumentTypeError(
            f"Cannot parse {putative_cli_bool} into boolean."
        )

    @staticmethod
    def connx() -> None:
        """Launch subroutine to check connection details using route & nmcli"""

        print("\nLaunching route & nmcli subroutine...\n")
        check_connx_main()
        print("\nExiting.")

    @staticmethod
    def publicip() -> None:
        """Launch subroutine to check publicip"""

        print("\nLaunching publicip subroutine...\n")
        run_publicip_routine()

        print("\nExiting.")

    @staticmethod
    def dns() -> None:
        """Launch subroutine to check DNS Servers"""

        print("\nLaunching DNS Server check subroutine...\n")
        active_nmcli_dict = check_connx_main()

        dns_test = DNSServers(
            active_nmcli_dict=active_nmcli_dict, check_url_dict=check_url_dict
        )
        dns_test.dns_check_main()

        print("\nExiting.")

    @staticmethod
    def traceroute() -> None:
        """Launch subroutine to perform traceroute"""

        print("\nLaunching traceroute check subroutine...\n")
        traceroute_main()

        print("\nExiting.")

    def all(self) -> None:
        """Launch all routines to detect internet connectivity issues"""

        parser = argparse.ArgumentParser(description="Run all diagnostics")
        parser.add_argument(
            "-f",
            "--force",
            default=False,
            type=bool,
            help="Switch to force error and run all tests.",
        )

        args = parser.parse_args(sys.argv[2:])

        NetupLauncher._str2bool(putative_cli_bool=args.force)

        print("\nLaunching all routines\n")

        #################################################################
        ### 1. Simple ping-like connectivity test for a connection
        # TODO: this can be set to use port 8080 to delibrately fail for testing purposes

        tcp_ping_commm = "nc -vz -w 5 www.google.com 80"
        tcp_ping = run_cmd_with_errorcode(comm_str=tcp_ping_commm)

        ### Switch to force error
        if args.force:
            tcp_ping = False

        if not tcp_ping:
            self.prt.fmt_bold_red(
                mystr="TCP Ping failed. Now checking connection settings.."
            )
            #################################################################
            ### 2. Check basic connectivity to internet
            active_nmcli_dict = check_connx_main()

            ################
            ## 3. Check traceroute
            traceroute_main()

            ################
            ## 4. Check DNS servers
            dns_test = DNSServers(
                active_nmcli_dict=active_nmcli_dict, check_url_dict=check_url_dict
            )
            dns_test.dns_check_main()

            print("\nExiting.")


if __name__ == "__main__":

    NetupLauncher()
