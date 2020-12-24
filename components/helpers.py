"""Helper functions."""

import shlex
import subprocess
import requests
from requests.exceptions import HTTPError
import dns.resolver

check_url_dict = {
    "google.com": "216.58.204.228",
    "simulate-error-tuydutyi.com": "8.8.8.8",  # 8.8.8.8 ip address simulates working dns
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
            result = f"OK - {str(status_code)}"
        except HTTPError as err:
            print(f"HTTP error occurred: {err}")
            result = f"OK - {str(err)}"
        except requests.ConnectTimeout as err:
            result = f"Timeout - {str(err)}"
        except requests.ConnectionError as err:
            result = f"Connection Error - {str(err)}"
        except Exception as err:
            print(f"Other error occurred - {err}")

        results_dict[myurl] = result

    return results_dict


def whatis_publicip(ip_check_url="https://ipinfo.io/ip", timeout=10):
    """
    Find users public IP address from a url service.
    """

    try:
        resp = requests.get(ip_check_url, timeout=timeout)
    except Exception as err:
        print(err)
        return None

    return resp.text


def run_cmd_with_errorcode(comm_str):
    """
    Run a subprocess command and print error code on failure.
    Also returns output on success and
    False on failure so that it can be handled downstream.
    """

    split_comm = shlex.split(comm_str, " ")

    # remove all instances of empty string
    split_comm_clean = list(filter(lambda a: a != "", split_comm))

    try:
        sp_resp = subprocess.check_output(split_comm_clean)
    except subprocess.CalledProcessError as err:
        print(f"error code  {err.returncode}")
        return False

    return sp_resp


def run_cmd_with_output(comm_str):
    """
    Run a subprocess command and print error message on failure.
    Also returns output on success and
    False on failure so that it can be handled downstream.
    """

    split_comm = shlex.split(comm_str, " ")

    # remove all instances of empty string
    split_comm_clean = list(filter(lambda a: a != "", split_comm))
    try:
        sp_resp = subprocess.check_output(split_comm_clean)
        return sp_resp
    except Exception as err:
        print("\n")
        print(err)
        return False


def process_subp_output(cmd_output, delimiter="\t", exclude_list=["", " "]):
    """
    Preprocesses output from subprocess command and returns a list of lists,
    Each sublist corresponds to a row in the output.
    Delimiter can be specified to split each row.
    Elements in exclude_list are stripped from each row.
    """

    holder = []
    for line in cmd_output.decode().split("\n"):
        # print(line)
        splitty_line = line.split(delimiter)
        # print(splitty_line)
        filtered_line = [
            elem.strip() for elem in splitty_line if elem not in exclude_list
        ]
        if len(filtered_line) > 1:
            holder.append(filtered_line)
    return holder


def gen_dict_from_list_of_2nelem_lists(list_of_2nelem_lists):
    """
    Takes in a list_of_2nelem_lists such as [[key1, val1], [key2, val2], [key3, val3]]
    and returns a dictionary.
    """

    mydict = {}
    for val_subli in list_of_2nelem_lists:
        key = val_subli[0]
        value = val_subli[1]
        mydict[key] = value

    return mydict


def gen_dict_from_list_of_nelem_lists(list_of_nelem_lists, keyn=1, valn=-1):
    """
    Takes in a list_of_nelem_lists such as [[val1, val2, val3, ..., ...], [val1, val2, val3, ..., ...], [val1, val2, val3, ..., ...]]
    and returns a dictionary.
    keyn allows user to specify index to slice to `:keyn` (i.e. start --> middle)
    valn allows user to specify index to slice from `:valn` (i.e. middle --> end)
    """

    mydict = {}
    for val_subli in list_of_nelem_lists:
        key = " ".join(val_subli[:keyn])
        value = " ".join(val_subli[valn:])
        mydict[key] = value

    return mydict


def check_dns_servers(dns_servers, site_list):
    """
    Try to resolve sites by checking each dns servers individually.
    """

    dns_results_dict = {}
    for mydns in dns_servers:
        dns_results_dict[mydns] = []

        myresolver = dns.resolver.Resolver()
        myresolver.nameservers = [mydns]

        for site in site_list:
            try:
                result = myresolver.resolve(site)
                for ipval in result:
                    #'try:
                    ipaddr = ipval.to_text()
                    #'print("IP", ipaddr)
            except Exception as err:
                ipaddr = str(err)

            dns_results_dict[mydns].append([site, ipaddr])
    return dns_results_dict


# https://www.certdepot.net/rhel7-get-started-nmcli/
# https://www.thegeekdiary.com/how-to-configure-and-manage-network-connections-using-nmcli/
