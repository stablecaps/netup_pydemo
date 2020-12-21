import os
import shlex
import subprocess
import requests
from requests.exceptions import HTTPError
import dns.resolver


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


def whatis_publicip(ip_check_url="https://ipinfo.io/ip", timeout=10):

    try:
        resp = requests.get(ip_check_url, timeout=timeout)
    except Exception as err:
        return err

    return resp.text


def run_cmd_with_output(comm_str):

    split_comm = shlex.split(comm_str, " ")

    # remove all instances of empty string
    split_comm_clean = list(filter(lambda a: a != "", split_comm))
    sp_resp = subprocess.check_output(split_comm_clean)

    return sp_resp


def preprocess_subp_output(cmd_output, delimiter="\t", exclude_list=["", " "]):

    holder = []
    for line in cmd_output.decode().split("\n"):
        #'print(line)
        splitty_line = line.split(delimiter)
        #'print(splitty_line)
        filtered_line = [
            elem.strip() for elem in splitty_line if elem not in exclude_list
        ]
        if len(filtered_line) > 1:
            holder.append(filtered_line)
    return holder


def get_iface_info():
    route_cmd = run_cmd_with_output("route")
    iface_info = preprocess_subp_output(cmd_output=route_cmd, delimiter=" ")

    interface_dict = {}
    for iface_list in iface_info:
        if iface_list[0] in ["Destination", "Kernel"]:
            pass
        else:
            destination = iface_list[0]
            iface_name = iface_list[-1]
            interface_dict[destination] = iface_name

    return interface_dict


def get_nmcli_info():
    route_cmd = run_cmd_with_output("nmcli dev show")
    nmcli_info = preprocess_subp_output(cmd_output=route_cmd, delimiter=": ")

    nmcli_dict = {}
    for subli in nmcli_info:
        # print(subli)

        assert len(subli) == 2, "nmcli split error. script assumes 2 values per line"

        nmkey = subli[0]
        nmval = subli[1]
        if nmkey == "GENERAL.DEVICE":
            dict_key = nmval
            nmcli_dict[dict_key] = []
        else:
            nmcli_dict[dict_key].append([nmkey, nmval])

    return nmcli_dict


def gen_nmcli_dict(nmcli_all_dict, iface_name):

    lu_dict = {}
    for val_subli in nmcli_all_dict[iface_name]:
        key = val_subli[0]
        value = val_subli[1]
        lu_dict[key] = value

    return lu_dict


def check_dns_servers(dns_servers, site_list):

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