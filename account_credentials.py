from dataclasses import dataclass


@dataclass
class AccountCredentials:
    username: str
    password: str
