import random
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_random_proxy() -> Dict[str, str]:
    proxy_list = get_proxy_list()

    for i in range(0, 5):
        try:
            random_proxy = random.choice(proxy_list)
            shown_ip = test_proxy(proxy_ip=random_proxy['ip'], proxy_port=random_proxy['port'])
            assert shown_ip == random_proxy['ip'], 'shown IP address is not the same as proxy IP'
        except Exception:
            pass
        else:
            return random_proxy
    raise Exception('no working proxy found')


def get_proxy_list() -> List[Dict[str, str]]:
    proxies_url = 'https://www.sslproxies.org/'
    ua = UserAgent()
    user_agent = ua.random

    page_obj = requests.get(proxies_url, headers={'User-Agent': user_agent})

    soup = BeautifulSoup(page_obj.text, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    proxy_list = []
    for row in proxies_table.tbody.find_all('tr'):
        table_cels = row.find_all('td')
        proxy_list.append({
            'ip': table_cels[0].string,
            'port': table_cels[1].string
        })

    return proxy_list


def test_proxy(proxy_ip: str, proxy_port: str) -> str:
    proxies = {
        'http': f'http://{proxy_ip}:{proxy_port}'
    }

    page_obj = requests.get('http://icanhazip.com', proxies=proxies)
    shown_ip = page_obj.text.strip('\n')

    return shown_ip


if __name__ == '__main__':
    random_proxy = get_random_proxy()

    print(random_proxy)
