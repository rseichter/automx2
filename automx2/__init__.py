"""
automx2

Successor to 'automx', designed to be easier to configure and use.
Written by Ralph Seichter for sys4 AG.
"""
import logging

IDENTIFIER = 'automx2'
VERSION = '0.0.1.dev7'


class InvalidEMailAddressError(Exception):
    """Email address is invalid/unparseable."""
    pass


log = logging.getLogger(__name__)
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter())
log.addHandler(_handler)
log.setLevel(logging.DEBUG)
