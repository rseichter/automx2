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

import unittest

from automx2 import AutomxException
from automx2.server import INITDB_ROUTE
from tests import TestCase
from tests import body


class DatabaseRoute(TestCase):
    create_db = False

    def test_init_internal(self):
        with self.app:
            r = self.get(INITDB_ROUTE)
            self.assertEqual(200, r.status_code)
            self.assertEqual("text/html", r.mimetype)
            x = body(r).find("Database is now prepared")
            self.assertNotEqual(-1, x)

    def test_init_incomplete(self):
        with self.app:
            with self.assertRaises(AutomxException):
                self.post(INITDB_ROUTE, json={"a": "b"})

    def test_init_json(self):
        data = {
            "provider": "Test Provider",
            "domains": ["test.com"],
            "servers": [
                {"name": "imap", "type": "imap"},
                {"name": "pop", "type": "pop"},
                {"name": "smtp", "type": "smtp"},
            ],
        }
        with self.app:
            r = self.post(INITDB_ROUTE, json=data)
            self.assertEqual(200, r.status_code)
            self.assertEqual("text/html", r.mimetype)
            self.assertNotEqual(-1, body(r).find("Database is now prepared"))

    def test_purge_db(self):
        with self.app:
            r = self.get(INITDB_ROUTE)
            self.assertEqual(200, r.status_code)
            r = self.app.delete(INITDB_ROUTE)
            self.assertEqual(200, r.status_code)
            self.assertNotEqual(-1, body(r).find("Database content purged"))


if __name__ == "__main__":
    unittest.main()
