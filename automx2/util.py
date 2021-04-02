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
    if not string:
        return ''
    placeholder_map = {
        PLACEHOLDER_ADDRESS: f'{local_part}@{domain_part}',
        PLACEHOLDER_DOMAIN: domain_part,
        PLACEHOLDER_LOCALPART: local_part,
    }
    for k, v in placeholder_map.items():
        string = string.replace(k, v)
    return string
