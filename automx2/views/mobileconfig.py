"""
App views: Autoconfigure mail, Apple-style.
"""

from automx2.generators.apple import AppleGenerator
from automx2.views import BaseView

CONTENT_TYPE_APPLE = 'application/x-apple-aspen-config'


class MailConfig(BaseView):
    @staticmethod
    def response_type() -> str:
        return CONTENT_TYPE_APPLE

    def config_response(self, local_part, domain_part: str, realname: str, password: str) -> str:
        data = AppleGenerator().client_config(local_part, domain_part, realname, password)
        return data
