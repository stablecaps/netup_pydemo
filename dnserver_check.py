import os
import sys
from scapy.all import *
from helpers import *
from printers import *


def calculate_dns_fail_perecentage(results_dict, num_domains):
    fail_list = [
        value for value in list(results_dict.values()) if len(value.split(" ")) > 1
    ]

    num_fails = len(fail_list)

    fail_percent = 0
    if num_fails != 0:
        fail_percent = (len(fail_list) / num_domains) * 100.0

    return fail_percent


def main():
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