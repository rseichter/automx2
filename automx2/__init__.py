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
import logging

IDENTIFIER = 'automx2'  # Do not change this!
VERSION = '2021.3.1'

PLACEHOLDER_ADDRESS = r'%EMAILADDRESS%'
PLACEHOLDER_DOMAIN = r'%EMAILDOMAIN%'
PLACEHOLDER_LOCALPART = r'%EMAILLOCALPART%'


class AutomxException(Exception):
    """Exception base class for this application.

    Will result in HTTP code 400 (bad request).
    """
    pass


class NotFoundException(AutomxException):
    """Exception base class for lookup failures etc.

    Will result in HTTP code 204 (no content).
    """
    pass


class InvalidEMailAddressError(AutomxException):
    """Email address is invalid/unparseable."""
    pass


class DomainNotFound(NotFoundException):
    """Database did not contain the given domain."""
    pass


class NoProviderForDomain(AutomxException):
    """Database did not contain a provider for the given address."""
    pass


class NoServersForDomain(AutomxException):
    """Database did not contain any servers for the given address."""
    pass


class InvalidServerType(AutomxException):
    """Database contains an invalid server type."""
    pass


class InvalidAuthenticationType(AutomxException):
    """Database contains an invalid authentication type."""
    pass


class LdapLookupError(AutomxException):
    """LDAP lookup failed."""
    pass


class LdapNoMatch(NotFoundException):
    """LDAP lookup returned no match."""
    pass


log = logging.getLogger(__name__)
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter())
log.addHandler(_handler)
log.setLevel(logging.DEBUG)
log.warning(f'Running {IDENTIFIER} version {VERSION}')
