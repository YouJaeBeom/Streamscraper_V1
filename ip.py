import requests

url = "http://icanhazip.com/"

proxies = {
        'http' : 'socks5://127.0.0.1:9070'
        }

re = requests.get(url, proxies=proxies)

print(re.text)
