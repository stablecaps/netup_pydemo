"""Check ability of dns servers to resolve sites."""

from components.helpers import check_url_dict, curl_websites, check_dns_servers
from components.printers import print_dict_results, dns_printer


def calc_dns_fail_percent(results_dict, num_domains):
    """
    Calculate the percentage failed dns lookups for one dns server.
    """

    fail_list = [
        value for value in list(results_dict.values()) if len(value.split(" ")) > 1
    ]

    num_fails = len(fail_list)

    fail_percent = 0
    if num_fails != 0:
        fail_percent = (len(fail_list) / num_domains) * 100.0

    return fail_percent


def dns_check_main(active_nmcli_dict):
    """
    Main routine to check dns servers bt:
        1. domain name
        2. IP address
    """

    ### 3. Check Domain Names
    print("\nNow testing DNS servers..")

    test_domains = list(check_url_dict.keys())
    len_test_domains = len(test_domains)

    domain_results = curl_websites(url_dict=test_domains, timeout=2)

    fail_percent1 = calc_dns_fail_percent(
        results_dict=domain_results, num_domains=len_test_domains
    )

    print_dict_results(
        results_dict=domain_results,
        header=f"Curl website domain-names had a failure rate of {fail_percent1}%",
        fmt_func_str="fmt_ok_error",
    )

    ### 3. Check IP addresses
    ip_dict = {
        check_url_dict[domain]: domain for domain, result in domain_results.items()
    }

    ip_results = curl_websites(url_dict=ip_dict, timeout=2)

    fail_percent2 = calc_dns_fail_percent(
        results_dict=ip_results, num_domains=len_test_domains
    )

    print_dict_results(
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
    dns_printer(dns_results_dict=dns_results_dict)
