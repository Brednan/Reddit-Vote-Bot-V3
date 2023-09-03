import datetime
import os
from account_credentials import AccountCredentials


def get_date_time_str():
    current_date_time = datetime.datetime.now()

    return f'{current_date_time.year}/{current_date_time.month:02d}/{current_date_time.day:02d} {current_date_time.hour:02d}:' \
           f'{current_date_time.minute:02d}'


def get_database_credentials() -> tuple:
    with open('./mysql.txt', 'r') as f:
        content = f.read().split('\n')
        mysql_ip = content[0]
        mysql_username = content[1]

    env_vars = os.environ
    return mysql_ip, mysql_username, env_vars.get('mysql_pass')


def get_accounts(accounts_path: str):
    account_list = []

    with open(accounts_path, 'r') as f:
        content = f.read()

        for account in content.strip().split('\n'):
            account_split = account.split(':')
            account_list.append(AccountCredentials(account_split[0], account_split[1]))

    return account_list
