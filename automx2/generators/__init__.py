"""
Configuration generators.
"""


class ConfigGenerator:
    def client_config(self, domain_name: str) -> str:
        raise NotImplementedError
