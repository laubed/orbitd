from omodules import OModule

import subprocess

class NetworkConfigurationModule(OModule):
    def handledKeys(self):
        return ( "network_hostname",
                 "network_ipv4",
                 "network_gateway",
                 "network_netmask",
                 "network_dns1",
                 "network_dns2" )

    def runKey(self, key, value, orbit):
        if key == "network_hostname":
            with open("/etc/hostname", "w") as hostfile:
                hostfile.write(value)

        if  key == "network_ipv4" or \
            key == "network_gateway" or \
            key == "network_netmask" or \
            key == "network_dns1" or \
            key == "network_dns2":

            with open("/etc/network/interfaces", "w") as interfacefile:
                interfacefile.writelines(["auto lo",
                                          "iface lo inet loopback",
                                          "",
                                          "auto eth0",
                                          "iface eth0 inet static",
                                          "address " + orbit.get_device_key("network_ipv4"),
                                          "gateway " + orbit.get_device_key("network_gateway"),
                                          "netmask " + orbit.get_device_key("network_netmask"),
                                          "dns-nameservers " + orbit.get_device_key("network_dns1") + " " + orbit.get_device_key("network_dns2")])


            subprocess.call(["ifdown", "eth0", "&&", "ifup", "eth0"])