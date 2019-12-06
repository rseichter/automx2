"""
App views: Autoconfigure mail, Apple-style.
"""

from automx2.generators.apple import AppleGenerator
from automx2.views import BaseView


class MailConfig(BaseView):
    def config_response(self, local_part, domain_part: str) -> str:
        data = AppleGenerator().client_config(local_part, domain_part)
        return data
