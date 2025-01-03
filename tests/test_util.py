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
import unittest

from automx2 import InvalidEMailAddressError
from automx2 import PLACEHOLDER_ADDRESS
from automx2 import PLACEHOLDER_DOMAIN
from automx2 import PLACEHOLDER_LOCALPART
from automx2.util import expand_placeholders
from automx2.util import dictget_optional
from automx2.util import from_environ
from automx2.util import parse_email_address
from automx2.util import socket_type_needs_ssl
from automx2.util import unique


class UtilTests(unittest.TestCase):
    """Tests for utility methods."""

    DOES_NOT_EXIST = unique()
    EXISTS = unique()
    VALUE = unique()

    def setUp(self) -> None:
        os.environ[self.EXISTS] = self.VALUE

    def test_key_exists(self):
        self.assertEqual("b", dictget_optional({"a": "b"}, "a", None))

    def test_key_missing(self):
        self.assertEqual("c", dictget_optional({}, "a", "c"))

    def test_exists(self):
        x = from_environ(self.EXISTS)
        self.assertEqual(self.VALUE, x)

    def test_does_not_exist(self):
        x = from_environ(self.DOES_NOT_EXIST)
        self.assertIsNone(x)

    def test_does_not_exist_with_default(self):
        default = unique()
        x = from_environ(self.DOES_NOT_EXIST, default=default)
        self.assertEqual(default, x)

    def test_valid_email_address(self):
        local, domain = parse_email_address("a@b.c")
        self.assertEqual("a", local)
        self.assertEqual("b.c", domain)

    def test_invalid_email_address(self):
        with self.assertRaises(InvalidEMailAddressError):
            parse_email_address("abc")

    def test_email_address_none(self):
        with self.assertRaises(InvalidEMailAddressError):
            # noinspection PyTypeChecker
            parse_email_address(None)

    def test_expand(self):
        local = "a"
        domain = "b.c"
        self.assertEqual(
            "1a@b.c2", expand_placeholders(f"1{PLACEHOLDER_ADDRESS}2", local, domain)
        )
        self.assertEqual(
            "3a4", expand_placeholders(f"3{PLACEHOLDER_LOCALPART}4", local, domain)
        )
        self.assertEqual(
            "5b.c6", expand_placeholders(f"5{PLACEHOLDER_DOMAIN}6", local, domain)
        )

    def test_needs_ssl(self):
        self.assertTrue(socket_type_needs_ssl("SSL"))
        self.assertFalse(socket_type_needs_ssl("STARTTLS"))
        self.assertFalse(socket_type_needs_ssl("INVALID"))


if __name__ == "__main__":
    unittest.main()
