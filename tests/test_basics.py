"""
Test basic functions of the automx2 Flask application.
"""
import unittest
from typing import List
from uuid import uuid1
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import fromstring

from flask import Response

from automx2 import ADDRESS_KEY
from automx2 import IDENTIFIER
from automx2.model import Domain
from automx2.model import Provider
from automx2.model import Server
from automx2.model import db
from automx2.server import MOZILLA_CONFIG_ROUTE
from automx2.server import app

HORUS_SMTP = 'smtp.horus-it.com'

HORUS_IMAP = 'imap.horus-it.com'

EXAMPLE_COM = 'example.com'
EXAMPLE_NET = 'example.net'
EXAMPLE_ORG = 'example.org'
ORPHAN_DOMAIN = 'orphan.tld'
SERVERLESS_DOMAIN = 'serverless.tld'

BIGCORP_NAME = 'Big Corporation, Inc.'
BIGCORP_SHORT = 'BigCorp'
HORUS_NAME = 'HORUS-IT Ralph Seichter'
HORUS_SHORT = 'HORUS-IT'
SYS4_MAILSERVER = 'mail.sys4.de'
SYS4_NAME = 'sys4 AG'
SYS4_SHORT = 'sys4'


def body(response: Response) -> str:
    return str(response.data, encoding='utf-8', errors='strict')


def unique() -> str:
    # UUID1 is sufficiently random for unittests
    return uuid1().hex


class TestCase(unittest.TestCase):
    imap1_name = unique()
    imap2_name = unique()
    smtp1_name = unique()
    smtp2_name = unique()

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        # app.config['SQLALCHEMY_ECHO'] = False
        # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////tmp/{IDENTIFIER}_unittest.sqlite'
        self.app = app.test_client()
        with app.app_context():
            db.init_app(app)
            db.drop_all()
            db.create_all()
            self.populate_db()
            db.session.commit()

    def tearDown(self) -> None:
        with app.app_context():
            db.drop_all()
            db.session.commit()

    def get(self, *args, **kwargs) -> Response:
        kwargs['follow_redirects'] = True
        return self.app.get(*args, **kwargs)

    def get_mozilla_config(self, address: str) -> Response:
        return self.get(f'{MOZILLA_CONFIG_ROUTE}?{ADDRESS_KEY}={address}')

    def populate_db(self):
        """Populate with some fixed samples."""
        id = 1000
        bigcorp = Provider(id=id, name=BIGCORP_NAME, short_name=BIGCORP_SHORT)
        id += 1
        horus = Provider(id=id, name=HORUS_NAME, short_name=HORUS_SHORT)
        id += 1
        sys4 = Provider(id=id, name=HORUS_NAME, short_name=HORUS_SHORT)
        db.session.add_all([bigcorp, horus, sys4])

        id = 2000
        d1 = Domain(id=id, name=EXAMPLE_COM, provider=bigcorp)
        id += 1
        d2 = Domain(id=id, name=EXAMPLE_NET, provider=bigcorp)
        id += 1
        d3 = Domain(id=id, name=EXAMPLE_ORG, provider=bigcorp)
        id += 1
        d1_horus = Domain(id=id, name='horus-it.de', provider=horus)
        id += 1
        d2_horus = Domain(id=id, name='horus-it.com', provider=horus)
        id += 1
        d1_sys4 = Domain(id=id, name='sys4.de', provider=sys4)
        id += 1
        orphan_domain = Domain(id=id, name=ORPHAN_DOMAIN, provider_id=(-1 * id))
        id += 1
        serverless_domain = Domain(id=id, name=SERVERLESS_DOMAIN, provider=bigcorp)
        horus_domains = [d1_horus, d2_horus]
        sys4_domains = [d1_sys4]
        db.session.add_all([d1, d2, d3])
        db.session.add_all(horus_domains)
        db.session.add_all(sys4_domains)
        db.session.add_all([orphan_domain, serverless_domain])

        id = 3000
        s1 = Server(id=id, type='smtp', port=587, name=self.smtp1_name, domains=[d1, d2])
        id += 1
        s2 = Server(id=id, type='smtp', port=587, name=self.smtp2_name, domains=[d3])
        id += 1
        s3 = Server(id=id, type='imap', port=143, name=self.imap1_name, domains=[d1])
        id += 1
        s4 = Server(id=id, type='imap', port=143, name=self.imap2_name, domains=[d2, d3])
        id += 1
        s5 = Server(id=id, type='imap', port=993, socket_type='SSL', name=HORUS_IMAP, domains=horus_domains)
        id += 1
        s6 = Server(id=id, type='smtp', port=587, name=HORUS_SMTP, domains=horus_domains)
        id += 1
        s7 = Server(id=id, type='imap', port=143, name=SYS4_MAILSERVER, domains=sys4_domains)
        id += 1
        s8 = Server(id=id, type='smtp', port=587, name=SYS4_MAILSERVER, domains=sys4_domains)
        db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8])

    @staticmethod
    def imap_hostname(element: Element) -> List[Element]:
        return element.findall('emailProvider/incomingServer/[@type="imap"]/hostname')

    @staticmethod
    def smtp_hostname(element: Element) -> List[Element]:
        return element.findall('emailProvider/outgoingServer/[@type="smtp"]/hostname')


