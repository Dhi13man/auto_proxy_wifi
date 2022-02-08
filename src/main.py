from models.proxy_rule import ProxyRule
from services.proxy_handler import ProxyHandler

if __name__ == "__main__":
    # Proxy Rules for different networks
    proxy_rules: list = [
        ProxyRule("TP-LINK_POCKET_3020_8D8E88", "http://172.16.199.40:8080", "http"),
    ]

    # Initialize data
    proxy_handler: ProxyHandler = ProxyHandler(proxy_rules, ask_admin_permission=True)
    proxy: str = proxy_handler.get_proxy_from_rules()

    # Tell user what's about to happen.
    print("For Wi-Fi SSID: " + ProxyHandler.get_wifi_ssid())
    print(("Proxy to be set: %s" % proxy) if proxy != "" else "No Proxy!")

    # Set proxy
    proxy_handler.set_proxy(proxy)
