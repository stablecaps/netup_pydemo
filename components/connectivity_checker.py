"""Check connectivity using route and nmcli."""

import sys
from components.helpers import (
    get_iface_info,
    get_nmcli_info,
    whatis_publicip,
    run_cmd_with_output,
    gen_dict_from_list_of_2nelem_lists,
)
from components.printers import (
    print_results_from_dict,
    fmt_highlight_bold_yellow,
    fmt_error_bold_red,
    nmcli_printer,
)


def check_connectivity_main():
    """
    Checks connection details using route & nmcli.
    """

    iface_dict = get_iface_info()

    print_results_from_dict(
        results_dict=iface_dict,
        header="Kernel IP routing table",
        fmt_func_str="fmt_bold_col1",
    )

    default_iface = iface_dict.get("0.0.0.0", None)

    if default_iface is None:
        fmt_error_bold_red(
            mystr=(
                "\nNo default gateway detected."
                + "\nPlease check network cable/connection."
                + "\nExiting.."
            )
        )
        sys.exit(1)

    fmt_highlight_bold_yellow(mystr=f"Default iface is {default_iface}")

    ###
    nmcli_all_dict = get_nmcli_info()

    nmcli_printer(
        nmcli_all_dict=nmcli_all_dict,
        default_iface=default_iface,
        print_all_ifaces=False,
    )

    active_nmcli_dict = gen_dict_from_list_of_2nelem_lists(
        list_of_2nelem_lists=nmcli_all_dict[default_iface]
    )

    default_gateway = active_nmcli_dict.get("IP4.GATEWAY", None)

    if default_gateway is None:
        fmt_error_bold_red(
            mystr="Cannot find default gateway. Possible configuration error.\n Exiting..."
        )
        sys.exit(1)

    fmt_highlight_bold_yellow(mystr=f"Default gateway is {default_gateway}")


def check_publicip_main():
    """
    Main routine to check:
    1.  users basic connection details & gateway (router) situation
    2.  users public IP address can be retrived via an https lookup or alternatively via dig
    """

    public_ip_https = whatis_publicip(ip_check_url="https://ipinfo.io/ip", timeout=2)

    if public_ip_https is None:
        fmt_error_bold_red(mystr="Cannot retrieve your public IP address over HTTPS.")

        print("Now checking via dig")

        # dig @resolver4.opendns.com myip.opendns.com +short
        public_ip_dig = run_cmd_with_output(
            comm_str="dig @208.67.220.222 myip.opendns.com +short"
        )

        ############################################################
        if not public_ip_dig:
            fmt_error_bold_red(
                mystr=(
                    "Cannot retrieve your public IP address via dig."
                    + "\n It is likely that the connection to your ISP is broken."
                )
            )
        else:
            fmt_highlight_bold_yellow(
                mystr=f"Your public IP (via dig) is {public_ip_dig}"
                + "\nTherefore TCP connectivity is limited"
            )
            # TODO: Decide whether to exit here
        ############################################################
    else:
        fmt_highlight_bold_yellow(
            mystr=f"Your public IP (over HTTPS) is {public_ip_https}"
        )


if __name__ == "__main__":
    check_publicip_main()
