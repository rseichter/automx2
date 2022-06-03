"""
Copyright © 2019-2022 Ralph Seichter

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
from typing import List, Union
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

import M2Crypto.X509

from automx2 import DomainNotFound
from automx2 import InvalidAuthenticationType
from automx2 import NoProviderForDomain
from automx2 import NoServersForDomain
from automx2 import NoCertsForSigningMobileconfig
from automx2 import NoKeyForSigningMobileconfig
from automx2 import MobileConfigSigningError
from automx2.generators import ConfigGenerator
from automx2.generators import branded_id
from automx2.generators import xml_to_string
from automx2.ldap import LookupResult
from automx2.ldap import STATUS_SUCCESS
from automx2.model import Domain
from automx2.model import Provider
from automx2.model import Server
from automx2.util import expand_placeholders
from automx2.util import socket_type_needs_ssl
from automx2.util import strip_none_values
from automx2.util import unique

from M2Crypto import BIO, SMIME

AUTH_MAP = {
    'none': 'EmailAuthNone',
    'NTLM': 'EmailAuthNTLM',
    'plain': 'EmailAuthPassword',
}
SERVER_TYPE_MAP = {
    'imap': ['Incoming', 'EmailTypeIMAP'],
    'pop': ['Incoming', 'EmailTypePOP'],
    'smtp': ['Outgoing', None],
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


def _str_element(parent: Element, key: str, value: str):
    SubElement(parent, 'key').text = key
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
        SubElement(parent, 'key').text = key
        p = SubElement(parent, 'array')
        for v in value:
            _subtree(p, 'dunno', v)
    else:
        _str_element(parent, key, value)


def _account_payload(local: str, domain: str, account_type: str, account_name: str) -> dict:
    address = f'{local}@{domain}'
    uuid = unique()
    return {
        'EmailAccountDescription': address,
        'EmailAccountName': account_name,
        'EmailAccountType': account_type,
        'EmailAddress': address,
        'IncomingMailServerAuthentication': 'EmailAuthPassword',
        'IncomingMailServerHostName': None,
        'IncomingMailServerPortNumber': -1,
        'IncomingMailServerUseSSL': None,
        'IncomingMailServerUsername': None,
        'OutgoingMailServerAuthentication': 'EmailAuthPassword',
        'OutgoingMailServerHostName': None,
        'OutgoingMailServerPortNumber': -1,
        'OutgoingMailServerUseSSL': None,
        'OutgoingMailServerUsername': None,
        'OutgoingPasswordSameAsIncomingPassword': True,
        'PayloadDescription': f'Email account {address}',
        'PayloadDisplayName': domain,
        'PayloadIdentifier': f'com.apple.mail.managed.{uuid}',
        'PayloadType': 'com.apple.mail.managed',
        'PayloadUUID': uuid,
        'PayloadVersion': 1,
    }


def _config_payload(domain: str, content: dict) -> dict:
    uuid = unique()
    return {
        'PayloadContent': [content],
        'PayloadDisplayName': f'Email account {domain}',
        'PayloadIdentifier': branded_id(uuid),
        'PayloadRemovalDisallowed': False,
        'PayloadType': 'Configuration',
        'PayloadUUID': uuid,
        'PayloadVersion': 1,
    }


def _sanitise(data, local: str, domain: str):
    for k, v in data.items():
        if isinstance(v, list):
            for members in v:
                _sanitise(members, local, domain)
        elif isinstance(v, dict):
            _sanitise(v, local, domain)
        elif isinstance(v, str):
            new = expand_placeholders(v, local, domain)
            data[k] = new


def _map_authentication(server: Server) -> str:
    if server.authentication in AUTH_MAP:
        return AUTH_MAP[server.authentication]
    raise InvalidAuthenticationType(f'Invalid authentication type "{server.authentication}"')


def _preferred_server(servers: List[Server], type_: str) -> Server:
    """Mobileconfig allows for only one inbound (IMAP/POP) and one outbound (SMTP) server.
    This code will find the preferred server of a given type, based on the DB records' priorities
    and on whether candidates support encryption or not.
    """
    encrypted = ['SSL', 'STARTTLS']
    # noinspection PyTypeChecker
    server: Server = None
    for s in servers:
        if s.type == type_:
            if server is None:
                # No previous matching candidate.
                server = s
            elif (server.socket_type not in encrypted) and (s.socket_type in encrypted):
                # Server uses one of the preferred socket types while the candidate does not.
                server = s
    return server


class AppleGenerator(ConfigGenerator):
    def client_config(self, local_part: str, domain_part: str, display_name: str) -> Union[str, bytes]:
        root_element = Element('plist', attrib={'version': '1.0'})
        domain: Domain = Domain.query.filter_by(name=domain_part).first()
        if not domain:
            raise DomainNotFound(f'Domain "{domain_part}" not found')
        provider: Provider = domain.provider
        if not provider:  # pragma: no cover (db constraints prevent this during testing)
            raise NoProviderForDomain(f'No provider for domain "{domain_part}"')
        if not domain.servers:
            raise NoServersForDomain(f'No servers for domain "{domain_part}"')
        if domain.ldapserver:
            lookup_result: LookupResult = self.ldap_lookup(f'{local_part}@{domain_part}', domain.ldapserver)
        else:
            lookup_result = LookupResult(STATUS_SUCCESS, display_name, None)

        servers = self.servers_by_prio(domain.servers)
        mail_server = _preferred_server(servers, 'imap')
        if not mail_server:
            mail_server = _preferred_server(servers, 'pop')
            if not mail_server:
                raise NoServersForDomain(f'No IMAP/POP server for domain "{domain_part}"')
        smtp_server = _preferred_server(servers, 'smtp')
        if not smtp_server:  # pragma: no cover (not expected during testing)
            raise NoServersForDomain(f'No SMTP server for domain "{domain_part}"')
        account = _account_payload(local_part, domain_part, SERVER_TYPE_MAP[mail_server.type][1], lookup_result.cn)
        for server in [mail_server, smtp_server]:
            direction = SERVER_TYPE_MAP[server.type][0]
            account[f'{direction}MailServerHostName'] = server.name
            account[f'{direction}MailServerPortNumber'] = server.port
            account[f'{direction}MailServerUsername'] = self.pick_one(server.user_name, lookup_result.uid)
            account[f'{direction}MailServerAuthentication'] = _map_authentication(server)
            account[f'{direction}MailServerUseSSL'] = socket_type_needs_ssl(server.socket_type)
        config = _config_payload(domain_part, strip_none_values(account))
        _sanitise(config, local_part, domain_part)
        _subtree(root_element, '', config)

        mobileconfig_content = xml_to_string(root_element)

        if provider.sign:
            if not provider.sign_cert:
                raise NoCertsForSigningMobileconfig(
                    f'Mobileconfig signing certificates for provider "{provider.short_name}" are missing')
            if not provider.sign_key:
                raise NoKeyForSigningMobileconfig(
                    f'Mobileconfig signing key provider "{provider.short_name}" is missing')

            mobileconfig_content_bio = BIO.MemoryBuffer(mobileconfig_content)

            pkey_bio = BIO.MemoryBuffer(provider.sign_key.encode('utf-8'))
            cert_bio = BIO.MemoryBuffer(provider.sign_cert.encode('utf-8'))

            try:
                signer = SMIME.SMIME()
                signer.load_key_bio(keybio=pkey_bio, certbio=cert_bio)

                p7f = signer.sign(mobileconfig_content_bio)
                data = BIO.MemoryBuffer(None)
                p7f.write_der(data)

            except (IOError, SMIME.SMIME_Error, SMIME.PKCS7_Error, M2Crypto.X509.X509Error) as e:
                raise MobileConfigSigningError(
                    f'Unable to sign mobileconfig key for provider "{provider.short_name}" and mail address '
                    f'"{local_part}@{domain_part} : "{e}"')

            signed_mobileconfig = data.read()
            return signed_mobileconfig

        return mobileconfig_content
