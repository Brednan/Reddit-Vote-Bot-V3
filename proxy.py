def filter_duplicate_proxies(proxies: list) -> list:
    filtered_proxies = []

    for proxy in proxies:
        is_duplicate = False
        for filtered_proxy in filtered_proxies:
            if proxy.ip == filtered_proxy.ip:
                is_duplicate = True
                break

        if not is_duplicate:
            filtered_proxies.append(proxy)

    return filtered_proxies


class Proxy:
    def __init__(self, ip, port, protocol, anonymity_level=None):
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.anonymity_level = anonymity_level

    def __repr__(self):
        return f'{self.ip}:{self.port}'

    def __str__(self):
        return f'{self.ip}:{self.port}'
