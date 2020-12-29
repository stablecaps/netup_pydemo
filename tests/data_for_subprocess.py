comm_output1 = b"GENERAL.DEVICE:                         enp3s0\nGENERAL.TYPE:                           ethernet\nGENERAL.HWADDR:                         F8:32:E4:9B:06:7F\nGENERAL.MTU:                            1500\nGENERAL.STATE:                          100 (connected)\nGENERAL.CONNECTION:                     Ethernet connection 1\nGENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveConnection/7\nWIRED-PROPERTIES.CARRIER:               on\nIP4.ADDRESS[1]:                         192.168.10.2/24\nIP4.GATEWAY:                            192.168.10.1\nIP4.ROUTE[1]:                           dst = 0.0.0.0/0, nh = 192.168.10.1, mt = 100\nIP4.ROUTE[2]:                           dst = 169.254.0.0/16, nh = 0.0.0.0, mt = 1000\nIP4.ROUTE[3]:                           dst = 192.168.10.0/24, nh = 0.0.0.0, mt = 100\nIP4.DNS[1]:                             192.168.10.1\nIP4.DNS[2]:                             72.66.115.13\nIP6.ADDRESS[1]:                         fe80::2cba:b04f:fa10:8eb4/64\nIP6.GATEWAY:                            --\nIP6.ROUTE[1]:                           dst = fe80::/64, nh = ::, mt = 100\nIP6.ROUTE[2]:                           dst = ff00::/8, nh = ::, mt = 256, table=255\n\nGENERAL.DEVICE:                         br-00e838e83286\nGENERAL.TYPE:                           bridge\nGENERAL.HWADDR:                         02:42:72:72:09:84\nGENERAL.MTU:                            1500\nGENERAL.STATE:                          100 (connected)\nGENERAL.CONNECTION:                     br-00e838e83286\nGENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveConnection/2\nIP4.ADDRESS[1]:                         172.18.0.1/16\nIP4.GATEWAY:                            --\nIP4.ROUTE[1]:                           dst = 172.18.0.0/16, nh = 0.0.0.0, mt = 0\nIP6.ADDRESS[1]:                         fe80::42:72ff:fe72:984/64\nIP6.GATEWAY:                            --\nIP6.ROUTE[1]:                           dst = fe80::/64, nh = ::, mt = 256\nIP6.ROUTE[2]:                           dst = ff00::/8, nh = ::, mt = 256, table=255\n\nGENERAL.DEVICE:                         docker0\nGENERAL.TYPE:                           bridge\nGENERAL.HWADDR:                         02:42:E8:84:21:E0\nGENERAL.MTU:                            1500\nGENERAL.STATE:                          100 (connected)\nGENERAL.CONNECTION:                     docker0\nGENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveConnection/3\nIP4.ADDRESS[1]:                         172.17.0.1/16\nIP4.GATEWAY:                            --\nIP4.ROUTE[1]:                           dst = 172.17.0.0/16, nh = 0.0.0.0, mt = 0\nIP6.GATEWAY:                            --\n\nGENERAL.DEVICE:                         veth3d71858\nGENERAL.TYPE:                           ethernet\nGENERAL.HWADDR:                         E6:70:A3:C2:86:68\nGENERAL.MTU:                            1500\nGENERAL.STATE:                          10 (unmanaged)\nGENERAL.CONNECTION:                     --\nGENERAL.CON-PATH:                       --\nWIRED-PROPERTIES.CARRIER:               on\n\nGENERAL.DEVICE:                         vethb9c3a73\nGENERAL.TYPE:                           ethernet\nGENERAL.HWADDR:                         86:23:EE:AF:5E:43\nGENERAL.MTU:                            1500\nGENERAL.STATE:                          10 (unmanaged)\nGENERAL.CONNECTION:                     --\nGENERAL.CON-PATH:                       --\nWIRED-PROPERTIES.CARRIER:               on\n\nGENERAL.DEVICE:                         vethba2e347\nGENERAL.TYPE:                           ethernet\nGENERAL.HWADDR:                         82:E1:50:39:74:89\nGENERAL.MTU:                            1500\nGENERAL.STATE:                          10 (unmanaged)\nGENERAL.CONNECTION:                     --\nGENERAL.CON-PATH:                       --\nWIRED-PROPERTIES.CARRIER:               on\n\nGENERAL.DEVICE:                         lo\nGENERAL.TYPE:                           loopback\nGENERAL.HWADDR:                         00:00:00:00:00:00\nGENERAL.MTU:                            65536\nGENERAL.STATE:                          10 (unmanaged)\nGENERAL.CONNECTION:                     --\nGENERAL.CON-PATH:                       --\nIP4.ADDRESS[1]:                         127.0.0.1/8\nIP4.GATEWAY:                            --\nIP6.ADDRESS[1]:                         ::1/128\nIP6.GATEWAY:                            --\nIP6.ROUTE[1]:                           dst = ::1/128, nh = ::, mt = 256\n"
comm_expected1 = [
    ["GENERAL.DEVICE", "enp3s0"],
    ["GENERAL.TYPE", "ethernet"],
    ["GENERAL.HWADDR", "F8:32:E4:9B:06:7F"],
    ["GENERAL.MTU", "1500"],
    ["GENERAL.STATE", "100 (connected)"],
    ["GENERAL.CONNECTION", "Ethernet connection 1"],
    ["GENERAL.CON-PATH", "/org/freedesktop/NetworkManager/ActiveConnection/7"],
    ["WIRED-PROPERTIES.CARRIER", "on"],
    ["IP4.ADDRESS[1]", "192.168.10.2/24"],
    ["IP4.GATEWAY", "192.168.10.1"],
    ["IP4.ROUTE[1]", "dst = 0.0.0.0/0, nh = 192.168.10.1, mt = 100"],
    ["IP4.ROUTE[2]", "dst = 169.254.0.0/16, nh = 0.0.0.0, mt = 1000"],
    ["IP4.ROUTE[3]", "dst = 192.168.10.0/24, nh = 0.0.0.0, mt = 100"],
    ["IP4.DNS[1]", "192.168.10.1"],
    ["IP4.DNS[2]", "72.66.115.13"],
    ["IP6.ADDRESS[1]", "fe80::2cba:b04f:fa10:8eb4/64"],
    ["IP6.GATEWAY", "--"],
    ["IP6.ROUTE[1]", "dst = fe80::/64, nh = ::, mt = 100"],
    ["IP6.ROUTE[2]", "dst = ff00::/8, nh = ::, mt = 256, table=255"],
    ["GENERAL.DEVICE", "br-00e838e83286"],
    ["GENERAL.TYPE", "bridge"],
    ["GENERAL.HWADDR", "02:42:72:72:09:84"],
    ["GENERAL.MTU", "1500"],
    ["GENERAL.STATE", "100 (connected)"],
    ["GENERAL.CONNECTION", "br-00e838e83286"],
    ["GENERAL.CON-PATH", "/org/freedesktop/NetworkManager/ActiveConnection/2"],
    ["IP4.ADDRESS[1]", "172.18.0.1/16"],
    ["IP4.GATEWAY", "--"],
    ["IP4.ROUTE[1]", "dst = 172.18.0.0/16, nh = 0.0.0.0, mt = 0"],
    ["IP6.ADDRESS[1]", "fe80::42:72ff:fe72:984/64"],
    ["IP6.GATEWAY", "--"],
    ["IP6.ROUTE[1]", "dst = fe80::/64, nh = ::, mt = 256"],
    ["IP6.ROUTE[2]", "dst = ff00::/8, nh = ::, mt = 256, table=255"],
    ["GENERAL.DEVICE", "docker0"],
    ["GENERAL.TYPE", "bridge"],
    ["GENERAL.HWADDR", "02:42:E8:84:21:E0"],
    ["GENERAL.MTU", "1500"],
    ["GENERAL.STATE", "100 (connected)"],
    ["GENERAL.CONNECTION", "docker0"],
    ["GENERAL.CON-PATH", "/org/freedesktop/NetworkManager/ActiveConnection/3"],
    ["IP4.ADDRESS[1]", "172.17.0.1/16"],
    ["IP4.GATEWAY", "--"],
    ["IP4.ROUTE[1]", "dst = 172.17.0.0/16, nh = 0.0.0.0, mt = 0"],
    ["IP6.GATEWAY", "--"],
    ["GENERAL.DEVICE", "veth3d71858"],
    ["GENERAL.TYPE", "ethernet"],
    ["GENERAL.HWADDR", "E6:70:A3:C2:86:68"],
    ["GENERAL.MTU", "1500"],
    ["GENERAL.STATE", "10 (unmanaged)"],
    ["GENERAL.CONNECTION", "--"],
    ["GENERAL.CON-PATH", "--"],
    ["WIRED-PROPERTIES.CARRIER", "on"],
    ["GENERAL.DEVICE", "vethb9c3a73"],
    ["GENERAL.TYPE", "ethernet"],
    ["GENERAL.HWADDR", "86:23:EE:AF:5E:43"],
    ["GENERAL.MTU", "1500"],
    ["GENERAL.STATE", "10 (unmanaged)"],
    ["GENERAL.CONNECTION", "--"],
    ["GENERAL.CON-PATH", "--"],
    ["WIRED-PROPERTIES.CARRIER", "on"],
    ["GENERAL.DEVICE", "vethba2e347"],
    ["GENERAL.TYPE", "ethernet"],
    ["GENERAL.HWADDR", "82:E1:50:39:74:89"],
    ["GENERAL.MTU", "1500"],
    ["GENERAL.STATE", "10 (unmanaged)"],
    ["GENERAL.CONNECTION", "--"],
    ["GENERAL.CON-PATH", "--"],
    ["WIRED-PROPERTIES.CARRIER", "on"],
    ["GENERAL.DEVICE", "lo"],
    ["GENERAL.TYPE", "loopback"],
    ["GENERAL.HWADDR", "00:00:00:00:00:00"],
    ["GENERAL.MTU", "65536"],
    ["GENERAL.STATE", "10 (unmanaged)"],
    ["GENERAL.CONNECTION", "--"],
    ["GENERAL.CON-PATH", "--"],
    ["IP4.ADDRESS[1]", "127.0.0.1/8"],
    ["IP4.GATEWAY", "--"],
    ["IP6.ADDRESS[1]", "::1/128"],
    ["IP6.GATEWAY", "--"],
    ["IP6.ROUTE[1]", "dst = ::1/128, nh = ::, mt = 256"],
]