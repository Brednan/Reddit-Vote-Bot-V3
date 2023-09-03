import json
from requests import Session
import requests
from bs4 import BeautifulSoup
from proxy import *
import random
from utilities import *
from account_credentials import *


def get_auth_token(soup: BeautifulSoup):
    script = soup.find('script', {'id': 'data'}).text
    script_json_content = json.loads(script[13:len(script) - 1])

    return script_json_content.get('user').get('session').get('accessToken')


def login_to_reddit(account: AccountCredentials, proxy: Proxy):

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
        return None

    session = Session()
    session.proxies.update(proxy_schema)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.'
                      '0 Safari/537.36',
        'Origin': 'https://www.reddit.com',
        'Referer': 'https://www.reddit.com/login/'
    })

    res = session.get('https://www.reddit.com/login')
    soup = BeautifulSoup(res.content, 'html.parser')

    csrf_token = soup.find('input', {'name': 'csrf_token'}).get('value')
    if not csrf_token:
        return None

    post_data = {
        'app_name': 'web3x',
        'csrf_token': csrf_token,
        'password': account.password,
        'dest': 'https://www.reddit.com',
        'username': account.username
    }

    res = session.post('https://www.reddit.com/login', data=post_data)

    if not res:
        return None

    if not 200 <= res.status_code < 300:
        return None

    res = session.get('https://www.reddit.com/')

    if not res:
        return None

    if not 200 <= res.status_code < 300:
        return None

    soup = BeautifulSoup(res.content, 'html.parser')
    auth_token = get_auth_token(soup)

    session.headers.update({
        'Authorization': f'Bearer {auth_token}'
    })

    return session


def send_vote_request(session: Session, post_id: str, vote_type: int):
    payload = {
        'id': f'{post_id}',
        'dir': vote_type,
        'api_type': 'json'
    }

    res = session.post('https://oauth.reddit.com/api/vote?redditWebClient=desktop2x&app=desktop2x-client-production&raw'
                       '_json=1&gilding_detail=1', data=payload)

    if res.status_code == 200:
        return True

    return False


def vote(account_credentials: AccountCredentials, proxies: list, post_id: str, vote_dir: int):
    attempt = 0
    rand = random.Random(20)

    while attempt < len(proxies):
        try:
            session = login_to_reddit(account_credentials, proxies[rand.randint(0, len(proxies) - 1)])

            if not session:
                print(f'{get_date_time_str()} - Upvote failed!')
                break

            if send_vote_request(session, post_id, vote_dir):
                print(f'{get_date_time_str()} - Successfully voted!')
            else:
                print(f'{get_date_time_str()} - Upvote failed!')

            break

        except requests.exceptions.ConnectionError:
            attempt += 1


def vote_bot(accounts: list, proxies: list, post_id: str, vote_dir: int):
    for account in accounts:
        vote(account, proxies, post_id, vote_dir)
