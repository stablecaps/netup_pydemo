"""Check connectivity using route and nmcli."""

import sys
from components.helpers import (
    whatis_publicip,
    run_cmd_with_output,
    list_of_2nelem_lists_2dict,
    substr_dict_key_search,
    process_subp_output,
)
from components.printers import ColourPrinter
from typing import Dict, List, Optional

prt = ColourPrinter()


def get_iface_cmd_dict() -> Dict[str, str]:
    """
    Returns a dictionary with network interface data as a result of running `route -n`.

    # The default gateway is always shown with the destination 0.0.0.0 when the -n option is used.
    # https://unix.stackexchange.com/questions/94018/what-is-the-meaning-of-0-0-0-0-as-a-gateway
    # https://opensource.com/business/16/8/introduction-linux-network-routing
    # https://www.techrepublic.com/article/understand-the-basics-of-linux-routing/
    """

    route_cmd = run_cmd_with_output("route -n")
    prt.exit_with_bye_if_none(check_var=route_cmd, cmd_run="route -n")

    iface_info = process_subp_output(cmd_output=route_cmd, delimiter=" ")

    interface_dict = {}
    for iface_list in iface_info:
        if iface_list[0] in ["Destination", "Kernel"]:
            pass
        else:
            destination = iface_list[0]
            iface_name = iface_list[-1]
            interface_dict[destination] = iface_name

    return interface_dict


def get_default_iface(iface_dict) -> Optional[str]:

    prt.print_dict_results(
        results_dict=iface_dict,
        header="Kernel IP routing table",
        fmt_func_str="fmt_bold_col1",
    )

    default_iface = iface_dict.get("0.0.0.0", None)

    if default_iface is None:
        prt.fmt_bold_red(
            mystr=(
                "\nNo default gateway detected."
                + "\nPlease check network cable/connection."
                + "\nExiting.."
            )
        )
        sys.exit(1)
    prt.fmt_bold_yellow(mystr=f"Default iface is {default_iface}")

    return default_iface


def get_nmcli_cmd_dict() -> Dict[str, List[List[str]]]:
    """
    Returns a dictionary with network connection data as a result of running `rnmcli dev show`.
    """

    nmcli_cmd = run_cmd_with_output("nmcli dev show")
    prt.exit_with_bye_if_none(check_var=nmcli_cmd, cmd_run="nmcli dev show")

    nmcli_info = process_subp_output(cmd_output=nmcli_cmd, delimiter=": ")

    nmcli_dict = {}
    for subli in nmcli_info:

        assert len(subli) == 2, "nmcli split error. script assumes 2 values per line"

        nmkey = subli[0]
        nmval = subli[1]
        if nmkey == "GENERAL.DEVICE":
            ### Create a new key with empty list ready to be appended to
            dict_key = nmval
            nmcli_dict[dict_key] = []
        else:
            nmcli_dict[dict_key].append([nmkey, nmval])

    return nmcli_dict


def process_nmcli_dict(nmcli_all_dict, default_iface: str) -> Dict[str, str]:
    """
    Get connection info for main network interface.
    """

    active_nmcli_dict = list_of_2nelem_lists_2dict(
        list_of_2nelem_lists=nmcli_all_dict[default_iface]
    )

    default_gateway = active_nmcli_dict.get("IP4.GATEWAY", None)

    priv_ip_addresses = substr_dict_key_search(
        in_dict=active_nmcli_dict, search_term="IP4.ADDRESS"
    )

    prt.nmcli_printer(
        nmcli_all_dict=nmcli_all_dict,
        default_iface=default_iface,
        print_all_ifaces=False,
    )

    if default_gateway is None:
        prt.fmt_bold_red(
            mystr="Cannot find default gateway. Possible configuration error.\n Exiting..."
        )
        sys.exit(1)

    prt.fmt_bold_yellow(mystr=f"Default gateway is {default_gateway}")

    if len(priv_ip_addresses) > 0:
        pip_str = ""
        for priv_ip in priv_ip_addresses:
            pip_str += f"\tPRIVATE IP: {priv_ip}\n"

        prt.fmt_bold_yellow(mystr=f"Detected private Ip Addresses:\n{pip_str}")

    return active_nmcli_dict


def run_publicip_routine() -> None:
    """
    Main routine to check:
    1.  users basic connection details & gateway (router) situation
    2.  users public IP address can be retrived via an https lookup or alternatively via dig
    """

    public_ip_https = whatis_publicip(ip_check_url="https://ipinfo.io/ip", timeout=2)

    # dig @resolver4.opendns.com myip.opendns.com +short
    # dig @8.8.8.8 -t txt o-o.myaddr.l.google.com +short
    # TODO: add alts
    public_ip_dig = run_cmd_with_output(
        comm_str="dig @208.67.220.222 myip.opendns.com +short"
    )
    prt.exit_with_bye_if_none(
        check_var=public_ip_dig, cmd_run="dig @208.67.220.222 myip.opendns.com +short"
    )

    if public_ip_https is None:
        prt.fmt_bold_red(mystr="Cannot retrieve your public IP address over HTTPS.")
    else:
        prt.fmt_bold_yellow(mystr=f"Your public IP (HTTPS) is {public_ip_https}")
    ############################################################
    if not public_ip_dig:
        prt.fmt_bold_red(
            mystr=(
                "Cannot retrieve your public IP address via dig (UDP)."
                + "\n It is likely that the connection to your ISP is broken."
            )
        )
    else:
        prt.fmt_bold_yellow(
            mystr=f"Your public IP via dig (UDP) is {public_ip_dig.decode()}"
        )
    ############################################################


def check_connx_main() -> Dict[str, str]:
    """
    Subroutine to check connection details using route & nmcli.
    """

    iface_dict = get_iface_cmd_dict()

    default_iface = get_default_iface(iface_dict=iface_dict)

    nmcli_all_dict = get_nmcli_cmd_dict()

    active_nmcli_dict = process_nmcli_dict(
        nmcli_all_dict=nmcli_all_dict, default_iface=default_iface
    )

    run_publicip_routine()

    return active_nmcli_dict