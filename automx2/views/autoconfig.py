"""
App views: Autoconfigure mail, Mozilla-style.
"""

from automx2.generators.mozilla import MozillaGenerator
from automx2.views import BaseView


class MailConfig(BaseView):
    def config_response(self, local_part, domain_part: str) -> str:
        data = MozillaGenerator().client_config(local_part, domain_part)
        return data
