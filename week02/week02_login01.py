import time
import requests
from fake_useragent import UserAgent

headers = {
    'referer': 'https://shimo.im/login?from=home',
    'authority': 'shimo.im',
    'scheme': 'https',
    'origin': 'https://shimo.im',
    'x-requested-with': 'XmlHttpRequest',
    'x-source': 'lizard-desktop',
    }

formdata = {
    "mobile": '+8615688888888', 
    'password': 'yourpasswd'
    }

rs = requests.Session()

rsp = rs.post('https://shimo.im/lizard-api/auth/password/login', data = formdata, headers = headers)

url2 = 'https://shimo.im/profile#setting-email'

rsg = rs.get(url2,headers = headers,cookies=rs.cookies)

print(r2g.text)