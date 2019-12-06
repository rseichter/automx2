"""
Flask application views.
"""
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import fromstring

from flask import Response
from flask import make_response
from flask import request
from flask import views

from automx2 import log
from automx2.generators.outlook import NS_AUTODISCOVER
from automx2.util import parse_email_address

# Keys are case-sensitive when used in XML
EMAIL_MOZILLA = 'emailaddress'
EMAIL_OUTLOOK = 'EMailAddress'

CONTENT_TYPE = 'Content-Type'
CONTENT_TYPE_XML = 'application/xml'


class BaseView(views.MethodView):
    # noinspection PyMethodMayBeStatic
    def get(self):
        """Mozilla-style GET request is expected to contain ?address=user@example.com"""
        address = request.args.get(EMAIL_MOZILLA, '')
        if not address:
            message = f'Missing request argument "{EMAIL_MOZILLA}"'
            log.error(message)
            return message, 400
        return self.config_from_address(address)

    # noinspection PyMethodMayBeStatic
    def post(self):
        """Outlook-style POST request is expected to contain XML."""
        if not self.is_xml_request():
            message = f'Required content type is "{CONTENT_TYPE_XML}"'
            log.error(message)
            return message, 400
        element: Element = fromstring(str(request.data, encoding='utf-8', errors='strict'))
        ns = {'n': NS_AUTODISCOVER}
        element = element.find(f'n:Request/n:{EMAIL_OUTLOOK}', ns)
        if element is None:
            message = f'Missing request argument "{EMAIL_OUTLOOK}"'
            log.error(message)
            return message, 400
        return self.config_from_address(element.text)

    def config_from_address(self, address: str) -> Response:
        local_part, domain_part = parse_email_address(address)
        data = self.config_response(local_part, domain_part)
        return self.xml_response(data)

    def config_response(self, local_part, domain_part: str) -> str:
        raise NotImplementedError

    @staticmethod
    def is_xml_request() -> bool:
        if CONTENT_TYPE in request.headers:
            return request.headers[CONTENT_TYPE] == CONTENT_TYPE_XML
        return False

    @staticmethod
    def xml_response(data: object) -> Response:
        response: Response = make_response(data)
        response.headers[CONTENT_TYPE] = CONTENT_TYPE_XML
        return response
