import os
import sys
from scapy.all import *
from helpers import *
from printers import *

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


def calculate_dns_fail_perecentage(results_dict, num_domains):
    fail_list = [
        value for value in list(results_dict.values()) if len(value.split(" ")) > 1
    ]

    num_fails = len(fail_list)

    fail_percent = 0
    if num_fails != 0:
        fail_percent = (len(fail_list) / num_domains) * 100.0

    return fail_percent


check_url_dict = {
    "google.com": "216.58.204.228",
    "simulate-error-tuydutyi.com": "8.8.8.8",  # 8.8.8.8 ip address simulates working dns
    "duckduckgo.com": "52.142.124.215",
    "www.bing.com": "13.107.21.200",
    "www.bbc.co.uk": "212.58.237.252",
}


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

        ################
        public_ip_https = whatis_publicip(
            ip_check_url="https://ipinfo.io/ip", timeout=2
        )

        if public_ip_https is None:
            fmt_error_bold_red(
                mystr="Cannot retrieve your public IP address over HTTPS."
            )

            print("Now checking via dig")

            public_ip_dig = run_cmd_with_output(
                comm_str="dig @resolver4.opendns.com myip.opendns.com +short"
            )

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

        else:
            fmt_highlight_bold_yellow(
                mystr=f"Your public IP (over HTTPS) is {public_ip_https}"
            )

        # sys.exit(0)

        ### 3. Check Domain Names
        print("\nNow testing DNS servers..")
        test_domains = list(check_url_dict.keys())
        len_test_domains = len(test_domains)

        domain_results = curl_websites(url_dict=test_domains, timeout=2)

        fail_percent1 = calculate_dns_fail_perecentage(
            results_dict=domain_results, num_domains=len_test_domains
        )

        print_results_from_dict(
            results_dict=domain_results,
            header=f"Curl website domain-names had a failure rate of {fail_percent1}%",
            fmt_func_str="fmt_ok_error",
        )

        ### 3. Check IP addresses
        failed_domain_ip_dict = {
            check_url_dict[domain]: domain
            for domain, result in domain_results.items()
            if "OK - " not in result
        }

        # TODO: sort out this logic
        ip_results = curl_websites(url_dict=failed_domain_ip_dict, timeout=2)

        fail_percent2 = calculate_dns_fail_perecentage(
            results_dict=ip_results, num_domains=len_test_domains
        )

        print_results_from_dict(
            results_dict=ip_results,
            header=f"Curl website IP address had a failure rate of {fail_percent2}%",
            fmt_func_str="fmt_ok_error",
        )

    ##################
    ### Find network setup details
    # 1. find my public ip address
    #   * curl https://ipinfo.io/ip
    # 2. find local connection details
    #   * interface-name
    #   * dhcp details (if relevant)
    #   * gateway ip
    #   * nameservers
    # 3. test route to gateway
    # 4. check if dns servers are working

    ################################################################################

    ################################################################################
    ### Check Connection status

    # connx_status = active_nmcli_dict.get("GENERAL.STATE", None)
    # print("connx_status", connx_status)
    #'sys.exit(0)

    ### Check DNS servers
    dns_servers = [
        value for key, value in active_nmcli_dict.items() if "IP4.DNS" in key
    ]

    print("\nChecking DNS servers")
    # https://stackoverflow.com/questions/13842116/how-do-we-get-txt-cname-and-soa-records-from-dnspython
    # import dnspython as dns

    dns_results_dict = check_dns_servers(
        dns_servers=dns_servers, site_list=test_domains
    )

    # for key, values in dns_results_dict.items():
    #     print("\nNameServer:", key)
    dnserver_test_printer(dns_results_dict=dns_results_dict)
