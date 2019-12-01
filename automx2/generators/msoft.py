"""
Configuration generator for Outlook et al.
See https://support.microsoft.com/en-us/help/3211279/outlook-2016-implementation-of-autodiscover
"""
from automx2.generators import ConfigGenerator


class MsGenerator(ConfigGenerator):
    def client_config(self, domain_name: str) -> str:
        return '<message>TODO: Implement this!</message>'
