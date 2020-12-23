import sys
from blessings import Terminal
from helpers import gen_dict_from_list_of_2nelem_lists


def find_longest_string_from_dict(mydict, mode="keys"):
    if mode == "keys":
        dict_list = list(mydict.keys())
    elif mode == "values":
        dict_list = list(mydict.values())
    else:
        print("incorrect mode. Exiting..")
        sys.exit(1)

    return len(max(dict_list, key=len))


def fmt_error_bold_red(mystr):
    term = Terminal()
    print(f"\n{term.red}{term.bold}{mystr}{term.normal}")


def fmt_highlight_bold_yellow(mystr):
    term = Terminal()
    print(f"\n{term.yellow}{term.bold}{mystr}{term.normal}")


def fmt_ok_error(results_dict):
    term = Terminal()

    max_spaces = find_longest_string_from_dict(mydict=results_dict, mode="keys")
    for key, value in results_dict.items():
        key_just = (key + ":").ljust(max_spaces, " ")
        if "OK - " in value:
            print(f"{term.green}{term.bold}{key_just} \t{term.normal} {value}")
        else:
            print(
                f"{term.bold}{term.green}{key_just} {term.normal}\t{term.red}{value}{term.normal}"
            )


def fmt_keyok_valerror(results_dict):
    term = Terminal()

    max_spaces = find_longest_string_from_dict(mydict=results_dict, mode="keys")
    for key, value in results_dict.items():
        key_just = (key + ":").ljust(max_spaces, " ")
        print(
            f"{term.bold}{term.green}{key_just} {term.normal}\t{term.red}{value}{term.normal}"
        )


def fmt_ok_error_dns(results_dict):
    term = Terminal()

    max_spaces = find_longest_string_from_dict(mydict=results_dict, mode="keys")
    for key, value in results_dict.items():
        key_just = (key + ":").ljust(max_spaces, " ")
        if value.startswith("The DNS"):
            print(
                f"{term.green}{term.bold}{key_just} {term.normal}\t{term.red}{value}{term.normal}"
            )
        else:
            print(f"{term.green}{term.bold}{key_just} \t{term.normal} {value}")


def fmt_bold_col1(results_dict):
    term = Terminal()

    max_spaces = find_longest_string_from_dict(mydict=results_dict, mode="keys")
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


def print_results_from_dict(results_dict, header, fmt_func_str):
    """
    Prints out colour coded results from dictionary.
    """

    term = Terminal()

    print(f"\n {term.bold}{term.underline}>> {header}: {term.normal}")
    fmt_func_dict[fmt_func_str](results_dict)


###################################################################
def nmcli_printer(nmcli_all_dict, default_iface, print_all_ifaces=False):

    iface_name_li = [default_iface]
    if print_all_ifaces:
        iface_name_li = list(nmcli_all_dict.keys())

    for iface in iface_name_li:
        iface_dict = gen_dict_from_list_of_2nelem_lists(
            list_of_2nelem_lists=nmcli_all_dict[iface]
        )

        print_results_from_dict(
            results_dict=iface_dict,
            header=f"Iface info for: {iface}",
            fmt_func_str="fmt_bold_col1",
        )


def dnserver_test_printer(dns_results_dict):

    for dns_name, list_of_2nelem_lists in dns_results_dict.items():
        dns_dict = gen_dict_from_list_of_2nelem_lists(
            list_of_2nelem_lists=list_of_2nelem_lists
        )

        print_results_from_dict(
            results_dict=dns_dict,
            header=f"NameServer {dns_name} Lookup results:",
            fmt_func_str="fmt_ok_error_dns",
        )