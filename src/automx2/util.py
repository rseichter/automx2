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

import os
import re
from uuid import uuid4

from automx2 import AutomxException
from automx2 import InvalidEMailAddressError
from automx2 import PLACEHOLDER_ADDRESS
from automx2 import PLACEHOLDER_DOMAIN
from automx2 import PLACEHOLDER_LOCALPART
from automx2 import log

email_address_re = re.compile(r"^([^@]+)@([^@]+)$", re.IGNORECASE)


def dictget_optional(data: dict, key: str, default: object = None):
    if key in data:
        return data[key]
    return default


def dictget_mandatory(data: dict, key: str):
    if key in data:
        return data[key]
    raise AutomxException(f'Missing mandatory key "{key}"')


def from_environ(env_var_name: str, default: object = None):
    if env_var_name in os.environ:
        return os.environ[env_var_name]
    return default


def parse_email_address(address: str):
    if address:
        match = email_address_re.search(address)
        if match:
            return match[1], match[2]
    raise InvalidEMailAddressError("Invalid email address")


def unique() -> str:
    return uuid4().hex


def expand_placeholders(string: str, local_part: str, domain_part: str) -> str:
    if not string:
        return ""
    placeholder_map = {
        PLACEHOLDER_ADDRESS: f"{local_part}@{domain_part}",
        PLACEHOLDER_DOMAIN: domain_part,
        PLACEHOLDER_LOCALPART: local_part,
    }
    for k, v in placeholder_map.items():
        string = string.replace(k, v)
    return string


def socket_type_needs_ssl(socket_type: str):
    """Map socket type to True (use SSL) or False (do not use SSL)."""
    if "SSL" == socket_type:
        return True
    elif "STARTTLS" != socket_type:
        """
        Existing versions auf automx2 return False for socket types other than
        SSL and STARTTLS. This can cause unexpected results. Future automx2 versions
        will raise an exception for invalid socket types, so log an error to notify
        users of this upcoming change.
        """
        log.error(
            f'Unexpected socket type "{socket_type}" will cause a failure in future versions'
        )
    return False


def strip_none_values(data: dict) -> dict:
    """Return copy of a dict containing only keys without 'None' values."""
    return {k: v for (k, v) in data.items() if v is not None}
