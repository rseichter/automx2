"""
Configuration generators.
"""
from automx2 import IDENTIFIER


def branded_id(id_: str) -> str:
    return f'{IDENTIFIER}-{id_}'


class ConfigGenerator:
    def client_config(self, user_name, domain_name: str, realname: str, password: str) -> str:
        raise NotImplementedError
