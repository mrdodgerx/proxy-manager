from modules.sslproxies import SSLProxies
from modules.githubproxy import ProxyManager

if __name__ == '__main__':
    
    # Create instances of ProxyManager
    proxy_manager = ProxyManager(protocol="socks5")

    # Example: Make a GET request using shortcut
    response1 = proxy_manager.request.get("https://httpbin.org/ip")
    if response1:
        print("GET Status Code:", response1.status_code)
        print("GET Response JSON:", response1.json())
       
    ssl_proxies = SSLProxies()
    response = ssl_proxies.request.get("https://httpbin.org/ip")

    # Print successful responses
    if response:
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())
