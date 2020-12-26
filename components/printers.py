"""Functions to assist printing to the terminal."""

import sys
from blessings import Terminal
from components.helpers import list_of_2nelem_lists_2dict


class ColourPrinter:
    def __init__(self):
        self.term = Terminal()

        ### Dictionary that holds format functions
        self.fmt_func_dict = {
            "fmt_ok_error": self.fmt_ok_error,
            "fmt_keyok_valerror": self.fmt_keyok_valerror,
            "fmt_ok_error_dns": self.fmt_ok_error_dns,
            "fmt_bold_col1": self.fmt_bold_col1,
        }

    def fmt_bold_red(self, mystr):
        """
        Return a string formatted in bold red.
        """

        print(f"\n{self.term.red}{self.term.bold}{mystr}{self.term.normal}")

    def fmt_bold_yellow(self, mystr):
        """
        Return a string formatted in bold yellow.
        """

        print(f"\n{self.term.yellow}{self.term.bold}{mystr}{self.term.normal}")

    def get_longest_str_in_dict(self, mydict, mode="keys"):
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

    def fmt_ok_error(self, results_dict):
        """
        Return a key value pair with value formatted in red if it does not contain
        the substring "OK".
        Key is always green bold.
        """

        max_spaces = self.get_longest_str_in_dict(mydict=results_dict, mode="keys")
        for key, value in results_dict.items():
            key_just = (key + ":").ljust(max_spaces, " ")
            if "OK - " in value:
                print(
                    f"{self.term.green}{self.term.bold}{key_just} \t{self.term.normal} {value}"
                )
            else:
                print(
                    f"{self.term.bold}{self.term.green}{key_just} {self.term.normal}\t{self.term.red}{value}{self.term.normal}"
                )

    def fmt_keyok_valerror(self, results_dict):
        """
        Return a key value pair with value always formatted in red.
        Key is always green bold.
        """

        max_spaces = self.get_longest_str_in_dict(mydict=results_dict, mode="keys")
        for key, value in results_dict.items():
            key_just = (key + ":").ljust(max_spaces, " ")
            print(
                f"{self.term.bold}{self.term.green}{key_just} {self.term.normal}\t{self.term.red}{value}{self.term.normal}"
            )

    def fmt_ok_error_dns(self, results_dict):
        """
        Return a key value pair with value formatted in red if it does not contain
        the substring starts with "The DNS".
        Key is always green bold.
        """

        # TODO: see if this can be combined with fmt_ok_error()

        max_spaces = self.get_longest_str_in_dict(mydict=results_dict, mode="keys")
        for key, value in results_dict.items():
            key_just = (key + ":").ljust(max_spaces, " ")
            if value.startswith("The DNS"):
                print(
                    f"{self.term.green}{self.term.bold}{key_just} {self.term.normal}\t{self.term.red}{value}{self.term.normal}"
                )
            else:
                print(
                    f"{self.term.green}{self.term.bold}{key_just} \t{self.term.normal} {value}"
                )

    def fmt_bold_col1(self, results_dict):
        """
        Return a key value pair with value always normal font.
        Key is always green bold.
        All text is green
        """

        max_spaces = self.get_longest_str_in_dict(mydict=results_dict, mode="keys")
        for key, value in results_dict.items():
            key_just = (key + ":").ljust(max_spaces, " ")
            print(
                f"{self.term.green}{self.term.bold}{key_just} \t{self.term.normal}{value}"
            )

    def print_dict_results(self, results_dict, header, fmt_func_str):
        """
        Prints out colour coded results from dictionary with user defined header.
        `fmt_func_str` is used to lookup functions stored in `fmt_func_dict`
        """

        print(
            f"\n {self.term.bold}{self.term.underline}>> {header}: {self.term.normal}"
        )
        self.fmt_func_dict[fmt_func_str](results_dict)

    ###################################################################

    def nmcli_printer(self, nmcli_all_dict, default_iface, print_all_ifaces=False):
        """
        Prints out colour coded results from dictionary containing nmcli data.
        Option `print_all_ifaces` prints all interface data.
        By default only the default interface is printed out.
        """

        iface_name_li = [default_iface]
        if print_all_ifaces:
            iface_name_li = list(nmcli_all_dict.keys())

        for iface in iface_name_li:
            iface_dict = list_of_2nelem_lists_2dict(
                list_of_2nelem_lists=nmcli_all_dict[iface]
            )

            self.print_dict_results(
                results_dict=iface_dict,
                header=f"Iface info for: {iface}",
                fmt_func_str="fmt_bold_col1",
            )
