"""
Configuration generator for Apple's property-list based mobileconfig
"""
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import tostring

from automx2 import DomainNotFound
from automx2 import InvalidServerType
from automx2 import NoProviderForDomain
from automx2 import NoServersForDomain
from automx2.generators import ConfigGenerator
from automx2.generators import branded_id
from automx2.model import Domain
from automx2.model import Provider
from automx2.util import expand_placeholders
from automx2.util import unique

TYPE_DIRECTION_MAP = {
    'imap': 'Incoming',
    'smtp': 'Outgoing',
}


def _bool_element(parent: Element, key: str, value: bool):
    SubElement(parent, 'key').text = key
    if value:
        v = 'true'
    else:
        v = 'false'
    SubElement(parent, v)


def _int_element(parent: Element, key: str, value: int):
    SubElement(parent, 'key').text = key
    SubElement(parent, 'integer').text = str(value)


def _str_element(parent: Element, key: str, value: str = ''):
    SubElement(parent, 'key').text = key
    if value:
        SubElement(parent, 'string').text = value


def _subtree(parent: Element, key: str, value):
    if isinstance(value, bool):
        _bool_element(parent, key, value)
    elif isinstance(value, dict):
        p = SubElement(parent, 'dict')
        for k, v in value.items():
            _subtree(p, k, v)
    elif isinstance(value, int):
        _int_element(parent, key, value)
    elif isinstance(value, list):
        _str_element(parent, key)
        p = SubElement(parent, 'array')
        for v in value:
            _subtree(p, 'dunno', v)
    else:
        _str_element(parent, key, value)


def _payload(local_part, domain_part):
    local = expand_placeholders(local_part, local_part, domain_part)
    domain = expand_placeholders(domain_part, local_part, domain_part)
    address = f'{local}@{domain}'
    uuid = unique()
    inner = {
        'EmailAccountDescription': '',
        'EmailAccountName': address,
        'EmailAccountType': 'EmailTypeIMAP',
        'EmailAddress': address,
        'IncomingMailServerAuthentication': 'EmailAuthPassword',
        'IncomingMailServerHostName': None,
        'IncomingMailServerPortNumber': -1,
        'IncomingMailServerUseSSL': True,
        'IncomingMailServerUsername': local,
        'IncomingPassword': '',
        'OutgoingMailServerAuthentication': 'EmailAuthPassword',
        'OutgoingMailServerHostName': None,
        'OutgoingMailServerPortNumber': -1,
        'OutgoingMailServerUseSSL': True,
        'OutgoingMailServerUsername': local,
        'OutgoingPasswordSameAsIncomingPassword': True,
        'PayloadDescription': 'Email account configuration',
        'PayloadDisplayName': domain,
        'PayloadIdentifier': f'com.apple.mail.managed.{uuid}',
        'PayloadType': 'com.apple.mail.managed',
        'PayloadUUID': uuid,
        'PayloadVersion': 1,
        'SMIMEEnablePerMessageSwitch': False,
        'SMIMEEnabled': False,
        'SMIMEEncryptionEnabled': False,
        'SMIMESigningEnabled': False,
        'allowMailDrop': False,
        'disableMailRecentsSyncing': False,
    }
    uuid = unique()
    outer = {
        'PayloadContent': [inner],
        'PayloadDisplayName': f'{domain} email account',
        'PayloadIdentifier': branded_id(uuid),
        'PayloadRemovalDisallowed': False,
        'PayloadType': 'Configuration',
        'PayloadUUID': uuid,
        'PayloadVersion': 1,
    }
    return inner, outer


class AppleGenerator(ConfigGenerator):
    def client_config(self, local_part, domain_part: str) -> str:
        domain: Domain = Domain.query.filter_by(name=domain_part).first()
        if not domain:
            raise DomainNotFound(f'Domain "{domain_part}" not found')
        provider: Provider = domain.provider
        if not provider:
            raise NoProviderForDomain(f'No provider for domain "{domain_part}"')
        if not domain.servers:
            raise NoServersForDomain(f'No servers for domain "{domain_part}"')
        inner, outer = _payload(local_part, domain_part)
        for server in domain.servers:
            if server.type not in TYPE_DIRECTION_MAP:
                raise InvalidServerType(f'Invalid server type "{server.type}"')
            direction = TYPE_DIRECTION_MAP[server.type]
            inner[f'{direction}MailServerHostName'] = server.name
            inner[f'{direction}MailServerPortNumber'] = server.port
        inner['PayloadDescription'] = f'Hosted by {provider.name}'
        plist = Element('plist', attrib={'version': '1.0'})
        _subtree(plist, '', outer)
        data = tostring(plist, 'utf-8')
        return data
