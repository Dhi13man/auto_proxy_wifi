import os, subprocess

from models.proxy_rule import ProxyRule

class ProxyHandler:
    """
    This class is used to change the device proxy settings based on proxy connection rules.
    """
    proxy_rules: list

    def __init__(self, proxy_rules: list) -> None:
        """
        Create an instance of ProxyHandler.
        """
        self.proxy_rules = proxy_rules

    def get_proxy_from_rules(self) -> str:
        """
        This function is used to get the proxy address for a given wifi network.
        :return: The address of the proxy.
        """
        wifi_name: str = self.get_wifi_ssid()
        for proxy_rule in self.proxy_rules:
            search_name = proxy_rule.wifi_ssid.lower()
            curr_name = wifi_name.lower()
            if search_name in curr_name: 
                return proxy_rule.proxy_address
        return ""

    def set_proxy_event_loop(self, verbose: bool = True) -> None:
        """
        Begins the proxy setting infinite event loop.
        :param verbose: Whether to tell user when proxy changes
        :return: None
        """
        old_ssid: str = ProxyHandler.get_wifi_ssid()
        while True:
            ssid: str = ProxyHandler.get_wifi_ssid()
            if ssid != "" and ssid != old_ssid:
                proxy: str = self.get_proxy_from_rules()
                # Tell user what's about to happen.
                if verbose:
                    print("For Wi-Fi SSID: " + ssid)
                    print(("Proxy to be set: %s" % proxy) if proxy != "" else "No Proxy!")
                # Set proxy
                self.set_proxy(proxy)
                old_ssid = ssid

    @staticmethod
    def unset_proxy() -> None:
        """
        This function is used to unset the proxy address.
        :return: None
        """
        # RegEdit
        os.system("reg add \"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\" /v ProxyEnable /t REG_DWORD /d 0 /f")
        # CMD Environment
        os.system("set http_proxy=%s" % "")
        os.system("set https_proxy=%s" % "")
        # Powershell Enviornment
        ProxyHandler.__powershell_run("[System.Environment]::SetEnvironmentVariable(\"http_proxy\",\"%s\")" % "")
        ProxyHandler.__powershell_run("[System.Environment]::SetEnvironmentVariable(\"https_proxy\",\"%s\")" % "")
        # More Environment
        os.environ["http_proxy"] = ""
        os.environ["https_proxy"] = ""
        # Netsh
        # os.system("netsh winhttp reset proxy")

    @staticmethod
    def set_proxy(proxy_address: str) -> None:
        """
        This function is used to set the proxy address.
        :param proxy_address: The address of the proxy.
        :return: None
        """
        if proxy_address == "":
            ProxyHandler.unset_proxy()
        else:
            # RegEdit
            os.system("reg add \"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\" /v ProxyEnable /t REG_DWORD /d 1 /f")
            os.system("reg add \"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\" /v ProxyServer /t REG_SZ /d %s /f" % proxy_address)
            # CMD Environment
            os.system("set http_proxy=%s" % proxy_address)
            os.system("set https_proxy=%s" % proxy_address)
            # Powershell Enviornment
            ProxyHandler.__powershell_run("[System.Environment]::SetEnvironmentVariable(\"http_proxy\",\"%s\")" % proxy_address)
            ProxyHandler.__powershell_run("[System.Environment]::SetEnvironmentVariable(\"https_proxy\",\"%s\")" % proxy_address)
            # More Environment
            os.environ["http_proxy"] = proxy_address
            os.environ["https_proxy"] = proxy_address
            # Netsh
            # os.system("netsh winhttp set proxy proxy-server=%s bypass-list=\"*.local;<local>\"" % proxy_address)

    @staticmethod
    def get_wifi_ssid() -> str:
        """
        This function is used to get the SSID of the wifi network.
        :return: The name of the wifi network.
        """
        out: str = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces']).decode("UTF-8")
        out_lines: list = out.split("\n")
        for line in out_lines:
            if "SSID" in line and "BSSID" not in line:
                return line.split(": ")[1]
        return ""

    @staticmethod
    def __powershell_run(cmd: str) -> str:
        """
        Utility function to run a command in powershell mode.
        """
        completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
        return completed.stdout.decode("UTF-8")

