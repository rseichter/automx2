"""
Copyright © 2019-2025 Ralph Seichter

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
from typing import List
from typing import Optional
from urllib.parse import ParseResult
from urllib.parse import urlparse
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from automx2 import DomainNotFound
from automx2 import InvalidAuthenticationType
from automx2 import InvalidServerType
from automx2 import NoProviderForDomain
from automx2 import NoServersForDomain
from automx2 import log
from automx2.generators import ConfigGenerator
from automx2.generators import branded_id
from automx2.generators import xml_to_string
from automx2.ldap import LookupResult
from automx2.ldap import STATUS_SUCCESS
from automx2.model import Davserver
from automx2.model import Domain
from automx2.model import Provider
from automx2.model import Server
from automx2.util import expand_placeholders
from automx2.util import from_environ
from automx2.util import strip_none_values
from automx2.util import unique

PERMIT_CLEARTEXT_PASSWORDS = from_environ('PERMIT_CLEARTEXT_PASSWORDS')

AUTH_MAP = {
    'none': 'EmailAuthNone',
    'NTLM': 'EmailAuthNTLM',
    'plain': 'EmailAuthPassword',
}
DAVSERVER_TYPE_MAP = {
    'caldav': ['CalDAV', 'com.apple.caldav.account'],
    'carddav': ['CardDAV', 'com.apple.carddav.account'],
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


def cleartext_password_if_permitted(password: str, force_permission_for_unittest: bool = False) -> Optional[str]:
    if password is not None and password != '':
        if PERMIT_CLEARTEXT_PASSWORDS == 'I_understand_the_risks' or force_permission_for_unittest:
            return password
        else:
            log.error('Password support is disabled, ignoring provided password.')
    return None


def _account_payload(local: str, domain: str, account_type: str, account_name: str, password: str) -> dict:
    address = f'{local}@{domain}'
    payload_type = 'com.apple.mail.managed'
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
        'IncomingPassword': cleartext_password_if_permitted(password),
        'OutgoingMailServerAuthentication': 'EmailAuthPassword',
        'OutgoingMailServerHostName': None,
        'OutgoingMailServerPortNumber': -1,
        'OutgoingMailServerUseSSL': None,
        'OutgoingMailServerUsername': None,
        'OutgoingPasswordSameAsIncomingPassword': True,
        'PayloadDescription': f'Email account {address}',
        'PayloadDisplayName': domain,
        'PayloadIdentifier': f'{payload_type}.{uuid}',
        'PayloadType': payload_type,
        'PayloadUUID': uuid,
        'PayloadVersion': 1,
    }


def _dav_payload(local: str, domain: str, username: str, password: str, server: Davserver) -> dict:
    address = f'{local}@{domain}'
    account_type = DAVSERVER_TYPE_MAP[server.type][0]
    payload_type = DAVSERVER_TYPE_MAP[server.type][1]
    url: ParseResult = urlparse(server.url)
    port = server.port
    if port < 1:
        port = url.port
    uuid = unique()
    return {
        f'{account_type}AccountDescription': address,
        f'{account_type}HostName': url.hostname,
        f'{account_type}Username': username,
        f'{account_type}Password': cleartext_password_if_permitted(password),
        f'{account_type}UseSSL': server.use_ssl,
        f'{account_type}Port': port,
        f'{account_type}PrincipalURL': server.url,
        'PayloadDescription': f'{account_type} account {address}',
        'PayloadDisplayName': domain,
        'PayloadIdentifier': f'{payload_type}.{uuid}',
        'PayloadType': payload_type,
        'PayloadUUID': uuid,
        'PayloadVersion': 1,
    }


def _config_payload(domain: str, content: List[dict]) -> dict:
    uuid = unique()
    return {
        'PayloadContent': content,
        'PayloadDisplayName': f'{domain} accounts',
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
    def client_config(self, local_part: str, domain_part: str, display_name: str, password: str) -> str:
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
        # Mail servers (mandatory)
        account = _account_payload(
            local=local_part, domain=domain_part,
            account_type=SERVER_TYPE_MAP[mail_server.type][1],
            account_name=lookup_result.cn,
            password=password
        )
        for server in [mail_server, smtp_server]:
            direction = SERVER_TYPE_MAP[server.type][0]
            account[f'{direction}MailServerHostName'] = server.name
            account[f'{direction}MailServerPortNumber'] = server.port
            account[f'{direction}MailServerUsername'] = self.pick_one(server.user_name, lookup_result.uid)
            account[f'{direction}MailServerAuthentication'] = _map_authentication(server)
            account[f'{direction}MailServerUseSSL'] = server.socket_type in ['SSL', 'STARTTLS']
        # CalDAV/CardDAV servers (optional)
        stuff = [strip_none_values(account)]
        for davserver in domain.davservers:
            if davserver.type not in DAVSERVER_TYPE_MAP:  # pragma: no cover (not expected during testing)
                raise InvalidServerType(f'Invalid DAV server type "{davserver.type}"')
            username = self.pick_one(davserver.user_name, lookup_result.uid)
            davaccount = _dav_payload(
                local=local_part,
                domain=domain_part,
                username=username,
                password=password,
                server=davserver
            )
            stuff.append(strip_none_values(davaccount))
        config = _config_payload(domain_part, stuff)
        _sanitise(config, local_part, domain_part)
        _subtree(root_element, '', config)
        return xml_to_string(root_element)
