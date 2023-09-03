import requests
from proxy import *
import threading


def check_proxy(proxy: Proxy):
    if proxy.protocol in ('http', 'https'):
        proxy_schema = {
            'http': f'http://{proxy.__str__()}',
            'https': f'http://{proxy.__str__()}'
        }

    elif proxy.protocol in ('socks4', 'socks5'):
        proxy_schema = {
            'http': f'{proxy.protocol}://{proxy.__str__()}',
            'https': f'{proxy.protocol}://{proxy.__str__()}'
        }

    else:
        return False

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.'
                      '0 Safari/537.36'
    }

    try:
        res = requests.get('https://www.reddit.com/', headers=headers, proxies=proxy_schema, timeout=10)
    except requests.exceptions.RequestException:
        return False

    if 200 <= res.status_code < 300:
        return True

    return False


def check_proxy_thread(proxy: Proxy, checked_proxies: list, lock: threading.Lock):
    if check_proxy(proxy):
        with lock:
            checked_proxies.append(proxy)


def check_proxies(proxies: list) -> list:
    thread_lock = threading.Lock()
    checked_proxies = []

    threads = []
    for proxy in proxies:
        while threading.active_count() > 4096:
            pass

        thread = threading.Thread(target=check_proxy_thread, args=(proxy, checked_proxies, thread_lock))
        thread.start()
        threads.append(thread)

    for thread in threads:
        if thread.is_alive():
            thread.join()

    return checked_proxies
