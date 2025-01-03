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

from automx2.server import MOZILLA_CONFIG_ROUTE
from tests import TestCase
from tests import body


class IndexRoute(TestCase):
    def test_index(self):
        with self.app:
            r = self.get("/")
            self.assertEqual(200, r.status_code)
            self.assertEqual("text/html", r.mimetype)
            x = body(r).find(f'<a href="{MOZILLA_CONFIG_ROUTE}?')
            self.assertNotEqual(-1, x)


class IndexRouteNoDatabase(TestCase):
    create_db = False

    def test_index_without_db(self):
        with self.app:
            r = self.get("/")
            self.assertEqual(200, r.status_code)
            self.assertEqual("text/html", r.mimetype)
            x = body(r).find("Operational error")
            self.assertNotEqual(-1, x)


if __name__ == "__main__":
    unittest.main()
