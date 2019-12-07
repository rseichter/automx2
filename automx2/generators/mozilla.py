"""
Configuration generator for Mozilla XML DOM.
See https://wiki.mozilla.org/Thunderbird:Autoconfiguration:ConfigFileFormat
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
