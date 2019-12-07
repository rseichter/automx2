"""
Various utility functions.
"""
import os
import re
from uuid import uuid4

from automx2 import InvalidEMailAddressError
from automx2 import PLACEHOLDER_ADDRESS
from automx2 import PLACEHOLDER_DOMAIN
from automx2 import PLACEHOLDER_LOCALPART

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
    raise InvalidEMailAddressError('Invalid email address')


def unique() -> str:
    return uuid4().hex


def expand_placeholders(string: str, local_part: str, domain_part: str) -> str:
    placeholder_map = {
        PLACEHOLDER_ADDRESS: f'{local_part}@{domain_part}',
        PLACEHOLDER_DOMAIN: domain_part,
        PLACEHOLDER_LOCALPART: local_part,
    }
    for k, v in placeholder_map.items():
        string = string.replace(k, v)
    return string
