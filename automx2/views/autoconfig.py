"""
App views: Autoconfigure mail, Mozilla-style.
"""
from flask import abort
from flask import request
from flask.views import MethodView

from automx2 import AutomxException
from automx2 import log
from automx2.generators.mozilla import MozillaGenerator
from automx2.views import EMAIL_MOZILLA
from automx2.views import MailConfig


class MozillaMailConfig(MailConfig, MethodView):
    def get(self):
        """GET request is expected to contain ?emailaddress=user@example.com"""
        address = request.args.get(EMAIL_MOZILLA, '')
        if not address:
            message = f'Missing request argument "{EMAIL_MOZILLA}"'
            log.error(message)
            return message, 400
        try:
            return self.config_from_address(address)
        except AutomxException as e:
            log.exception(e)
            abort(400)

    def config_response(self, local_part, domain_part: str, realname: str, password: str) -> str:
        data = MozillaGenerator().client_config(local_part, domain_part, realname, password)
        return data
