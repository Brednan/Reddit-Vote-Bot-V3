from proxy_server_api import ProxyServerAPI
from vote_bot import vote_bot, get_date_time_str, get_accounts
from proxy_checker import check_proxy, check_proxies
from utilities import *


if __name__ == '__main__':
    vote_dir = 0

    while True:
        vote_type_input = input('Enter vote type (upvote, downvote): ').lower()
        if vote_type_input in ('upvote', 'downvote'):
            break
        print('Vote type invalid! Please try again')

    while True:
        post_id = input('Enter post ID: ').lower()
        if post_id:
            break
        print('Post ID invalid! Please try again')

    if vote_type_input == 'upvote':
        vote_dir = 1
    elif vote_type_input == 'downvote':
        vote_dir = -1

    with open('./proxy_server_ip', 'r') as f:
        proxy_api_ip = f.read()

    api = ProxyServerAPI(proxy_api_ip, 65433, True)
    proxies = check_proxies(api.get_proxies())

    accounts = get_accounts('./accounts.txt')
    vote_bot(accounts, proxies, post_id, vote_dir)

    # TODO: Make an object that keeps track of the progress and is able to print it out (i.e displays number of
    #  successful or failed attempts)
