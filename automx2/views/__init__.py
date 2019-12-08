"""
Flask application views.
"""

from flask import Response
from flask import make_response
from flask import request

from automx2.util import parse_email_address

# Keys are case-sensitive when used in XML
EMAIL_MOZILLA = 'emailaddress'
EMAIL_OUTLOOK = 'EMailAddress'

CONTENT_TYPE = 'Content-Type'
CONTENT_TYPE_XML = 'application/xml'


class MailConfig:
    def config_from_address(self, address: str, realname: str = '', password: str = '') -> Response:
        local_part, domain_part = parse_email_address(address)
        data = self.config_response(local_part, domain_part, realname, password)
        return self.response_with_type(data)

    def config_response(self, local_part, domain_part: str, realname: str, password: str) -> str:
        raise NotImplementedError

    @staticmethod
    def response_type() -> str:
        return CONTENT_TYPE_XML

    def response_with_type(self, data: object) -> Response:
        response: Response = make_response(data)
        response.headers[CONTENT_TYPE] = self.response_type()
        return response

    @staticmethod
    def is_xml_request() -> bool:
        if CONTENT_TYPE in request.headers:
            return request.headers[CONTENT_TYPE] == CONTENT_TYPE_XML
        return False
