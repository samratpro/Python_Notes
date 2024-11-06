

## 1. GET Request with User-Agent, Headers, and Proxy
```py
import urllib3
proxy_url = 'http://proxy.example.com:8080'
http = urllib3.ProxyManager(proxy_url)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json'
}
response = http.request('GET', 'http://www.example.com', headers=headers)
print(response.data.decode('utf-8'))
```
## 2. POST Request with Payload
```py
import urllib3
http = urllib3.PoolManager()
payload = {
    'field1': 'value1',
    'field2': 'value2'
}
response = http.request('POST', 'http://httpbin.org/post', fields=payload)
print(response.data.decode('utf-8'))
```

## 3. POST Request for Authentication
```py
import urllib3
http = urllib3.PoolManager()
auth_payload = {
    'username': 'myusername',
    'password': 'mypassword'
}
response = http.request('POST', 'http://httpbin.org/post', fields=auth_payload)
print(response.data.decode('utf-8'))
```

## 4. Session-based Request with Authentication
```py
from http.cookiejar import CookieJar
from urllib3 import PoolManager
cookie_jar = CookieJar()
http = PoolManager(cookies=cookie_jar)
auth_payload = {
    'username': 'myusername',
    'password': 'mypassword'
}

auth_response = http.request('POST', 'http://httpbin.org/post', fields=auth_payload)
print(auth_response.data.decode('utf-8'))

response = http.request('GET', 'http://httpbin.org/cookies')
print(response.data.decode('utf-8'))
```

## 5. Request with Cookies
```py
from http.cookiejar import CookieJar
from urllib3 import PoolManager
cookie_jar = CookieJar()
http = PoolManager(cookies=cookie_jar)
http.request('GET', 'http://httpbin.org/cookies/set?mycookie=myvalue')
response = http.request('GET', 'http://httpbin.org/cookies')
print(response.data.decode('utf-8'))
```

## 6. Multipart File Upload
```py
from urllib3 import encode_multipart_formdata
fields = {
    'field1': 'value1',
    'file': ('filename.txt', open('filename.txt', 'rb').read())
}
body, content_type = encode_multipart_formdata(fields)

headers = {'Content-Type': content_type}
response = http.request('POST', 'http://httpbin.org/post', body=body, headers=headers)
print(response.data.decode('utf-8'))
```




## Advance Request like real visitor
```py
import urllib3
import time
import random
from http.cookiejar import CookieJar

# Initialize a CookieJar to handle cookies
cookie_jar = CookieJar()

# Define a list of User-Agent strings
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    # Add more user agents as needed
]

# Create a PoolManager instance
http = urllib3.PoolManager()

# Define the URL to visit
url = 'https://www.linkedin.com/in/samratpy/'

# Randomly select a User-Agent string
headers = {
    'User-Agent': random.choice(user_agents),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/',
    'Connection': 'keep-alive',
    # Add more headers as needed
}

# Make the request with the custom headers
response = http.request('GET', url, headers=headers)

# Print response data or perform other actions
print(response.data.decode('utf-8'))
```
## Real visitor with Proxy
```py
import urllib3
import time
import random
from http.cookiejar import CookieJar

# Initialize a CookieJar to handle cookies
cookie_jar = CookieJar()

# Define a list of User-Agent strings
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    # Add more user agents as needed
]

# Define the URL to visit
url = 'https://www.linkedin.com/in/samratpy/'

# Randomly select a User-Agent string
headers = {
    'User-Agent': random.choice(user_agents),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/',
    'Connection': 'keep-alive',
    # Add more headers as needed
}

# Define proxy settings
proxy_url = 'http://your-proxy-url:port'  # Replace with your proxy URL and port
proxy_headers = {'User-Agent': random.choice(user_agents)}  # Add headers for proxy if required

# Create a ProxyManager instance
proxy_http = urllib3.ProxyManager(proxy_url, headers=proxy_headers)

# Make the request with the custom headers and proxy
response = proxy_http.request('GET', url, headers=headers)

# Print response data or perform other actions
print(response.data.decode('utf-8'))

```

## Request with autheticate custom cookie
```py
import urllib3
import time
import random
from http.cookiejar import Cookie, CookieJar

# Function to parse cookies from the given file format
def load_cookies_from_file(file_path):
    cookie_jar = CookieJar()
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                parts = line.strip().split('\t')
                if len(parts) >= 7:
                    domain, domain_specified, path, secure, expires, name, value = parts[:7]
                    secure = secure == 'TRUE'
                    expires = int(expires) if expires.isdigit() else None
                    cookie = Cookie(
                        version=0,
                        name=name,
                        value=value.strip('"'),
                        port=None,
                        port_specified=False,
                        domain=domain,
                        domain_specified=domain_specified == 'TRUE',
                        domain_initial_dot=domain.startswith('.'),
                        path=path,
                        path_specified=True,
                        secure=secure,
                        expires=expires,
                        discard=False,
                        comment=None,
                        comment_url=None,
                        rest={'HttpOnly': None},
                        rfc2109=False
                    )
                    cookie_jar.set_cookie(cookie)
    return cookie_jar

# Load cookies from the file
cookie_jar = load_cookies_from_file('cookies.txt')

# Define a list of User-Agent strings
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    # Add more user agents as needed
]

# Define the URL to visit
url = 'https://www.linkedin.com/in/samratpy/'

# Randomly select a User-Agent string
headers = {
    'User-Agent': random.choice(user_agents),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/',
    'Connection': 'keep-alive',
    # Add more headers as needed
}

# Create the cookies header
cookies_header = '; '.join([f"{cookie.name}={cookie.value}" for cookie in cookie_jar])

# Add the cookies header to the headers
headers['Cookie'] = cookies_header

# Generate a random mouse movement delay between 1 to 5 seconds
mouse_movement_delay = random.uniform(1, 5)

# Create a PoolManager instance
http = urllib3.PoolManager()

# Make the request with the custom headers
response = http.request('GET', url, headers=headers)

# Simulate waiting for the page to load
time.sleep(mouse_movement_delay)  # Add delay to simulate human behavior

# Print response data or perform other actions
print(response.data.decode('utf-8'))
```
