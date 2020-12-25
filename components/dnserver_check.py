"""Check ability of dns servers to resolve sites."""

import dns.resolver
import dns.rdatatype
from components.helpers import (
    check_url_dict,
    curl_websites,
    list_of_2nelem_lists_2dict,
)
from components.printers import print_dict_results


def calc_dns_fail_percent(results_dict, num_domains):
    """
    Calculate the percentage failed dns lookups for one dns server.
    """

    fail_list = [
        value for value in list(results_dict.values()) if value.split(" ")[0] != "OK"
    ]

    num_fails = len(fail_list)

    fail_percent = 0.0
    if num_fails != 0:
        fail_percent = (len(fail_list) / num_domains) * 100.0

    return fail_percent


def print_with_dns_header(results_dict, header, len_test_domains):
    """Print curl result with percentage fail number in header."""

    fail_percent = calc_dns_fail_percent(
        results_dict=results_dict, num_domains=len_test_domains
    )
    print_dict_results(
        results_dict=results_dict,
        header=f"{header} {fail_percent}%",
        fmt_func_str="fmt_ok_error",
    )


def query_dns_via_udp(nameserver, mydomain):

    where = nameserver

    qry = dns.message.make_query(mydomain, dns.rdatatype.A)

    try:
        resp = dns.query.udp(
            qry, where, timeout=5, port=53, one_rr_per_rrset=True, ignore_trailing=True
        )
    except Exception as err:
        return f" Fail - {err}"

    a_record_matches = []
    for ans in resp.answer:
        for item in ans.items:
            if ans.rdtype == dns.rdatatype.A:
                a_record_matches.append(item.address)

    if len(a_record_matches) != 0:
        a_record_str = "OK - " + ", ".join(a_record_matches)
    else:
        a_record_str = " Fail - Lookup returned no results"

    return a_record_str


def check_dns_servers(dns_servers, site_list):
    """
    Try to resolve sites by checking each dns servers individually.
    """

    dns_results_dict = {}
    for mydns in dns_servers:
        dns_results_dict[mydns] = []
        for site in site_list:
            ip_arecords = query_dns_via_udp(nameserver=mydns, mydomain=site)

            dns_results_dict[mydns].append([site, ip_arecords])
    return dns_results_dict


def dns_check_main(active_nmcli_dict):
    """
    Main routine to check dns servers bt:
        1. domain name
        2. IP address
    Assumes that google dns server 8.8.8.8 is highly available
    """

    ################################################################################
    ### Check if we can curl websites over https
    test_domains = list(check_url_dict.keys())
    len_test_domains = len(test_domains)

    domain_results = curl_websites(url_dict=test_domains, timeout=2)

    print_with_dns_header(
        results_dict=domain_results,
        header=f"Curl website domain (HTTPS) fail rate =",
        len_test_domains=len_test_domains,
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
    ### Check DNS servers
    print("\nNow testing DNS servers..")
    dns_servers = [
        value for key, value in active_nmcli_dict.items() if "IP4.DNS" in key
    ]

    ### Add google dns server to list if not already present
    if "8.8.8.8" not in dns_servers:
        dns_servers.append("8.8.8.8")

    print("\nChecking DNS servers...")

    dns_results_dict = check_dns_servers(
        dns_servers=dns_servers, site_list=test_domains
    )

    for dns_name, list_of_2nelem_lists in dns_results_dict.items():
        dns_dict = list_of_2nelem_lists_2dict(list_of_2nelem_lists=list_of_2nelem_lists)

        print_with_dns_header(
            results_dict=dns_dict,
            header=f"NameServer {dns_name} UDP Lookup fail rate =",
            len_test_domains=len_test_domains,
        )
