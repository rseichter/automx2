import unittest

from automx2.server import MOZILLA_CONFIG_ROUTE
from tests.base import TestCase
from tests.base import body


class IndexRoute(TestCase):
    def test_index(self):
        with self.app:
            r = self.get('/')
            self.assertEqual(200, r.status_code)
            self.assertEqual('text/html', r.mimetype)
            x = body(r).find(f'<a href="{MOZILLA_CONFIG_ROUTE}?')
            self.assertNotEqual(-1, x)


class IndexRouteNoDatabase(TestCase):
    create_db = False

    def test_index_without_db(self):
        with self.app:
            r = self.get('/')
            self.assertEqual(200, r.status_code)
            self.assertEqual('text/html', r.mimetype)
            x = body(r).find('Operational error')
            self.assertNotEqual(-1, x)


if __name__ == '__main__':
    unittest.main()
