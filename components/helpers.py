"""Helper functions."""

import shlex
import subprocess
import requests
from requests.exceptions import HTTPError, Timeout
from typing import Dict, List, Optional

check_url_dict = {
    "www.google.com": "216.58.204.228",
    "simulate-error-tuydutyi.com": "8.8.8.8",  # 8.8.8.8 ip address simulates working dns
    "www.duckduckgo.com": "52.142.124.215",
    "www.bing.com": "13.107.21.200",
    "www.bbc.co.uk": "212.58.237.252",
}


def get_https_request_status(myurl: str, timeout: int = 10) -> str:
    """
    Perform simple get request to a website over HTTPS.
    """

    try:
        resp = requests.get(f"https://{myurl}", timeout=timeout)
        status_code = resp.status_code
        result = f"OK - {str(status_code)}"
    except HTTPError as err:
        result = f"OK - {str(err)}"
    except requests.ConnectTimeout as err:
        result = f"Timeout - {str(err)}"
    except requests.ConnectionError as err:
        result = f"Connection Error - {str(err)}"
    except Exception as err:
        result = f"Other error occurred - str({err})"

    return result


def curl_websites(url_dict: List[str], timeout: int = 10) -> Dict[str, str]:
    """
    Use requests to get http response codes or appopriate error from a list of websites.
    https://realpython.com/python-requests/
    """

    results_dict = {}
    for myurl in url_dict:
        result = get_https_request_status(
            myurl=get_https_request_status(myurl), timeout=timeout
        )
        results_dict[myurl] = result

    return results_dict


def whatis_publicip(
    ip_check_url: str = "https://ipinfo.io/ip", timeout: int = 10
) -> str:
    """
    Find users public IP address from a url service.
    """

    try:
        resp = requests.get(ip_check_url, timeout=timeout)
    except Timeout as err:
        print(err)
        return None
    except Exception as err:
        print(err)
        return None

    return resp.text


def shlex_convert_str_2list(comm_str: str) -> List[str]:
    """
    Convert a linux command into list format with shlex.
    """

    split_comm = shlex.split(comm_str, " ")

    # remove all instances of empty string
    split_comm_clean = list(filter(lambda a: a != "", split_comm))

    return split_comm_clean


def run_cmd_with_output(comm_str: str) -> Optional[bytes]:
    """
    Run a subprocess command and print error message on failure.
    Also returns output on success and
    False on failure so that it can be handled downstream.
    """

    split_comm_clean = shlex_convert_str_2list(comm_str=comm_str)

    try:
        sp_resp = subprocess.check_output(split_comm_clean)
        return sp_resp
    except Exception as err:
        print(f"\n{err}")
        return None


def run_cmd_with_errorcode(comm_str: str) -> bool:
    """
    Run a subprocess command and print error code on failure.
    Also returns output on success and
    False on failure so that it can be handled downstream.
    """

    split_comm_clean = shlex_convert_str_2list(comm_str=comm_str)

    try:
        subprocess.check_output(split_comm_clean)
    except Exception as err:
        print(f"error code  {err}")
        return False

    return True


def process_subp_output(
    cmd_output: bytes, delimiter: str = "\t", exclude_list: List[str] = ["", " "]
) -> List[List[str]]:
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
        if len(filtered_line) > 0:
            holder.append(filtered_line)
    return holder


def substr_dict_key_search(in_dict: Dict[str, str], search_term: str) -> List[str]:
    """
    Returns a list of values from a dictionary depending on what keys are matched
    by the substring specified by search_term.
    """

    match_list = [value for key, value in in_dict.items() if search_term in key]
    return match_list


def list_of_2nelem_lists_2dict(list_of_2nelem_lists: List[List[str]]) -> Dict[str, str]:
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


def list_of_nelem_lists_2dict(
    list_of_nelem_lists: List[List[str]], keyn: int = 1, valn: int = -1
) -> Dict[str, str]:
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


# https://www.certdepot.net/rhel7-get-started-nmcli/
# https://www.thegeekdiary.com/how-to-configure-and-manage-network-connections-using-nmcli/
