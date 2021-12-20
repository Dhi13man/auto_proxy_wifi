from os import environ

from models.proxy_rule import ProxyRule
from services.system_calls import powershell_exec_output, exec_output, exec


class ProxyHandler:
    """
    This class is used to change the device proxy settings based on proxy connection rules.

    Attributes
    ----------
    proxy_rules : list
        A list of ProxyRule objects to be used for proxy setting.
    ask_admin_permission : bool
        Whether to ask for admin permission to set use netsh.exe. Won't configure netsh if set to False.

    Methods
    -------
    get_proxy_from_rules()
        This function is used to get the proxy address for the currently connected wifi network.
    set_proxy_event_loop(verbose: bool = True)
        Begins the proxy setting infinite event loop.
    unset_proxy()
        This function is used to unset the proxy address.
    set_proxy(proxy_address: str)
        This function is used to set the proxy address.
    get_wifi_ssid()
        This function is used to get the SSID of the currently connected wifi network.
    """
    proxy_rules: list
    ask_admin_permission: bool = True

    def __init__(self, proxy_rules: list, ask_admin_permission: bool = True) -> 'ProxyHandler':
        """
        Create an instance of ProxyHandler.

        Parameters
        ----------
        proxy_rules : list
            A list of ProxyRule objects to be used for proxy setting.
        ask_admin_permission : bool
            Whether to ask for admin permission to set use netsh.exe. Won't configure netsh if set to False.

        Returns
        -------
        ProxyHandler
            An instance of ProxyHandler with the given proxy rules.
        """
        self.proxy_rules = proxy_rules
        self.ask_admin_permission = ask_admin_permission

    def get_proxy_from_rules(self) -> str:
        """
        This function is used to get the proxy address for the currently connected wifi network.

        Returns
        -------
        str
            The address of the proxy.
        """
        wifi_name: str = self.get_wifi_ssid()
        # Strict Search
        for proxy_rule in self.proxy_rules:
            search_name: str = str(proxy_rule.wifi_ssid).lower().lstrip().rstrip()
            curr_name: str = wifi_name.lower().lstrip().rstrip()
            if search_name == curr_name:
                return proxy_rule.proxy_address
        return ""

    def set_proxy_event_loop(self, verbose: bool = True) -> None:
        """
        Begins the proxy setting infinite event loop.

        Parameters
        ----------
        verbose : bool
            Whether to tell user when proxy changes.
        
        Returns
        -------
        None
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

    def unset_proxy(self) -> None:
        """
        This function is used to unset the proxy address.
        
        Returns
        -------
        None
        """
        # RegEdit
        exec(
            'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f',
        )
        # CMD Environment
        exec('setx http_proxy "%s"' % '')
        exec('setx https_proxy "%s"' % '')
        # Powershell Enviornment
        powershell_exec_output(
            '[System.Environment]::SetEnvironmentVariable("http_proxy","%s")' % '',
        )
        powershell_exec_output(
            '[System.Environment]::SetEnvironmentVariable("https_proxy","%s")' % '',
        )
        # More Environment
        environ["http_proxy"] = ""
        environ["https_proxy"] = ""
        # Netsh (requires admin)
        if self.ask_admin_permission:
            powershell_exec_output('Start-Process netsh.exe -ArgumentList "winhttp reset proxy" -Verb runas')

    def set_proxy(self, proxy_address: str) -> None:
        """
        This function is used to set the proxy address.

        Parameters
        ----------
        proxy_address : str
            The address of the proxy.
        
        Returns
        -------
        None
        """
        if proxy_address == "":
            ProxyHandler.unset_proxy()
        else:
            # RegEdit
            exec(
                'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f',
            )
            exec(
                'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d %s /f' % proxy_address,
            )
            # CMD Environment
            exec('setx http_proxy "%s"' % proxy_address)
            exec('setx https_proxy "%s"' % proxy_address)
            # Powershell Enviornment
            powershell_exec_output(
                '[System.Environment]::SetEnvironmentVariable("http_proxy","%s")' % proxy_address,
            )
            powershell_exec_output(
                '[System.Environment]::SetEnvironmentVariable("https_proxy","%s")' % proxy_address,
            )
            # More Environment
            environ["http_proxy"] = proxy_address
            environ["https_proxy"] = proxy_address
            # Netsh (requires admin)
            if self.ask_admin_permission:
                powershell_exec_output(
                    "Start-Process netsh.exe -ArgumentList 'winhttp set proxy proxy-server=\"%s\" bypass-list=\"*.local;<local>\"' -Verb runas"
                    % proxy_address,
                )

    @staticmethod
    def get_wifi_ssid() -> str:
        """
        This function is used to get the SSID of the wifi network.

        Returns
        -------
        str
            The name (SSID) of the currently connected wifi network.
        """
        out: str = exec_output(
            ['netsh', 'WLAN', 'show', 'interfaces'],
        )
        out_lines: list = out.split("\n")
        for line in out_lines:
            if "SSID" in line and "BSSID" not in line:
                return line.split(": ")[1]
        return ""
