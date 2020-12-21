from blessings import Terminal


def fmt_ok_error(results_dict):
    term = Terminal()
    for key, value in results_dict.items():
        if "OK - " in value:
            print(f"{term.green}{term.bold}{key}:\t{term.normal} {value}")
        else:
            print(f"{term.red}{term.bold}{key}:\t{value}{term.normal}")


def fmt_bold_col1(results_dict):
    term = Terminal()
    for key, value in results_dict.items():
        print(f"{term.green}{term.bold}{key}:\t{term.normal}{value}")


### Dictionary that holds format functions
fmt_func_dict = {"fmt_ok_error": fmt_ok_error, "fmt_bold_col1": fmt_bold_col1}


def print_results_from_dict(results_dict, header, fmt_func_str):
    """
    Prints out colour coded results from dictionary.
    """

    term = Terminal()

    print(f"\n {term.bold}{term.underline}>> {header}: {term.normal}")
    fmt_func_dict[fmt_func_str](results_dict)


###################################################################
def print_dict_with_list_of_lists(list_of_lists):
    for values in list_of_lists:
        fmt_kv_pair = ": ".join(values)
        print(fmt_kv_pair)


def nmcli_printer(nmcli_all_dict, default_iface, print_all_ifaces=False):

    iface_li = [default_iface]
    if print_all_ifaces:
        iface_li = list(nmcli_all_dict.keys())

    for iface in iface_li:
        print(f"\ninfo for: {iface}")
        # TODO: use print_dict_with_list_of_lists()
        for val_subli in nmcli_all_dict[iface]:
            fmt_kv_pair = ": ".join(val_subli)
            print(fmt_kv_pair)
