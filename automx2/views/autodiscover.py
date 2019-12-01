"""
App views: Autoconfigure mail, M$-style.
"""
from flask import request
from flask.views import MethodView

from automx2 import ADDRESS_KEY
from automx2 import log
from automx2.generators.mozilla import client_config
from automx2.util import parse_email_address
from automx2.views import xml_response


class MailConfig(MethodView):
    # noinspection PyMethodMayBeStatic
    def get(self):
        address = request.args.get(ADDRESS_KEY, '')
        if not address:
            message = f'Missing request argument "{ADDRESS_KEY}"'
            log.error(message)
            return message, 400
        local_part, domain_part = parse_email_address(address)
        data = client_config(domain_part)
        return xml_response(data)
