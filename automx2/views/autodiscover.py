"""
App views: Autoconfigure mail, M$-style.
"""

from automx2.generators.outlook import OutlookGenerator
from automx2.views import BaseView


class MailConfig(BaseView):
    def config_response(self, local_part, domain_part: str, realname: str, password: str) -> str:
        data = OutlookGenerator().client_config(local_part, domain_part, realname, password)
        return data
