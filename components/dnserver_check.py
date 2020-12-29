"""Check ability of dns servers to resolve sites."""

import dns.resolver
import dns.rdatatype
from components.helpers import (
    curl_websites,
    list_of_2nelem_lists_2dict,
    substr_dict_key_search,
)
from components.printers import ColourPrinter
from typing import Dict, List, Tuple


class DNSServers:
    """Class to check Domain names via HTTPS and Nameserver queries."""

    def __init__(
        self, active_nmcli_dict: Dict[str, str], check_url_dict: Dict[str, str]
    ) -> None:
        self.active_nmcli_dict = active_nmcli_dict
        self.check_url_dict = check_url_dict
        self.test_domains = list(self.check_url_dict.keys())
        self.num_domains = len(self.test_domains)

        self.prt = ColourPrinter()

    def calc_dns_fail_percent(self, results_dict: Dict[str, str]) -> float:
        """
        Calculate the percentage failed dns lookups for one dns server.
        """

        fail_list = [
            value
            for value in list(results_dict.values())
            if value.split(" ")[0] != "OK"
        ]

        num_fails = len(fail_list)

        fail_percent = 0.0
        if num_fails != 0:
            fail_percent = (len(fail_list) / self.num_domains) * 100.0

        return fail_percent

    def find_name_servers(self) -> Tuple[List[str], bool]:
        """
        Creates a list of dns servers used by the system.
        Reference google DNS nameserver (8.8.8.8) is added to compare against
        already configured nameservers.
        """

        dns_servers = substr_dict_key_search(
            in_dict=self.active_nmcli_dict, search_term="IP4.DNS"
        )

        added_google_ns = False
        ### Add google dns server to list if not already present
        if "8.8.8.8" not in dns_servers:
            added_google_ns = True
            dns_servers.append("8.8.8.8")

        return (dns_servers, added_google_ns)

    @staticmethod
    def query_dns_via_udp(nameserver: str, mydomain: str) -> str:
        """
        Returns a string of ip addresses returned by querying the specified
        nameserver of UDP (port 53).
        """

        where = nameserver

        qry = dns.message.make_query(mydomain, dns.rdatatype.A)

        try:
            resp = dns.query.udp(
                qry,
                where,
                timeout=5,
                port=53,
                one_rr_per_rrset=True,
                ignore_trailing=True,
            )
        except Exception as err:
            return f" Fail - {err}"

        a_record_matches = []
        for ans in resp.answer:
            for item in ans.items:
                if ans.rdtype == dns.rdatatype.A:
                    a_record_matches.append(item.address)

        if len(a_record_matches) != 0:
            a_record_str = "OK - " + ", ".join(a_record_matches)
        else:
            a_record_str = " Fail - Lookup returned no results"

        return a_record_str

    def check_dns_servers(self, dns_servers: List[str]) -> Dict[str, List[List[str]]]:
        """
        Try to resolve sites by checking each dns servers individually.
        """

        dns_results_dict = {}
        for mydns in dns_servers:
            dns_results_dict[mydns] = []
            for site in self.test_domains:
                ip_arecords = DNSServers.query_dns_via_udp(
                    nameserver=mydns, mydomain=site
                )

                dns_results_dict[mydns].append([site, ip_arecords])
        return dns_results_dict

    def dns_check_main(self) -> None:
        """
        Main routine to check dns servers bt:
            1. domain name
            2. IP address
        Assumes that google dns server 8.8.8.8 is highly available
        """

        #########################################################
        ### Check if we can curl websites over https
        domain_results = curl_websites(url_dict=self.test_domains, timeout=10)

        fail_perc = self.calc_dns_fail_percent(results_dict=domain_results)
        self.prt.print_dict_results(
            results_dict=domain_results,
            header=f"Curl website domain (HTTPS) fail rate = {fail_perc}%",
            fmt_func_str="fmt_ok_error",
        )

        if fail_perc == 100:
            self.prt.fmt_bold_red(mystr="Error: cannot curl any websites over HTTPS")
        elif 50 < fail_perc < 100:
            self.prt.fmt_bold_yellow(
                mystr="Warning: Cannot curl the majority of test sites over HTTPS."
            )
        else:
            self.prt.fmt_bold_yellow(
                mystr="Warning: A few test sites could not be curled over HTTPS."
            )

        #########################################################
        ### Check DNS servers
        print("\nNow testing DNS servers..")

        dns_servers, added_google_ns = self.find_name_servers()

        dns_results_dict = self.check_dns_servers(dns_servers=dns_servers)

        dns_fail_perc_dict = {}
        for nameserver, list_of_2nelem_lists in dns_results_dict.items():
            dns_dict = list_of_2nelem_lists_2dict(
                list_of_2nelem_lists=list_of_2nelem_lists
            )

            fail_perc2 = self.calc_dns_fail_percent(results_dict=dns_dict)
            self.prt.print_dict_results(
                results_dict=dns_dict,
                header=f"NameServer {nameserver} UDP Lookup fail rate = {fail_perc2}%",
                fmt_func_str="fmt_ok_error",
            )

            dns_fail_perc_dict[nameserver] = fail_perc2

        all_perc_fails = {
            True if perc > 80 else False for perc in list(dns_fail_perc_dict.values())
        }

        #########################################################
        ### Print DNS messages
        google_ns_perc = dns_fail_perc_dict.pop("8.8.8.8")
        for nameserver, fail_perc3 in dns_fail_perc_dict.items():
            msg = None
            if fail_perc3 > 41:

                msg = (
                    f"Nameserver {nameserver} is having trouble resolving "
                    + f"{fail_perc3}% of test domains.."
                )

                if added_google_ns and google_ns_perc < 40:
                    msg += (
                        f"\nHowever, Google's nameserver (8.8.8.8) failed {google_ns_perc}% "
                        + "\nConsider adding google nameservers 8.8.8.8 & 8.8.4.4 "
                        + "to your internet connection settings."
                    )

            if msg is not None:
                self.prt.fmt_bold_red(mystr=msg)

        if len(all_perc_fails) == 1 and all_perc_fails:
            self.prt.fmt_bold_red(
                mystr=(
                    "All configured DNS servers are experiencing trouble "
                    + "resolving addresses over UDP"
                )
            )
