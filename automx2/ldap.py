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
from collections import namedtuple

from ldap3 import Connection
from ldap3 import Server

from automx2 import log

STATUS_SUCCESS = 0
STATUS_ERROR = 1
STATUS_NO_MATCH = 2

LookupResult = namedtuple('LookupResult', 'status cn uid')


class LdapAccess:
    def __init__(self, hostname, port=636, use_ssl=True, user=None, password=None) -> None:
        self._server = Server(hostname, port=port, use_ssl=use_ssl)
        self._connection = Connection(self._server, lazy=False, read_only=True, user=user, password=password)

    def lookup(self, search_base: str, search_filter: str, attr_uid='uid', attr_cn=None) -> LookupResult:
        if not self._connection.bind():  # pragma: no cover (bind errors are not expected during unittests)
            log.error(f'LDAP bind failed: {self._connection.result}')
            return LookupResult(STATUS_ERROR, None, None)
        attributes = [attr_uid]
        if attr_cn:
            attributes.append(attr_cn)
        self._connection.search(search_base, search_filter, attributes=attributes, size_limit=1)
        if self._connection.response:
            ldap_entry = self._connection.response[0]
            log.debug(f'LDAP match {ldap_entry["dn"]}')
            cn = self.get_attribute(ldap_entry, attr_cn)
            uid = self.get_attribute(ldap_entry, attr_uid)
            result = LookupResult(STATUS_SUCCESS, cn, uid)
        else:
            log.warning(f'No LDAP match for filter {search_filter}')
            result = LookupResult(STATUS_NO_MATCH, None, None)
        self._connection.unbind()
        log.debug(result)
        return result

    @staticmethod
    def get_attribute(ldap_entry: dict, attribute: str):
        attributes = ldap_entry['attributes']
        if attribute and attribute in attributes:
            value = attributes[attribute]
            if isinstance(value, str):  # pragma: no cover (Will not happen when testing against OpenLDAP)
                log.debug(f'Returning string "{value}"')
                return value
            elif isinstance(value, list):
                log.debug(f'Returning list element "{value[0]}"')
                return value[0]
            log.error(f'Unexpected lookup result type: {type(value).__name__}')
        elif attribute:
            log.warning(f"Attribute '{attribute}' not found")
        return None
