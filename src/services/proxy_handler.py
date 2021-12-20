from os import environ

from models.proxy_rule import ProxyRule
from services.system_calls import powershell_exec_output, exec_output, exec


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
        This function is used to get the proxy address for the currently connected wifi network.
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
                    print(("Proxy to be set: %s" % proxy)
                          if proxy != "" else "No Proxy!")
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
        exec(
            "reg add \"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\" /v ProxyEnable /t REG_DWORD /d 0 /f",
        )
        # CMD Environment
        exec("set http_proxy=%s" % "")
        exec("set https_proxy=%s" % "")
        # Powershell Enviornment
        powershell_exec_output(
            "[System.Environment]::SetEnvironmentVariable(\"http_proxy\",\"%s\")" % "",
        )
        powershell_exec_output(
            "[System.Environment]::SetEnvironmentVariable(\"https_proxy\",\"%s\")" % "",
        )
        # More Environment
        environ["http_proxy"] = ""
        environ["https_proxy"] = ""
        # Netsh (requires admin)
        powershell_exec_output("Start-Process netsh.exe -ArgumentList 'winhttp reset proxy' -Verb runas")

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
            exec(
                "reg add \"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\" /v ProxyEnable /t REG_DWORD /d 1 /f",
            )
            exec(
                "reg add \"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\" /v ProxyServer /t REG_SZ /d %s /f" % proxy_address,
            )
            # CMD Environment
            exec("set http_proxy=%s" % proxy_address)
            exec("set https_proxy=%s" % proxy_address)
            # Powershell Enviornment
            powershell_exec_output(
                "[System.Environment]::SetEnvironmentVariable(\"http_proxy\",\"%s\")" % proxy_address,
            )
            powershell_exec_output(
                "[System.Environment]::SetEnvironmentVariable(\"https_proxy\",\"%s\")" % proxy_address,
            )
            # More Environment
            environ["http_proxy"] = proxy_address
            environ["https_proxy"] = proxy_address
            # Netsh (requires admin)
            powershell_exec_output(
                "Start-Process netsh.exe -ArgumentList 'winhttp set proxy proxy-server=%s bypass-list=\"*.local;<local>\"' -Verb runas"
                % proxy_address,
            )

    @staticmethod
    def get_wifi_ssid() -> str:
        """
        This function is used to get the SSID of the wifi network.
        :return: The name of the wifi network.
        """
        out: str = exec_output(
            ['netsh', 'WLAN', 'show', 'interfaces'],
        )
        out_lines: list = out.split("\n")
        for line in out_lines:
            if "SSID" in line and "BSSID" not in line:
                return line.split(": ")[1]
        return ""
