"""
Flask application views.
"""
from flask import Response
from flask import make_response
from flask import request
from flask import views

from automx2 import ADDRESS_KEY
from automx2 import log
from automx2.util import parse_email_address


class BaseView(views.MethodView):
    # noinspection PyMethodMayBeStatic
    def get(self):
        address = request.args.get(ADDRESS_KEY, '')
        if not address:
            message = f'Missing request argument "{ADDRESS_KEY}"'
            log.error(message)
            return message, 400
        local_part, domain_part = parse_email_address(address)
        data = self.config_response(domain_part)
        return self.xml_response(data)

    def config_response(self, domain_name: str) -> Response:
        raise NotImplementedError

    @staticmethod
    def xml_response(data: object) -> Response:
        response: Response = make_response(data)
        response.headers['Content-Type'] = 'text/xml'
        return response
