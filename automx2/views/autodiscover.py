"""
App views: Autoconfigure mail, M$-style.
"""
from flask import Response

from automx2.generators.msoft import MsGenerator
from automx2.views import BaseView


class MailConfig(BaseView):
    def config_response(self, domain_name: str) -> Response:
        data = MsGenerator().client_config(domain_name)
        return self.xml_response(data)
