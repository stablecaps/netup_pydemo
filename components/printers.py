"""Functions to assist printing to the terminal."""

import sys
from blessings import Terminal
from components.helpers import gen_dict_from_list_of_2nelem_lists


def get_longest_str_in_dict(mydict, mode="keys"):
    """
    Return an integer corresponding to the greatest number of characters
    from all the keys or values in a dictionary.
    `mode` sets whether keys or values are searched.
    """

    if mode == "keys":
        dict_list = list(mydict.keys())
    elif mode == "values":
        dict_list = list(mydict.values())
    else:
        print("incorrect mode. Exiting..")
        sys.exit(1)

    return len(max(dict_list, key=len))


def fmt_bold_red(mystr):
    """
    Return a string formatted in bold red.
    """

    term = Terminal()
    print(f"\n{term.red}{term.bold}{mystr}{term.normal}")


def fmt_bold_yellow(mystr):
    """
    Return a string formatted in bold yellow.
    """

    term = Terminal()
    print(f"\n{term.yellow}{term.bold}{mystr}{term.normal}")


def fmt_ok_error(results_dict):
    """
    Return a key value pair with value formatted in red if it does not contain
    the substring "OK".
    Key is always green bold.
    """

    term = Terminal()

    max_spaces = get_longest_str_in_dict(mydict=results_dict, mode="keys")
    for key, value in results_dict.items():
        key_just = (key + ":").ljust(max_spaces, " ")
        if "OK - " in value:
            print(f"{term.green}{term.bold}{key_just} \t{term.normal} {value}")
        else:
            print(
                f"{term.bold}{term.green}{key_just} {term.normal}\t{term.red}{value}{term.normal}"
            )


def fmt_keyok_valerror(results_dict):
    """
    Return a key value pair with value always formatted in red.
    Key is always green bold.
    """

    term = Terminal()

    max_spaces = get_longest_str_in_dict(mydict=results_dict, mode="keys")
    for key, value in results_dict.items():
        key_just = (key + ":").ljust(max_spaces, " ")
        print(
            f"{term.bold}{term.green}{key_just} {term.normal}\t{term.red}{value}{term.normal}"
        )


def fmt_ok_error_dns(results_dict):
    """
    Return a key value pair with value formatted in red if it does not contain
    the substring starts with "The DNS".
    Key is always green bold.
    """

    # TODO: see if this can be combined with fmt_ok_error()
    term = Terminal()

    max_spaces = get_longest_str_in_dict(mydict=results_dict, mode="keys")
    for key, value in results_dict.items():
        key_just = (key + ":").ljust(max_spaces, " ")
        if value.startswith("The DNS"):
            print(
                f"{term.green}{term.bold}{key_just} {term.normal}\t{term.red}{value}{term.normal}"
            )
        else:
            print(f"{term.green}{term.bold}{key_just} \t{term.normal} {value}")


def fmt_bold_col1(results_dict):
    """
    Return a key value pair with value always normal font.
    Key is always green bold.
    All text is green
    """

    term = Terminal()

    max_spaces = get_longest_str_in_dict(mydict=results_dict, mode="keys")
    for key, value in results_dict.items():
        key_just = (key + ":").ljust(max_spaces, " ")
        print(f"{term.green}{term.bold}{key_just} \t{term.normal}{value}")


### Dictionary that holds format functions
fmt_func_dict = {
    "fmt_ok_error": fmt_ok_error,
    "fmt_keyok_valerror": fmt_keyok_valerror,
    "fmt_ok_error_dns": fmt_ok_error_dns,
    "fmt_bold_col1": fmt_bold_col1,
}


def print_dict_results(results_dict, header, fmt_func_str):
    """
    Prints out colour coded results from dictionary with user defined header.
    `fmt_func_str` is used to lookup functions stored in `fmt_func_dict`
    """

    term = Terminal()

    print(f"\n {term.bold}{term.underline}>> {header}: {term.normal}")
    fmt_func_dict[fmt_func_str](results_dict)


###################################################################
def nmcli_printer(nmcli_all_dict, default_iface, print_all_ifaces=False):
    """
    Prints out colour coded results from dictionary containing nmcli data.
    Option `print_all_ifaces` prints all interface data.
    By default only the default interface is printed out.
    """

    iface_name_li = [default_iface]
    if print_all_ifaces:
        iface_name_li = list(nmcli_all_dict.keys())

    for iface in iface_name_li:
        iface_dict = gen_dict_from_list_of_2nelem_lists(
            list_of_2nelem_lists=nmcli_all_dict[iface]
        )

        print_dict_results(
            results_dict=iface_dict,
            header=f"Iface info for: {iface}",
            fmt_func_str="fmt_bold_col1",
        )


def dns_printer(dns_results_dict):
    """
    Prints out colour coded results from dictionary containing dns server data.
    """

    for dns_name, list_of_2nelem_lists in dns_results_dict.items():
        dns_dict = gen_dict_from_list_of_2nelem_lists(
            list_of_2nelem_lists=list_of_2nelem_lists
        )

        print_dict_results(
            results_dict=dns_dict,
            header=f"NameServer {dns_name} Lookup results:",
            fmt_func_str="fmt_ok_error_dns",
        )
