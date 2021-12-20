import urllib.parse

from dataclasses import dataclass
import json

@dataclass()
class ProxyRule:
    """
    This class is used to store proxy connection rules.

    Attributes:
    -----------
        wifi_ssid : str
            If the name of the wifi network is equal to this string, the proxy will be used.
        proxy_address : str
            The address of the proxy.
        proxy_type : str
            The type of the proxy. Supported types are: http, https, socks5.
    """
    wifi_ssid: str
    proxy_address: str
    proxy_type: str

    def __init__(self, wifi_ssid: str, proxy_address: str ="", proxy_type: str="") -> 'ProxyRule':
        """
            This function is used to initialize the Proxy Rule.

            Parameters
            ----------
            wifi_ssid : str
                The name of the wifi network where this proxy rule applies.
            proxy_address : str
                The address of the proxy.
            proxy_type : str
                The type of the proxy. Supported types are: http, https, socks5.

            Returns
            -------
            ProxyRule
                The ProxyRule object.

        """
        if proxy_type == "":
            if proxy_address == "":
                proxy_type = "none"
            else:
                components: list = proxy_address.split(":")
                proxy_type = components[0] if len(components) > 1 else ""
        if proxy_type not in ["none", "http", "https", "socks5"]:
            raise ValueError("Proxy type not supported.")
        self.proxy_type = proxy_type
        self.wifi_ssid = wifi_ssid
        self.proxy_address = urllib.parse.urlparse(proxy_address).geturl()

    @staticmethod
    def from_json(json_string: str) -> 'ProxyRule':
        """
        This function is used to convert a json string to a ProxyRule.

        Parameters
        ----------
        json_string : str
            The json string to be converted.

        Returns
        -------
        ProxyRule
            The ProxyRule object deserialized from the json string.
        """
        return ProxyRule(**json.loads(json_string))

    def to_json(self) -> str:
        """
        This function is used to convert the ProxyRule to a json string.

        Returns
        -------
        str
            The json string representation of the ProxyRule.
        """
        return json.dumps(self.__dict__)