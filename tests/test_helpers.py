"""Test helper functions."""

import pytest
import components.helpers as helpo

test_dict = {
    "GENERAL.TYPE": "ethernet",
    "GENERAL.HWADDR": "F8:32:E4:9B:06:7F",
    "GENERAL.MTU": "1500",
    "GENERAL.STATE": "100 (connected)",
    "GENERAL.CONNECTION": "Ethernet connection 1",
    "GENERAL.CON-PATH": "/org/freedesktop/NetworkManager/ActiveConnection/7",
    "WIRED-PROPERTIES.CARRIER": "on",
    "IP4.ADDRESS[1]": "192.168.10.2/24",
    "IP4.GATEWAY": "192.168.10.1",
    "IP4.ROUTE[1]": "dst = 0.0.0.0/0, nh = 192.168.10.1, mt = 100",
    "IP4.ROUTE[2]": "dst = 169.254.0.0/16, nh = 0.0.0.0, mt = 1000",
    "IP4.ROUTE[3]": "dst = 192.168.10.0/24, nh = 0.0.0.0, mt = 100",
    "IP4.DNS[1]": "192.168.10.1",
    "IP4.DNS[2]": "72.66.115.13",
    "IP6.ADDRESS[1]": "fe80::2cba:b04f:fa10:8eb4/64",
    "IP6.GATEWAY": "--",
    "IP6.ROUTE[1]": "dst = fe80::/64, nh = ::, mt = 100",
    "IP6.ROUTE[2]": "dst = ff00::/8, nh = ::, mt = 256, table=255",
}


@pytest.mark.parametrize(
    "in_dict,search_term,expected",
    [
        (test_dict, "GENERAL.STA", ["100 (connected)"]),
        (
            test_dict,
            "IP4.ROUTE",
            [
                "dst = 0.0.0.0/0, nh = 192.168.10.1, mt = 100",
                "dst = 169.254.0.0/16, nh = 0.0.0.0, mt = 1000",
                "dst = 192.168.10.0/24, nh = 0.0.0.0, mt = 100",
            ],
        ),
        (test_dict, "IP4.GATEWAY", ["192.168.10.1"]),
        (test_dict, "randomnonexistantkey", []),
    ],
)
def test_substr_dict_key_search(in_dict, search_term, expected):

    assert helpo.substr_dict_key_search(in_dict, search_term) == expected


@pytest.mark.parametrize(
    "list_of_2nelem_lists,expected",
    [
        ([["key1", "val1"], ["key2", "val2"]], {"key1": "val1", "key2": "val2"}),
        (
            [["key1", "middle", "val1"], ["key2", "val2"]],
            {"key1": "middle", "key2": "val2"},
        ),
    ],
)
def test_list_of_2nelem_lists_2dict(list_of_2nelem_lists, expected):

    assert helpo.list_of_2nelem_lists_2dict(list_of_2nelem_lists) == expected


@pytest.mark.parametrize(
    "list_of_xnelem_lists,keyn,valn,expected",
    [
        ([["key1", "val1"], ["key2", "val2"]], 1, -1, {"key1": "val1", "key2": "val2"}),
        (
            [["key1", "middle", "val1"], ["key2", "val2"]],
            1,
            -1,
            {"key1": "val1", "key2": "val2"},
        ),
    ],
)
def test_list_of_xnelem_lists_2dict(list_of_xnelem_lists, keyn, valn, expected):

    assert (
        helpo.list_of_xnelem_lists_2dict(list_of_xnelem_lists, keyn, valn) == expected
    )


def test_assert_list_of_xnelem_lists_2dict():

    lolists = [["key1", "val1"], ["key2", "val2"]]

    with pytest.raises(Exception):
        helpo.list_of_xnelem_lists_2dict(list_of_xnelem_lists=lolists, keyn=3, valn=-1)

    with pytest.raises(Exception):
        helpo.list_of_xnelem_lists_2dict(list_of_xnelem_lists=lolists, keyn=1, valn=-3)
