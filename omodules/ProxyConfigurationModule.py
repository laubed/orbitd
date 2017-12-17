from omodules import OModule
import subprocess

class NetworkConfigurationModule(OModule):
    def handledKeys(self):
        return ("proxy_mode",
                "proxy_address",
                "proxy_port",
                "proxy_bypass")

    def runKey(self, key, value, database):
        if  key == "proxy_mode" or \
            key == "proxy_address" or \
            key == "proxy_port" or \
            key == "proxy_bypass":

            if  database.get_device_key("proxy_mode") is None or \
                database.get_device_key("proxy_mode") == "none":
                with open("/etc/profile.d/orbit_proxy.sh", "w") as proxyfile:
                    proxyfile.write("")

                with open("/etc/chromium-browser/policies/orbit_proxy", "w") as proxyfile:
                    proxyfile.writelines(["{",
                                          "\"ProxyMode\" : \"direct\"",
                                          "}"])



            if database.get_device_key("proxy_mode") == "manual":
                with open("/etc/profile.d/orbit_proxy.sh", "w") as proxyfile:
                    proxyfile.writelines(["export http_proxy=http://" + database.get_device_key("proxy_address") + ":" + database.get_device_key("proxy_port"),
                                          "export https_proxy=$http_proxy",
                                          "export ftp_proxy=$http_proxy",
                                          "export rsync_proxy=$http_proxy",
                                          "export HTTP_PROXY=$http_proxy",
                                          "export HTTPS_PROXY=$http_proxy",
                                          "export FTP_PROXY=$http_proxy",
                                          "export RSYNC_PROXY=$http_proxy",
                                          "export no_proxy=\""+ database.get_device_key("proxy_bypass")+"\"",
                                          "export NO_PROXY=$no_proxy"])

                with open("/etc/chromium-browser/policies/orbit_proxy", "w") as proxyfile:
                    proxyfile.writelines(["{",
                                          "\"ProxyMode\" : \"fixed_servers\",",
                                          "\"ProxyServer\" : \"" + database.get_device_key("proxy_address") + ":" + database.get_device_key("proxy_port") + "\"",
                                          "}"])

                subprocess.call(["chmod", "+x", "/etc/profile.d/orbit_proxy.sh"])
