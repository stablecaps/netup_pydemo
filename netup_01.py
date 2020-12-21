import os
import sys
import requests
from requests.exceptions import HTTPError
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

check_url_dict = {
    "google.com": "216.58.204.228",
    "simulate-error-tuydutyi.com": "8.8.8.8",
    "duckduckgo.com": "52.142.124.215",
    "www.bing.com": "13.107.21.200",
    "www.bbc.co.uk": "212.58.237.252",
}


if __name__ == "__main__":

    ### Check Domain Names
    test_domains = list(check_url_dict.keys())

    domain_results = curl_websites(url_dict=test_domains, timeout=2)

    print_results_from_dict(
        results_dict=domain_results,
        header="Curl website domain name results",
        fmt_func_str="fmt_ok_error",
    )

    # ### Check IP addresses
    failed_domain_ip_dict = {
        check_url_dict[domain]: domain
        for domain, result in domain_results.items()
        if "OK - " not in result
    }

    # print("failed_domain_ip_dict", failed_domain_ip_dict)

    # TODO: sort out this logic
    ip_results = curl_websites(url_dict=failed_domain_ip_dict, timeout=2)

    print_results_from_dict(
        results_dict=ip_results,
        header="Curl website IP address results",
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
    conx_data_dict = {}
    public_ip = whatis_publicip(ip_check_url="https://ipinfo.io/ip", timeout=2)

    # print("public_ip", public_ip)
    conx_data_dict["public_ip"] = public_ip

    ###
    iface_dict = get_iface_info()

    # print("\nKernel IP routing table")
    # print("\nDestination\tIface")
    # for destination, iface in iface_dict.items():
    #     print(f"{destination}\t{iface}")

    print_results_from_dict(
        results_dict=iface_dict,
        header="Kernel IP routing table",
        fmt_func_str="fmt_bold_col1",
    )
    sys.exit(0)

    default_iface = iface_dict.get("default", None)

    # TODO: sort out default iface logic/assumptions
    # TODO: use `nmcli general status`
    # print(f"\ndefault_iface {default_iface} on {iface_dict['default']}")

    ###
    nmcli_all_dict = get_nmcli_info()

    nmcli_printer(
        nmcli_all_dict=nmcli_all_dict,
        default_iface=default_iface,
        print_all_ifaces=False,
    )

    active_nmcli_dict = gen_nmcli_dict(
        nmcli_all_dict=nmcli_all_dict, iface_name=default_iface
    )

    ################################################################################
    ### Check Connection status

    connx_status = active_nmcli_dict.get("GENERAL.STATE", None)
    print("connx_status", connx_status)
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

    for key, values in dns_results_dict.items():
        print("\nNameServer:", key)
        print_dict_with_list_of_lists(list_of_lists=values)
