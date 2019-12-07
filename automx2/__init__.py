"""
automx2

Successor to 'automx', designed to be easier to configure and use.
Written by Ralph Seichter for sys4 AG.
"""
import logging

IDENTIFIER = 'automx2'
VERSION = '0.0.1.dev13'

PLACEHOLDER_ADDRESS = r'%EMAILADDRESS%'
PLACEHOLDER_DOMAIN = r'%EMAILDOMAIN%'
PLACEHOLDER_LOCALPART = r'%EMAILLOCALPART%'


class AutomxException(Exception):
    """Exception base class for this application."""
    pass


class InvalidEMailAddressError(AutomxException):
    """Email address is invalid/unparseable."""
    pass


class DomainNotFound(AutomxException):
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


log = logging.getLogger(__name__)
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter())
log.addHandler(_handler)
log.setLevel(logging.DEBUG)
