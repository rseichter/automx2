import unittest
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import fromstring

from automx2.server import MSOFT_CONFIG_ROUTE
from tests.base import BIGCORP_NAME
from tests.base import EXAMPLE_COM
from tests.base import EXAMPLE_NET
from tests.base import EXAMPLE_ORG
from tests.base import HORUS_IMAP
from tests.base import HORUS_SMTP
from tests.base import ORPHAN_DOMAIN
from tests.base import SERVERLESS_DOMAIN
from tests.base import SYS4_MAILSERVER
from tests.base import TestCase
from tests.base import body


class MsRoutes(TestCase):
    def test_ms_missing_arg(self):
        with self.app:
            r = self.get(MSOFT_CONFIG_ROUTE)
            self.assertEqual(400, r.status_code)

    def test_ms_no_domain_match(self):
        with self.app:
            r = self.get_msoft_config('a@b.c')
            self.assertEqual(200, r.status_code)
            self.assertEqual('text/xml', r.mimetype)
            e: Element = fromstring(body(r))
            self.assertEqual('clientConfig', e.tag)
            self.assertEqual('1.1', e.attrib['version'])
            self.assertEqual([], list(e))

    def test_ms_domain_match(self):
        with self.app:
            r = self.get_msoft_config(f'a@{EXAMPLE_COM}')
            self.assertEqual(200, r.status_code)
            self.assertEqual('text/xml', r.mimetype)
            e: Element = fromstring(body(r))
            x = e.findall('emailProvider/displayName')
            self.assertEqual(BIGCORP_NAME, x[0].text)

    def test_ms_imap(self):
        with self.app:
            r = self.get_msoft_config(f'a@{EXAMPLE_ORG}')
            x = self.imap_hostname(fromstring(body(r)))
            self.assertEqual(self.imap2_name, x[0].text)

    def test_ms_smtp(self):
        with self.app:
            r = self.get_msoft_config(f'a@{EXAMPLE_NET}')
            x = self.smtp_hostname(fromstring(body(r)))
            self.assertEqual(self.smtp1_name, x[0].text)

    def test_broken_provider_id(self):
        with self.app:
            with self.assertRaises(AttributeError):
                self.get_msoft_config(f'a@{ORPHAN_DOMAIN}')

    def test_domain_without_servers(self):
        with self.app:
            r = self.get_msoft_config(f'a@{SERVERLESS_DOMAIN}')
            b = fromstring(body(r))
            self.assertEqual([], self.imap_hostname(b))
            self.assertEqual([], self.smtp_hostname(b))

    def test_horus_imap(self):
        with self.app:
            r = self.get_msoft_config(f'a@horus-it.com')
            b = fromstring(body(r))
            imap = self.imap_hostname(b)
            self.assertEqual(1, len(imap))
            self.assertEqual(HORUS_IMAP, imap[0].text)

    def test_horus_smtp(self):
        with self.app:
            r = self.get_msoft_config(f'a@horus-it.de')
            b = fromstring(body(r))
            smtp = self.smtp_hostname(b)
            self.assertEqual(1, len(smtp))
            self.assertEqual(HORUS_SMTP, smtp[0].text)

    def test_sys4_servers(self):
        with self.app:
            r = self.get_msoft_config(f'a@sys4.de')
            b = fromstring(body(r))
            imap = self.imap_hostname(b)
            self.assertEqual(1, len(imap))
            smtp = self.smtp_hostname(b)
            self.assertEqual(1, len(smtp))
            self.assertEqual(SYS4_MAILSERVER, imap[0].text)
            self.assertEqual(SYS4_MAILSERVER, smtp[0].text)


if __name__ == '__main__':
    unittest.main()
