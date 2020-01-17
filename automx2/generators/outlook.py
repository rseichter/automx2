"""
Copyright © 2019-2020 Ralph Seichter

Graciously sponsored by sys4 AG <https://sys4.de/>

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
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import tostring

from automx2 import DomainNotFound
from automx2 import InvalidServerType
from automx2.generators import ConfigGenerator
from automx2.model import Domain
from automx2.model import Server

NS_AUTODISCOVER = 'http://schemas.microsoft.com/exchange/autodiscover/outlook/requestschema/2006'
NS_RESPONSE = 'http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a'

TYPE_MAP = {
    'imap': 'IMAP',
    'smtp': 'SMTP',
}


class OutlookGenerator(ConfigGenerator):
    """Configuration generator for Outlook et al.

    See https://support.microsoft.com/en-us/help/3211279/outlook-2016-implementation-of-autodiscover
    """

    @staticmethod
    def on_off(condition: bool) -> str:
        if condition:
            return 'on'
        return 'off'

    def protocol_element(self, parent: Element, server: Server) -> Element:
        element = SubElement(parent, 'Protocol')
        SubElement(element, 'Type').text = TYPE_MAP[server.type]
        SubElement(element, 'Server').text = server.name
        SubElement(element, 'Port').text = str(server.port)
        SubElement(element, 'LoginName').text = server.user_name
        SubElement(element, 'SSL').text = self.on_off('SSL' == server.authentication)
        SubElement(element, 'AuthRequired').text = self.on_off(True)
        return element

    def client_config(self, user_name, domain_name: str, realname: str, password: str) -> str:
        domain: Domain = Domain.query.filter_by(name=domain_name).first()
        autodiscover = Element('Autodiscover', attrib={'xmlns': NS_AUTODISCOVER})
        response = SubElement(autodiscover, 'Response', attrib={'xmlns': NS_RESPONSE})
        if not domain:
            raise DomainNotFound(f'Domain "{domain_name}" not found')
        account = SubElement(response, 'Account')
        SubElement(account, 'AccountType').text = 'email'
        SubElement(account, 'Action').text = 'settings'
        for server in domain.servers:
            if server.type not in TYPE_MAP:
                raise InvalidServerType(f'Invalid server type "{server.type}"')
            self.protocol_element(account, server)
        data = tostring(autodiscover, 'utf-8')
        return data
