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
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import fromstring

from flask import abort
from flask import request
from flask.views import MethodView

from automx2 import AutomxException
from automx2 import NotFoundException
from automx2 import log
from automx2.generators.outlook import NS_REQUEST
from automx2.generators.outlook import OutlookGenerator
from automx2.views import CONTENT_TYPE_XML
from automx2.views import EMAIL_OUTLOOK
from automx2.views import MailConfig


class OutlookView(MailConfig, MethodView):
    """Autoconfigure mail, Outlook-style."""

    def post(self):
        """Outlook-style POST request is expected to contain XML."""
        if not self.is_xml_request():
            message = f'Required content type is "{CONTENT_TYPE_XML}"'
            log.error(message)
            return message, 400
        element: Element = fromstring(str(request.data, encoding='utf-8', errors='strict'))
        ns = {'n': NS_REQUEST}
        element = element.find(f'n:Request/n:{EMAIL_OUTLOOK}', ns)
        if element is None:
            message = f'Missing request argument "{EMAIL_OUTLOOK}"'
            log.error(message)
            return message, 400
        try:
            return self.config_from_address(element.text)
        except NotFoundException:
            return '', 204
        except AutomxException as e:
            log.exception(e)
            abort(400)

    def config_response(self, local_part, domain_part: str, realname: str, password: str) -> str:
        data = OutlookGenerator().client_config(local_part, domain_part, realname)
        return data
