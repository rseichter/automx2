import unittest
from typing import List
from xml.dom import minidom
from xml.dom.minidom import Element

from automx2.model import EXAMPLE_COM
from automx2.model import EXAMPLE_NET
from automx2.model import EXAMPLE_ORG
from automx2.model import HORUS_IMAP
from automx2.model import HORUS_SMTP
from automx2.model import ORPHAN_DOMAIN
from automx2.model import SERVERLESS_DOMAIN
from automx2.model import SYS4_MAILSERVER
from automx2.model import sample_server_names
from automx2.server import APPLE_CONFIG_ROUTE
from automx2.views import CONTENT_TYPE_XML
from tests.base import TestCase
from tests.base import body


class AppleRoutes(TestCase):
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
            self.assertEqual(200, r.status_code)
            self.assertEqual(CONTENT_TYPE_XML, r.mimetype)
            md = minidom.parseString(body(r))
            plist = md.getElementsByTagName('plist')
            self.assertIsNotNone(plist)
            e: Element = plist[0]
            self.assertEqual('1.0', e.getAttribute('version'))

    def test_apple_domain_match(self):
        with self.app:
            r = self.get_apple_config(f'a@{EXAMPLE_COM}')
            self.assertEqual(200, r.status_code)
            self.assertEqual(CONTENT_TYPE_XML, r.mimetype)
            md = minidom.parseString(body(r))
            self.assert_kv(md, 'OutgoingMailServerHostName', sample_server_names['smtp1'])

    def test_apple_imap(self):
        with self.app:
            r = self.get_apple_config(f'a@{EXAMPLE_ORG}')
            x = self.imap_server_names(minidom.parseString(body(r)))
            self.assertEqual(sample_server_names['imap2'], x[0])

    def test_apple_smtp(self):
        with self.app:
            r = self.get_apple_config(f'a@{EXAMPLE_NET}')
            x = self.smtp_server_names(minidom.parseString(body(r)))
            self.assertEqual(sample_server_names['smtp1'], x[0])

    def test_broken_provider_id(self):
        with self.app:
            r = self.get_apple_config(f'a@{ORPHAN_DOMAIN}')
            b = minidom.parseString(body(r))
            self.assertEqual([], b.getElementsByTagName('PayloadUUID'))

    def test_domain_without_servers(self):
        with self.app:
            r = self.get_apple_config(f'a@{SERVERLESS_DOMAIN}')
            b = minidom.parseString(body(r))
            self.assertEqual([], self.imap_server_names(b))
            self.assertEqual([], self.smtp_server_names(b))

    def test_horus_imap(self):
        with self.app:
            r = self.get_apple_config(f'a@horus-it.com')
            b = minidom.parseString(body(r))
            imap = self.imap_server_names(b)
            self.assertEqual(1, len(imap))
            self.assertEqual(HORUS_IMAP, imap[0])

    def test_horus_smtp(self):
        with self.app:
            r = self.get_apple_config(f'a@horus-it.de')
            b = minidom.parseString(body(r))
            smtp = self.smtp_server_names(b)
            self.assertEqual(1, len(smtp))
            self.assertEqual(HORUS_SMTP, smtp[0])

    def test_sys4_servers(self):
        with self.app:
            r = self.get_apple_config(f'a@sys4.de')
            b = minidom.parseString(body(r))
            imap = self.imap_server_names(b)
            self.assertEqual(1, len(imap))
            smtp = self.smtp_server_names(b)
            self.assertEqual(1, len(smtp))
            self.assertEqual(SYS4_MAILSERVER, imap[0])
            self.assertEqual(SYS4_MAILSERVER, smtp[0])


if __name__ == '__main__':
    unittest.main()
