"""
Configuration generators.
"""
from automx2 import IDENTIFIER


class ConfigGenerator:
    def client_config(self, user_name, domain_name: str) -> str:
        raise NotImplementedError

    @staticmethod
    def branded_id(provider) -> str:
        return f'{IDENTIFIER}-{provider.id}'
