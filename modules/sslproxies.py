import requests
from bs4 import BeautifulSoup
import random
from concurrent.futures import ThreadPoolExecutor
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RequestWrapper:
    """Wrapper for SSLProxies to allow method-based requests (GET, POST, PUT, etc.)."""
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


class SSLProxies:
    """Fetches and manages SSL proxies from sslproxies.org."""
    
    SSL_PROXIES_URL = "https://www.sslproxies.org/"
    
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    def __init__(self, max_workers=10, timeout=5):
        self.max_workers = max_workers
        self.timeout = timeout
        self.proxies = self._fetch_proxies()
        self.request = RequestWrapper(self)  # ✅ Fix: Assign wrapper instead of overriding `request`

    def _fetch_proxies(self):
        """Scrapes proxy list from sslproxies.org and returns them."""
        try:
            response = requests.get(self.SSL_PROXIES_URL, headers=self.HEADERS, timeout=10, verify=False)
            response.raise_for_status()
        except requests.RequestException:
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="table table-striped table-bordered")

        if not table:
            return []

        # Extracting proxies
        proxy_list = []
        for row in table.tbody.find_all("tr"):
            columns = row.find_all("td")
            ip = columns[0].text.strip()
            port = columns[1].text.strip()
            proxy = f"http://{ip}:{port}"
            proxy_list.append(proxy)

        return proxy_list

    def get_random_proxy(self):
        """Returns a random proxy in requests format."""
        if not self.proxies:
            return None
        proxy = random.choice(self.proxies)
        return {"http": proxy, "https": proxy}

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
            try:
                response = requests.request(method, url, proxies={"http": proxy, "https": proxy}, headers=self.HEADERS, timeout=self.timeout, verify=False, **kwargs)

                if response.status_code == 200:
                    return response  # Return successful response
                
                last_response = response  # Store last response in case all fail
            except requests.RequestException:
                pass

        return last_response  # Return last failed response if all fail

    def request_with_all_proxies(self, method, url, **kwargs):
        """Attempts to request the given URL using all proxies concurrently."""
        if not self.proxies:
            return []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(lambda proxy: self._make_request(method, url, proxy, **kwargs), self.proxies)

        return [result for result in results if result]

    def _make_request(self, method, url, proxy, **kwargs):
        """Helper method to send a request using a specific proxy."""
        try:
            response = requests.request(method, url, proxies={"http": proxy, "https": proxy}, headers=self.HEADERS, timeout=self.timeout, verify=False, **kwargs)
            
            if response.status_code == 200:
                return response  # Return successful response
        
        except requests.RequestException:
            pass
        
        return None
