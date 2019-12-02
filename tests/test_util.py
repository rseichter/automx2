import os
import unittest

from automx2 import InvalidEMailAddressError
from automx2.util import from_environ
from automx2.util import parse_email_address
from tests.base import unique


class UtilTests(unittest.TestCase):
    DOES_NOT_EXIST = unique()
    EXISTS = unique()
    VALUE = unique()

    def setUp(self) -> None:
        os.environ[self.EXISTS] = self.VALUE

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
        local, domain = parse_email_address('a@b.c')
        self.assertEqual('a', local)
        self.assertEqual('b.c', domain)

    def test_invalid_email_address(self):
        with self.assertRaises(InvalidEMailAddressError):
            parse_email_address('abc')

    def test_email_address_none(self):
        with self.assertRaises(InvalidEMailAddressError):
            # noinspection PyTypeChecker
            parse_email_address(None)


if __name__ == '__main__':
    unittest.main()
