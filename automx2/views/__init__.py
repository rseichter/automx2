"""
Flask application views.
"""
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import fromstring

from flask import Response
from flask import make_response
from flask import request
from flask import views

from automx2 import ADDRESS_KEY
from automx2 import log
from automx2.util import parse_email_address

MSOFT_NAMESPACE = r'{http://schemas.microsoft.com/exchange/autodiscover/outlook/requestschema/2006}'


class BaseView(views.MethodView):
    # noinspection PyMethodMayBeStatic
    def get(self):
        address = request.args.get(ADDRESS_KEY, '')
        if not address:
            message = f'Missing request argument "{ADDRESS_KEY}"'
            log.error(message)
            return message, 400
        return self.config_from_address(address)

    # noinspection PyMethodMayBeStatic
    def post(self):
        if 'text/xml' != request.headers['Content-Type']:
            message = f'Unexpected request content type'
            log.error(message)
            return message, 400
        root: Element = fromstring(str(request.data, encoding='utf-8', errors='strict'))
        e = root.findall(f'{MSOFT_NAMESPACE}Request/{MSOFT_NAMESPACE}EMailAddress')
        return self.config_from_address(e[0].text)

    def config_from_address(self, address: str) -> Response:
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
