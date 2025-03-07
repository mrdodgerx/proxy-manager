# Proxy Manager & SSL Proxies

This repository provides two Python classes for **proxy management**:
- `ProxyManager`: Fetches free proxies from [proxifly/free-proxy-list](https://github.com/proxifly/free-proxy-list) and supports **HTTP, HTTPS, SOCKS4, and SOCKS5** proxies.
- `SSLProxies`: Scrapes **free SSL proxies** from [sslproxies.org](https://www.sslproxies.org) for secure requests.

## 📌 Features
✅ **Supports HTTP, HTTPS, SOCKS4, and SOCKS5 proxies**  
✅ **Automatic proxy rotation** – switches proxies if one fails  
✅ **Supports all HTTP methods** – `GET`, `POST`, `PUT`, `DELETE`, etc.  
✅ **Retries failed requests** using multiple proxies  
✅ **Provides method-based requests** (`.get()`, `.post()`, `.put()`, etc.)  
✅ **Works with both free SSL and SOCKS proxies**  

---

# 🔧 Installation

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/mrdodgerx/proxy-manager.git
cd proxy-manager
```

### **2️⃣ Install Dependencies**
Use the `requirements.txt` file to install all required packages:
```bash
pip install -r requirements.txt
```

#### **📌 Dependencies in `requirements.txt`**
```
beautifulsoup4==4.13.3
bs4==0.0.2
certifi==2025.1.31
charset-normalizer==3.4.1
colorama==0.4.6
idna==3.10
PySocks==1.7.1
requests==2.32.3
soupsieve==2.6
typing_extensions==4.12.2
urllib3==2.3.0
```

---

# 🚀 Usage Guide

## **1️⃣ Using `ProxyManager` (Proxifly Free Proxy List)**
`ProxyManager` fetches **free proxies** (HTTP, HTTPS, SOCKS4, SOCKS5) from **proxifly**.

### **📌 Example: Initialize `ProxyManager`**
```python
from proxy_manager import ProxyManager

# Get an HTTP proxy from the United States
proxy_manager = ProxyManager(protocol="http", country="US")
```

### **📌 Example: Make a Request with a Proxy**
```python
response = proxy_manager.request.get("https://httpbin.org/ip")
if response:
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
```

### **📌 Example: Use SOCKS4 or SOCKS5 Proxies**
```python
# Get a SOCKS5 proxy
proxy_manager = ProxyManager(protocol="socks5")

# Make a request using SOCKS5
response = proxy_manager.request.get("https://httpbin.org/ip")
print(response.json())
```

### **📌 Example: POST Request with JSON Data**
```python
response = proxy_manager.request.post("https://httpbin.org/post", json={"user": "admin"})
print(response.json())
```

---

## **2️⃣ Using `SSLProxies` (Scraped from sslproxies.org)**
`SSLProxies` scrapes **free SSL proxies** from **sslproxies.org**.

### **📌 Example: Initialize `SSLProxies`**
```python
from ssl_proxies import SSLProxies

proxy_manager = SSLProxies()
```

### **📌 Example: Make a GET Request with an SSL Proxy**
```python
response = proxy_manager.request.get("https://httpbin.org/ip")
print(response.json())
```

### **📌 Example: Use Different HTTP Methods**
```python
response = proxy_manager.request.post("https://httpbin.org/post", data={"name": "John"})
print(response.json())

response = proxy_manager.request.put("https://httpbin.org/put", json={"key": "value"})
print(response.json())
```

---

# ⚙️ Configuration Options

### **📌 `ProxyManager` Options**
```python
ProxyManager(protocol="http", country="US")
```
| Parameter  | Description                                  | Example Values  |
|------------|----------------------------------------------|----------------|
| `protocol` | Choose proxy type (`http`, `https`, `socks4`, `socks5`, `all`) | `"http"`, `"socks5"` |
| `country`  | Filter proxies by country (optional)        | `"US"`, `"AE"` |

### **📌 `SSLProxies` Options**
```python
SSLProxies(max_workers=10, timeout=5)
```
| Parameter    | Description                                | Example Values |
|-------------|--------------------------------------------|---------------|
| `max_workers` | Number of threads for concurrent requests | `5`, `10`, `20` |
| `timeout`    | Request timeout in seconds               | `5`, `10` |

---

# 🔥 Features Comparison

| Feature                 | `ProxyManager` | `SSLProxies` |
|-------------------------|---------------|-------------|
| **Source**              | Proxifly Free Proxy List | sslproxies.org |
| **Supports SOCKS4/5**   | ✅ Yes | ❌ No |
| **Supports HTTP/HTTPS** | ✅ Yes | ✅ Yes |
| **Country Filtering**   | ✅ Yes | ❌ No |
| **Auto Proxy Rotation** | ✅ Yes | ✅ Yes |
| **Multi-threading**     | ❌ No  | ✅ Yes |

---

# ⚠️ Troubleshooting

### **1️⃣ SOCKS Proxies Not Working?**
**Solution:** Install PySocks support for `requests`:
```bash
pip install requests[socks]
```

### **2️⃣ SSL Warning (`InsecureRequestWarning`)?**
**Solution:** Suppress SSL warnings in your script:
```python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

---

# 📜 License
This project is **open-source** and free to use.

---

# ⭐ Contribution
Feel free to **submit issues** or **contribute** to improve this project! 🚀