class RouteTests(TestCase):
    def test_index(self):
        with self.app:
            r = self.get('/')
            self.assertEqual(200, r.status_code)
            self.assertEqual('text/html', r.mimetype)
            x = body(r).find(f'<a href="{MOZILLA_CONFIG_ROUTE}?')
            self.assertNotEqual(-1, x)

    def test_mozilla_missing_arg(self):
        with self.app:
            r = self.get(MOZILLA_CONFIG_ROUTE)
            self.assertEqual(400, r.status_code)

    def test_mozilla_no_domain_match(self):
        with self.app:
            r = self.get_mozilla_config('a@b.c')
            self.assertEqual(200, r.status_code)
            self.assertEqual('text/xml', r.mimetype)
            e: Element = fromstring(body(r))
            self.assertEqual('clientConfig', e.tag)
            self.assertEqual('1.1', e.attrib['version'])
            self.assertEqual([], list(e))

    def test_mozilla_domain_match(self):
        with self.app:
            r = self.get_mozilla_config(f'a@{EXAMPLE_COM}')
            self.assertEqual(200, r.status_code)
            self.assertEqual('text/xml', r.mimetype)
            e: Element = fromstring(body(r))
            x = e.findall('emailProvider/displayName')
            self.assertEqual(BIGCORP_NAME, x[0].text)

    def test_mozilla_imap(self):
        with self.app:
            r = self.get_mozilla_config(f'a@{EXAMPLE_ORG}')
            x = self.imap_hostname(fromstring(body(r)))
            self.assertEqual(self.imap2_name, x[0].text)

    def test_mozilla_smtp(self):
        with self.app:
            r = self.get_mozilla_config(f'a@{EXAMPLE_NET}')
            x = self.smtp_hostname(fromstring(body(r)))
            self.assertEqual(self.smtp1_name, x[0].text)

    def test_broken_provider_id(self):
        with self.app:
            with self.assertRaises(AttributeError):
                self.get_mozilla_config(f'a@{ORPHAN_DOMAIN}')

    def test_domain_without_servers(self):
        with self.app:
            r = self.get_mozilla_config(f'a@{SERVERLESS_DOMAIN}')
            b = fromstring(body(r))
            self.assertEqual([], self.imap_hostname(b))
            self.assertEqual([], self.smtp_hostname(b))

    def test_horus_imap(self):
        with self.app:
            r = self.get_mozilla_config(f'a@horus-it.com')
            b = fromstring(body(r))
            imap = self.imap_hostname(b)
            self.assertEqual(1, len(imap))
            self.assertEqual(HORUS_IMAP, imap[0].text)

    def test_horus_smtp(self):
        with self.app:
            r = self.get_mozilla_config(f'a@horus-it.de')
            b = fromstring(body(r))
            smtp = self.smtp_hostname(b)
            self.assertEqual(1, len(smtp))
            self.assertEqual(HORUS_SMTP, smtp[0].text)

    def test_sys4_servers(self):
        with self.app:
            r = self.get_mozilla_config(f'a@sys4.de')
            b = fromstring(body(r))
            imap = self.imap_hostname(b)
            self.assertEqual(1, len(imap))
            smtp = self.smtp_hostname(b)
            self.assertEqual(1, len(smtp))
            self.assertEqual(SYS4_MAILSERVER, imap[0].text)
            self.assertEqual(SYS4_MAILSERVER, smtp[0].text)


if __name__ == '__main__':
    unittest.main()
