"""
Copyright © 2019-2021 Ralph Seichter

Sponsored by sys4 AG <https://sys4.de/>

This file is part of automx2.

automx2 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

automx2 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with automx2. If not, see <https://www.gnu.org/licenses/>.
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
            return request.headers[CONTENT_TYPE] == CONTENT_TYPE_XML or request.headers[CONTENT_TYPE] == 'text/xml'
        return False
