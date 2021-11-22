from models.proxy_rule import ProxyRule
from services.proxy_handler import ProxyHandler

if __name__ == "__main__":
    # Proxy Rules for different networks
    proxy_rules: list = [
        ProxyRule("TP-Link", "http://172.16.199.40:8080", "http"),
    ]
    
    # Initialize data
    proxy_handler: ProxyHandler = ProxyHandler(proxy_rules)
    proxy_handler.set_proxy_event_loop()
