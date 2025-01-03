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

from automx2.server import _sd_notify


class ServerTests(unittest.TestCase):
    """Tests for server.py methods."""

    def test_invalid_socket(self):
        os.environ["NOTIFY_SOCKET"] = "foo"
        with self.assertRaises(OSError):
            _sd_notify("")

    def test_missing_socket(self):
        os.environ["NOTIFY_SOCKET"] = "/missing/socket"
        self.assertFalse(_sd_notify(""))


if __name__ == "__main__":
    unittest.main()
