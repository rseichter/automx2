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
import unittest
from typing import List
from xml.dom import minidom
from xml.dom.minidom import Element

from automx2 import InvalidAuthenticationType
from automx2 import PLACEHOLDER_ADDRESS
from automx2.model import EGGS_DOMAIN
from automx2.model import EXAMPLE_COM
from automx2.model import EXAMPLE_NET
from automx2.model import EXAMPLE_ORG
from automx2.model import ORPHAN_DOMAIN
from automx2.model import SERVERLESS_DOMAIN
from automx2.model import Server
from automx2.model import sample_server_names
from automx2.server import APPLE_CONFIG_ROUTE
from automx2.views.mobileconfig import CONTENT_TYPE_APPLE
from tests.base import TestCase
from tests.base import body


class AppleRoutes(TestCase):
    """Tests for Mobileconfig routes."""

    def assert_kv(self, _minidom, key: str, value: str):
        elements = _minidom.getElementsByTagName('key')
        element: Element
        for element in elements:
            if key == element.firstChild.data:
                sibling = element.nextSibling
                self.assertEqual(value, sibling.firstChild.data)
                return
        raise AssertionError(f'Key/value pair ({key}/{value}) not found')

    @staticmethod
    def mail_server_names(_minidom, incoming: bool) -> List[Element]:
        r = []
        if incoming:
            whut = 'Incoming'
        else:
            whut = 'Outgoing'
        elements = _minidom.getElementsByTagName('key')
        element: Element
        for element in elements:
            if f'{whut}MailServerHostName' == element.firstChild.data:
                sibling = element.nextSibling
                r.append(sibling.firstChild.data)
        return r

    def imap_server_names(self, _minidom) -> List[Element]:
        return self.mail_server_names(_minidom, True)

    def smtp_server_names(self, _minidom) -> List[Element]:
        return self.mail_server_names(_minidom, False)

    def test_apple_missing_arg(self):
        with self.app:
            r = self.get(APPLE_CONFIG_ROUTE)
            self.assertEqual(400, r.status_code)

    def test_apple_no_domain_match(self):
        with self.app:
            r = self.get_apple_config('a@b.c')
            self.assertEqual(204, r.status_code)

    def test_apple_domain_match(self):
        with self.app:
            r = self.get_apple_config(f'a@{EXAMPLE_COM}')
            self.assertEqual(200, r.status_code)
            self.assertEqual(CONTENT_TYPE_APPLE, r.mimetype)
            md = minidom.parseString(body(r))
            self.assert_kv(md, 'OutgoingMailServerHostName', sample_server_names['smtp1'])

    def test_apple_pop(self):
        with self.app:
            r = self.get_apple_config(f'a@{EXAMPLE_ORG}')
            x = self.imap_server_names(minidom.parseString(body(r)))
            self.assertEqual(sample_server_names['pop1'], x[0])

    def test_apple_smtp(self):
        with self.app:
            r = self.get_apple_config(f'a@{EXAMPLE_NET}')
            x = self.smtp_server_names(minidom.parseString(body(r)))
            self.assertEqual(sample_server_names['smtp1'], x[0])

    def test_broken_provider_id(self):
        with self.app:
            r = self.get_apple_config(f'a@{ORPHAN_DOMAIN}')
            self.assertEqual(400, r.status_code)

    def test_domain_without_servers(self):
        with self.app:
            r = self.get_apple_config(f'a@{SERVERLESS_DOMAIN}')
            self.assertEqual(400, r.status_code)

    def test_invalid_server(self):
        with self.app:
            r = self.get_apple_config(f'a@{EGGS_DOMAIN}')
            self.assertEqual(400, r.status_code)

    def test_sanitise_dict(self):
        from automx2.generators.apple import _sanitise
        with self.app:
            d1 = {'b': PLACEHOLDER_ADDRESS}
            d2 = {'a': d1}
            _sanitise(d2, 'x', 'y')
            self.assertEqual('x@y', d1['b'])

    def test_sanitise_valid(self):
        from automx2.generators.apple import _sanitise
        with self.app:
            d = {'a': PLACEHOLDER_ADDRESS}
            _sanitise(d, 'l', 'd')
            self.assertEqual('l@d', d['a'])

    def test_sanitise_missing(self):
        from automx2.generators.apple import _sanitise
        with self.app:
            with self.assertRaises(TypeError):
                _sanitise({'a': None}, 'l', 'd')

    def test_map_bad_auth(self):
        from automx2.generators.apple import _map_authentication
        with self.app:
            s = Server(authentication='BAD')
            with self.assertRaises(InvalidAuthenticationType):
                _map_authentication(s)

    def test_map_valid_auth(self):
        from automx2.generators.apple import _map_authentication, AUTH_MAP
        with self.app:
            for k, v in AUTH_MAP.items():
                s = Server(authentication=k)
                self.assertEqual(AUTH_MAP[k], _map_authentication(s))

    def test_map_bad_socktype(self):
        from automx2.generators.apple import _map_socket_type
        with self.app:
            s = Server(socket_type='BAD')
            self.assertFalse(_map_socket_type(s))

    def test_map_valid_socktype(self):
        from automx2.generators.apple import _map_socket_type
        with self.app:
            s1 = Server(socket_type='SSL')
            s2 = Server(socket_type='STARTTLS')
            self.assertTrue(_map_socket_type(s1))
            self.assertTrue(_map_socket_type(s2))


if __name__ == '__main__':
    unittest.main()
