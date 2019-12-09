"""
Copyright © 2019 Ralph Seichter

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

from automx2 import InvalidServerType
from automx2 import log
from automx2.generators import ConfigGenerator
from automx2.generators import branded_id
from automx2.model import Domain
from automx2.model import Provider
from automx2.model import Server

TYPE_DIRECTION_MAP = {
    'imap': 'incoming',
    'smtp': 'outgoing',
}


class MozillaGenerator(ConfigGenerator):
    @staticmethod
    def server_element(parent: Element, server: Server) -> Element:
        direction = TYPE_DIRECTION_MAP[server.type]
        element = SubElement(parent, f'{direction}Server', attrib={'type': server.type})
        SubElement(element, 'hostname').text = server.name
        SubElement(element, 'port').text = str(server.port)
        SubElement(element, 'socketType').text = server.socket_type
        SubElement(element, 'username').text = server.user_name
        SubElement(element, 'authentication').text = server.authentication
        return element

    def client_config(self, user_name, domain_name: str, realname: str, password: str) -> str:
        root = Element('clientConfig', attrib={'version': '1.1'})
        domain: Domain = Domain.query.filter_by(name=domain_name).first()
        if domain:
            provider: Provider = domain.provider
            provider_element = SubElement(root, 'emailProvider', attrib={'id': branded_id(provider.id)})
            SubElement(provider_element, 'identity')  # Deliberately left empty
            for provider_domain in provider.domains:
                SubElement(provider_element, 'domain').text = provider_domain.name
            SubElement(provider_element, 'displayName').text = provider.name
            SubElement(provider_element, 'displayShortName').text = provider.short_name
            for server in domain.servers:
                if server.type not in TYPE_DIRECTION_MAP:
                    raise InvalidServerType(f'Invalid server type "{server.type}"')
                self.server_element(provider_element, server)
        else:
            log.error(f'No provider for domain "{domain_name}"')
        data = tostring(root, 'utf-8')
        return data
