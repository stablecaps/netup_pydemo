from blessings import Terminal
from helpers import gen_dict_from_list_of_2nlists


def fmt_error_bold_red(mystr):
    term = Terminal()
    print(f"{term.red}{term.bold}{mystr}{term.normal}")


def fmt_ok_error(results_dict):
    term = Terminal()
    for key, value in results_dict.items():
        if "OK - " in value:
            print(f"{term.green}{term.bold}{key}:\t{term.normal} {value}")
        else:
            print(f"{term.bold}{term.green}{key}:{term.normal}\t{term.red}{value}")


def fmt_ok_error_dns(results_dict):
    term = Terminal()
    for key, value in results_dict.items():
        if value.startswith("The DNS"):
            print(
                f"{term.green}{term.bold}{key}:{term.normal}\t{term.red}{value}{term.normal}"
            )
        else:
            print(f"{term.green}{term.bold}{key}:\t{term.normal} {value}")


def fmt_bold_col1(results_dict):
    term = Terminal()
    for key, value in results_dict.items():
        print(f"{term.green}{term.bold}{key}:\t{term.normal}{value}")


### Dictionary that holds format functions
fmt_func_dict = {
    "fmt_ok_error": fmt_ok_error,
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
        iface_dict = gen_dict_from_list_of_2nlists(
            list_of_2nlists=nmcli_all_dict[iface]
        )

        print_results_from_dict(
            results_dict=iface_dict,
            header=f"Iface info for: {iface}",
            fmt_func_str="fmt_bold_col1",
        )


def dnserver_test_printer(dns_results_dict):

    for dns_name, list_of_2nlists in dns_results_dict.items():
        dns_dict = gen_dict_from_list_of_2nlists(list_of_2nlists=list_of_2nlists)

        print_results_from_dict(
            results_dict=dns_dict,
            header=f"NameServer {dns_name} Lookup results:",
            fmt_func_str="fmt_ok_error_dns",
        )