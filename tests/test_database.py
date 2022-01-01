"""
Copyright © 2019-2022 Ralph Seichter

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

from tests.base import TestCase
from tests.base import body


class DatabaseRoute(TestCase):
    create_db = False

    def test_init_db(self):
        with self.app:
            r = self.get('/initdb/')
            self.assertEqual(200, r.status_code)
            self.assertEqual('text/html', r.mimetype)
            x = body(r).find('Database is now prepared')
            self.assertNotEqual(-1, x)


if __name__ == '__main__':
    unittest.main()
