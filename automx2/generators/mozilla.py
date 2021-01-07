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
from xml.etree.ElementTree import SubElement

from automx2 import DomainNotFound
from automx2 import InvalidServerType
from automx2 import NoProviderForDomain
from automx2.generators import ConfigGenerator
from automx2.generators import branded_id
from automx2.generators import xml_to_string
from automx2.ldap import LookupResult
from automx2.ldap import STATUS_SUCCESS
from automx2.model import Domain
from automx2.model import Provider
from automx2.model import Server

SERVER_TYPE_MAP = {
    'imap': ['incoming', 'imap'],
    'pop': ['incoming', 'pop3'],
    'smtp': ['outgoing', 'smtp'],
}


class MozillaGenerator(ConfigGenerator):
    def server_element(self, parent: Element, server: Server, override_uid: str = None) -> None:
        direction = SERVER_TYPE_MAP[server.type][0]
        type_attrib = SERVER_TYPE_MAP[server.type][1]
        element = SubElement(parent, f'{direction}Server', attrib={'type': type_attrib})
        SubElement(element, 'hostname').text = server.name
        SubElement(element, 'port').text = str(server.port)
        SubElement(element, 'socketType').text = server.socket_type
        SubElement(element, 'username').text = self.pick_one(server.user_name, override_uid)
        SubElement(element, 'authentication').text = server.authentication

    def client_config(self, local_part, domain_part: str, display_name: str) -> str:
        root_element = Element('clientConfig', attrib={'version': '1.1'})
        domain: Domain = Domain.query.filter_by(name=domain_part).first()
        if not domain:
            raise DomainNotFound(f'Domain "{domain_part}" not found')
        if domain.ldapserver:
            lookup_result: LookupResult = self.ldap_lookup(f'{local_part}@{domain_part}', domain.ldapserver)
        else:
            lookup_result = LookupResult(STATUS_SUCCESS, display_name, None)
        provider: Provider = domain.provider
        if not provider:
            raise NoProviderForDomain(f'No provider for domain "{domain_part}"')
        provider_element = SubElement(root_element, 'emailProvider', attrib={'id': branded_id(provider.id)})
        SubElement(provider_element, 'identity')  # Deliberately left empty
        for provider_domain in provider.domains:
            SubElement(provider_element, 'domain').text = provider_domain.name
        SubElement(provider_element, 'displayName').text = provider.name
        SubElement(provider_element, 'displayShortName').text = provider.short_name
        for server in self.servers_by_prio(domain.servers):
            if server.type not in SERVER_TYPE_MAP:
                raise InvalidServerType(f'Invalid server type "{server.type}"')
            self.server_element(provider_element, server, lookup_result.uid)
        return xml_to_string(root_element)
