import os
import sys
import requests
from requests.exceptions import HTTPError
from blessings import Terminal

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


def curl_websites(url_dict, timeout=10):
    """
    Use requests to get http response codes or appopriate error from a list of websites.
    https://realpython.com/python-requests/
    """

    results_dict = {}
    for myurl in url_dict:
        try:
            resp = requests.get(f"https://{myurl}", timeout=timeout)
            status_code = resp.status_code
            # print("resp", resp.status_code)
            result = f"OK - {str(status_code)}"
        except HTTPError as err:
            print(f"HTTP error occurred: {err}")
            result = f"OK - {str(err)}"
        except requests.ConnectTimeout as err:
            # print(f"{myurl} timed out with {err}")
            result = f"Timeout - {str(err)}"
        except requests.ConnectionError as err:
            # print(f"{myurl} had the following connection error {err}")
            result = f"Connection Error - {str(err)}"
        except Exception as err:
            print(f"Other error occurred - {err}")

        results_dict[myurl] = result

    return results_dict


def print_results_from_dict(results_dict, header):
    """
    Prints out colour coded results from dictionary.
    """

    term = Terminal()

    print(f"\n{term.bold} {term.underline} {header}: {term.normal}")
    for key, value in results_dict.items():
        if "OK - " in value:
            print(f"{term.green}{term.bold}{key}: {term.normal} {value}")
        else:
            print(f"{term.red}{term.bold}{key}: {value}{term.normal}")


def whatis_publicip(ip_check_url="https://ipinfo.io/ip", timeout=10):

    try:
        resp = requests.get(ip_check_url, timeout=timeout)
    except Exception as err:
        return err

    return resp.text


if __name__ == "__main__":

    # ### Check Domain Names
    # test_domains = list(check_url_dict.keys())

    # domain_results = curl_websites(url_dict=test_domains, timeout=2)

    # print_results_from_dict(
    #     results_dict=domain_results, header="Curl website domain name results"
    # )

    # ### Check IP addresses
    # failed_domain_ip_dict = {
    #     check_url_dict[domain]: domain
    #     for domain, result in domain_results.items()
    #     if "OK - " not in result
    # }

    # print("failed_domain_ip_dict", failed_domain_ip_dict)

    # ip_results = curl_websites(url_dict=failed_domain_ip_dict, timeout=2)

    # print_results_from_dict(
    #     results_dict=ip_results, header="Curl website IP address results"
    # )

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

    conx_data_dict = {}
    public_ip = whatis_publicip(ip_check_url="https://ipinfo.io/ip", timeout=2)

    # print("public_ip", public_ip)
    conx_data_dict["public_ip"] = public_ip
