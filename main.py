from modules.sslproxies import SSLProxies
from modules.githubproxy import ProxyManager

if __name__ == '__main__':
    
    # scraper = SSLProxies(max_workers=10, timeout=5)

    # # Fetch proxies and request www.google.com using all of them
    # url = "https://www.google.com"
    # response = scraper.request.get(url)
    
    proxy_manager = ProxyManager(protocol="socks5")

    # Example: Make a GET request using shortcut
    response1 = proxy_manager.request.get("https://httpbin.org/ip")
    if response1:
        print("GET Status Code:", response1.status_code)
        print("GET Response JSON:sadasd", response1.text)
       

    # # Print successful responses
    # if response:
    #     print("Status Code:", response.status_code)
    #     print("Response JSON:", response.text)
