import urllib.parse

from dataclasses import dataclass
import json

@dataclass()
class ProxyRule:
    """
    This class is used to store proxy connection rules.
    Attributes:
        wifi_ssid: If the name of the wifi network is equal to this string, the proxy will be used.
        proxy_address: The address of the proxy.
    """
    wifi_ssid: str
    proxy_address: str
    proxy_type: str

    def __init__(self, wifi_ssid: str, proxy_address: str ="", proxy_type: str="") -> None:
        """
            This function is used to initialize the Proxy Rule.
            :param wifi_ssid: The name of the wifi network.
            :param proxy_address: The address of the proxy.
            :param proxy_type: The type of the proxy. Supported types are: http, https, socks5.
            :return: None
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
        :param json_string: The json string to convert.
        :return: None
        """
        return ProxyRule(**json.loads(json_string))

    def to_json(self) -> str:
        """
        This function is used to convert the ProxyRule to a json string.
        :return: The ProxyRule as a json string.
        """
        return json.dumps(self.__dict__)