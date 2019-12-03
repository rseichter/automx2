import unittest
from typing import List
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import fromstring

from automx2.model import BIGCORP_NAME
from automx2.model import EXAMPLE_COM
from automx2.model import EXAMPLE_NET
from automx2.model import EXAMPLE_ORG
from automx2.model import HORUS_IMAP
from automx2.model import HORUS_SMTP
from automx2.model import ORPHAN_DOMAIN
from automx2.model import SERVERLESS_DOMAIN
from automx2.model import SYS4_MAILSERVER
from automx2.model import sample_server_names
from automx2.server import MOZILLA_CONFIG_ROUTE
from automx2.views import CONTENT_TYPE_XML
from tests.base import TestCase
from tests.base import body


class MozillaRoutes(TestCase):
    @staticmethod
    def imap_server_elements(element: Element) -> List[Element]:
        return element.findall('emailProvider/incomingServer/[@type="imap"]/hostname')

    @staticmethod
    def smtp_server_elements(element: Element) -> List[Element]:
        return element.findall('emailProvider/outgoingServer/[@type="smtp"]/hostname')

    def test_mozilla_missing_arg(self):
        with self.app:
            r = self.get(MOZILLA_CONFIG_ROUTE)
            self.assertEqual(400, r.status_code)

    def test_mozilla_no_domain_match(self):
        with self.app:
            r = self.get_mozilla_config('a@b.c')
            self.assertEqual(200, r.status_code)
            self.assertEqual(CONTENT_TYPE_XML, r.mimetype)
            e: Element = fromstring(body(r))
            self.assertEqual('clientConfig', e.tag)
            self.assertEqual('1.1', e.attrib['version'])
            self.assertEqual([], list(e))

    def test_mozilla_domain_match(self):
        with self.app:
            r = self.get_mozilla_config(f'a@{EXAMPLE_COM}')
            self.assertEqual(200, r.status_code)
            self.assertEqual(CONTENT_TYPE_XML, r.mimetype)
            e: Element = fromstring(body(r))
            x = e.findall('emailProvider/displayName')
            self.assertEqual(BIGCORP_NAME, x[0].text)

    def test_mozilla_imap(self):
        with self.app:
            r = self.get_mozilla_config(f'a@{EXAMPLE_ORG}')
            x = self.imap_server_elements(fromstring(body(r)))
            self.assertEqual(sample_server_names['imap2'], x[0].text)

    def test_mozilla_smtp(self):
        with self.app:
            r = self.get_mozilla_config(f'a@{EXAMPLE_NET}')
            x = self.smtp_server_elements(fromstring(body(r)))
            self.assertEqual(sample_server_names['smtp1'], x[0].text)

    def test_broken_provider_id(self):
        with self.app:
            with self.assertRaises(AttributeError):
                self.get_mozilla_config(f'a@{ORPHAN_DOMAIN}')

    def test_domain_without_servers(self):
        with self.app:
            r = self.get_mozilla_config(f'a@{SERVERLESS_DOMAIN}')
            b = fromstring(body(r))
            self.assertEqual([], self.imap_server_elements(b))
            self.assertEqual([], self.smtp_server_elements(b))

    def test_horus_imap(self):
        with self.app:
            r = self.get_mozilla_config(f'a@horus-it.com')
            b = fromstring(body(r))
            imap = self.imap_server_elements(b)
            self.assertEqual(1, len(imap))
            self.assertEqual(HORUS_IMAP, imap[0].text)

    def test_horus_smtp(self):
        with self.app:
            r = self.get_mozilla_config(f'a@horus-it.de')
            b = fromstring(body(r))
            smtp = self.smtp_server_elements(b)
            self.assertEqual(1, len(smtp))
            self.assertEqual(HORUS_SMTP, smtp[0].text)

    def test_sys4_servers(self):
        with self.app:
            r = self.get_mozilla_config(f'a@sys4.de')
            b = fromstring(body(r))
            imap = self.imap_server_elements(b)
            self.assertEqual(1, len(imap))
            smtp = self.smtp_server_elements(b)
            self.assertEqual(1, len(smtp))
            self.assertEqual(SYS4_MAILSERVER, imap[0].text)
            self.assertEqual(SYS4_MAILSERVER, smtp[0].text)


if __name__ == '__main__':
    unittest.main()
