"""
Various utility functions.
"""
import os
import re

email_address_re = re.compile(r'^([^@]+)@([^@]+)$', re.IGNORECASE)


def from_environ(env_var_name: str, default: object = None):
    if env_var_name in os.environ:
        return os.environ[env_var_name]
    return default


def parse_email_address(address: str):
    match = email_address_re.search(address)
    if not match:
        return 'INVALID_LOCAL', 'INVALID_DOMAIN'
    return match[1], match[2]
