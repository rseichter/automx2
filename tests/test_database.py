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
