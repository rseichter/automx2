"""
Various utility functions.
"""
import os
import re
from uuid import uuid4

from automx2 import InvalidEMailAddressError

email_address_re = re.compile(r'^([^@]+)@([^@]+)$', re.IGNORECASE)


def from_environ(env_var_name: str, default: object = None):
    if env_var_name in os.environ:
        return os.environ[env_var_name]
    return default


def parse_email_address(address: str):
    if address:
        match = email_address_re.search(address)
        if match:
            return match[1], match[2]
    raise InvalidEMailAddressError


def unique() -> str:
    return uuid4().hex