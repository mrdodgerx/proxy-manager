import requests
import random
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RequestWrapper:
    """Wrapper for ProxyManager to allow method-based requests (GET, POST, PUT, etc.)."""
    def __init__(self, proxy_manager):
        self.proxy_manager = proxy_manager

    def __call__(self, method, url, **kwargs):
        return self.proxy_manager._send_request(method, url, **kwargs)

    def get(self, url, **kwargs):
        return self.proxy_manager._send_request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.proxy_manager._send_request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self.proxy_manager._send_request("PUT", url, **kwargs)

    def delete(self, url, **kwargs):
        return self.proxy_manager._send_request("DELETE", url, **kwargs)

    def patch(self, url, **kwargs):
        return self.proxy_manager._send_request("PATCH", url, **kwargs)

    def head(self, url, **kwargs):
        return self.proxy_manager._send_request("HEAD", url, **kwargs)

    def options(self, url, **kwargs):
        return self.proxy_manager._send_request("OPTIONS", url, **kwargs)


class ProxyManager:
    """Fetches and manages proxies from proxifly free-proxy-list."""
    
    BASE_URL = "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies"

    PROXY_SOURCES = {
        "all": f"{BASE_URL}/all/data.json",
        "http": f"{BASE_URL}/protocols/http/data.json",
        "https": f"{BASE_URL}/protocols/https/data.json",
        "socks4": f"{BASE_URL}/protocols/socks4/data.json",
        "socks5": f"{BASE_URL}/protocols/socks5/data.json",
    }

    def __init__(self, protocol="all", country=None):
        """
        :param protocol: Proxy type ("all", "http", "https", "socks4", "socks5").
        :param country: Filter proxies by country (e.g., "US", "AE").
        """
        self.protocol = protocol
        self.country = country
        self.proxies = self._fetch_proxies()
        self.request = RequestWrapper(self)  # ✅ Fix: Assign wrapper instead of overriding `request`

    def _fetch_proxies(self):
        """Fetches proxies from the appropriate source and filters them."""
        url = self.PROXY_SOURCES.get(self.protocol, self.PROXY_SOURCES["all"])
        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()
            proxy_list = response.json()
        except requests.RequestException:
            return []

        # Filter proxies by country if specified
        if self.country:
            proxy_list = [p for p in proxy_list if p["geolocation"]["country"] == self.country]

        return proxy_list

    def get_random_proxy(self):
        """Returns a random proxy in requests format."""
        if not self.proxies:
            return None
        proxy = random.choice(self.proxies)
        if "socks4" in proxy["protocol"]:
            return {"http": f"socks4://{proxy['ip']}:{proxy['port']}", "https": f"socks4://{proxy['ip']}:{proxy['port']}"}
        elif "socks5" in proxy["protocol"]:
            return {"http": f"socks5://{proxy['ip']}:{proxy['port']}", "https": f"socks5://{proxy['ip']}:{proxy['port']}"}
        else:
            return {"http": proxy["proxy"], "https": proxy["proxy"]}

    def _send_request(self, method, url, **kwargs):
        """
        Sends a request using multiple proxies until one succeeds.

        :param method: HTTP method (GET, POST, PUT, DELETE, etc.).
        :param url: Target URL.
        :param kwargs: Additional arguments for `requests.request()`.
        :return: requests.Response object or last failed response.
        """
        if not self.proxies:
            return None

        last_response = None
        random.shuffle(self.proxies)  # Shuffle proxies to avoid predictable patterns

        for proxy in self.proxies:
            proxy_format = self.get_random_proxy()
            try:
                response = requests.request(method, url, proxies=proxy_format, timeout=10, verify=False, **kwargs)

                if response.status_code == 200:
                    return response  # Return successful response
                
                last_response = response  # Store last response in case all fail
            except requests.RequestException:
                pass

        return last_response  # Return last failed response if all fail


# Example usage
if __name__ == "__main__":
    # Example: Get a SOCKS4 proxy
    proxy_manager = ProxyManager(protocol="socks4")

    # Example: Make a GET request using SOCKS4 proxy
    response = proxy_manager.request.get("https://httpbin.org/ip")
    if response:
        print("GET Status Code:", response.status_code)
        try:
            print("GET Response JSON:", response.json())
        except requests.exceptions.JSONDecodeError:
            print("GET Response Text:", response.text[:200])

    # Example: Get a SOCKS5 proxy
    proxy_manager = ProxyManager(protocol="socks5")

    # Example: Make a GET request using SOCKS5 proxy
    response = proxy_manager.request.get("https://httpbin.org/ip")
    if response:
        print("SOCKS5 GET Status Code:", response.status_code)
        try:
            print("SOCKS5 GET Response JSON:", response.json())
        except requests.exceptions.JSONDecodeError:
            print("SOCKS5 GET Response Text:", response.text[:200])

    # Example: Make a POST request using shortcut
    response = proxy_manager.request.post("https://httpbin.org/post", data={"name": "test"})
    if response:
        print("POST Status Code:", response.status_code)
        try:
            print("POST Response JSON:", response.json())
        except requests.exceptions.JSONDecodeError:
            print("POST Response Text:", response.text[:200])

    # Example: Make a DELETE request using shortcut
    response = proxy_manager.request.delete("https://httpbin.org/delete")
    if response:
        print("DELETE Status Code:", response.status_code)
