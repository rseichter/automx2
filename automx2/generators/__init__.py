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
from typing import List
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring

from automx2 import IDENTIFIER
from automx2 import LdapLookupError
from automx2 import LdapNoMatch
from automx2.ldap import LdapAccess
from automx2.ldap import LookupResult
from automx2.ldap import STATUS_ERROR
from automx2.ldap import STATUS_NO_MATCH
from automx2.model import Ldapserver
from automx2.model import Server


def branded_id(id_) -> str:
    return f'{IDENTIFIER}-{id_}'


def xml_to_string(root_element: Element) -> str:
    return tostring(root_element, 'utf-8')


class ConfigGenerator:
    def client_config(self, local_part: str, domain_part: str, display_name: str) -> str:
        raise NotImplementedError

    @staticmethod
    def ldap_lookup(email_address: str, server: Ldapserver) -> LookupResult:
        if not (server and server.name):
            raise LdapLookupError('No LDAP server specified')
        ldap = LdapAccess(server.name, port=server.port, use_ssl=server.use_ssl,
                          user=server.bind_user, password=server.bind_password)
        r = ldap.lookup(server.search_base, server.search_filter.format(email_address),
                        attr_cn=server.attr_cn, attr_uid=server.attr_uid)
        if r.status == STATUS_ERROR:  # pragma: no cover
            raise LdapLookupError('LDAP bind failed')
        elif r.status == STATUS_NO_MATCH:  # pragma: no cover
            raise LdapNoMatch(f'No LDAP match for <{email_address}>')
        return r

    @staticmethod
    def pick_one(low_prio_value, high_prio_value):
        if high_prio_value:
            return high_prio_value
        return low_prio_value

    @staticmethod
    def servers_by_prio(servers: List[Server]) -> List[Server]:
        return sorted(servers, key=lambda _server: _server.prio)
