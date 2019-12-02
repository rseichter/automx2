"""
Test basic functions of the automx2 Flask application.
"""
import unittest
from uuid import uuid1

from flask import Response

from automx2.generators.outlook import NS_AUTODISCOVER
from automx2.generators.outlook import NS_RESPONSE
from automx2.model import Domain
from automx2.model import Provider
from automx2.model import Server
from automx2.model import db
from automx2.server import MOZILLA_CONFIG_ROUTE
from automx2.server import MSOFT_CONFIG_ROUTE
from automx2.server import app
from automx2.views import CONTENT_TYPE_XML
from automx2.views import EMAIL_MOZILLA
from automx2.views import EMAIL_OUTLOOK

EXAMPLE_COM = 'example.com'
EXAMPLE_NET = 'example.net'
EXAMPLE_ORG = 'example.org'
ORPHAN_DOMAIN = 'orphan.tld'
SERVERLESS_DOMAIN = 'serverless.tld'

BIGCORP_NAME = 'Big Corporation, Inc.'
BIGCORP_SHORT = 'BigCorp'
HORUS_IMAP = 'imap.horus-it.com'
HORUS_NAME = 'HORUS-IT Ralph Seichter'
HORUS_SHORT = 'HORUS-IT'
HORUS_SMTP = 'smtp.horus-it.com'
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
    create_db = True

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        with app.app_context():
            db.init_app(app)
            db.drop_all()
            if self.create_db:
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

    def post(self, *args, **kwargs) -> Response:
        kwargs['follow_redirects'] = True
        return self.app.post(*args, **kwargs)

    def get_mozilla_config(self, address: str) -> Response:
        return self.get(f'{MOZILLA_CONFIG_ROUTE}?{EMAIL_MOZILLA}={address}')

    def get_msoft_config(self, address: str) -> Response:
        data = (
            f'<Autodiscover xmlns="{NS_AUTODISCOVER}">'
            f'<AcceptableResponseSchema>{NS_RESPONSE}</AcceptableResponseSchema>'
            '<Request>'
            f'<{EMAIL_OUTLOOK}>{address}</{EMAIL_OUTLOOK}>'
            '</Request>'
            '</Autodiscover>'
        )
        return self.post(MSOFT_CONFIG_ROUTE, data=data, content_type=CONTENT_TYPE_XML)

    def populate_db(self):
        """Populate with some fixed samples."""
        i = 1000
        bigcorp = Provider(id=i, name=BIGCORP_NAME, short_name=BIGCORP_SHORT)
        i += 1
        horus = Provider(id=i, name=HORUS_NAME, short_name=HORUS_SHORT)
        i += 1
        sys4 = Provider(id=i, name=HORUS_NAME, short_name=HORUS_SHORT)
        db.session.add_all([bigcorp, horus, sys4])

        i = 2000
        d1 = Domain(id=i, name=EXAMPLE_COM, provider=bigcorp)
        i += 1
        d2 = Domain(id=i, name=EXAMPLE_NET, provider=bigcorp)
        i += 1
        d3 = Domain(id=i, name=EXAMPLE_ORG, provider=bigcorp)
        i += 1
        d1_horus = Domain(id=i, name='horus-it.de', provider=horus)
        i += 1
        d2_horus = Domain(id=i, name='horus-it.com', provider=horus)
        i += 1
        d1_sys4 = Domain(id=i, name='sys4.de', provider=sys4)
        i += 1
        orphan_domain = Domain(id=i, name=ORPHAN_DOMAIN, provider_id=(-1 * i))
        i += 1
        serverless_domain = Domain(id=i, name=SERVERLESS_DOMAIN, provider=bigcorp)
        horus_domains = [d1_horus, d2_horus]
        sys4_domains = [d1_sys4]
        db.session.add_all([d1, d2, d3])
        db.session.add_all(horus_domains)
        db.session.add_all(sys4_domains)
        db.session.add_all([orphan_domain, serverless_domain])

        i = 3000
        s1 = Server(id=i, type='smtp', port=587, name=self.smtp1_name, domains=[d1, d2])
        i += 1
        s2 = Server(id=i, type='smtp', port=587, name=self.smtp2_name, domains=[d3])
        i += 1
        s3 = Server(id=i, type='imap', port=143, name=self.imap1_name, domains=[d1])
        i += 1
        s4 = Server(id=i, type='imap', port=143, name=self.imap2_name, domains=[d2, d3])
        i += 1
        s5 = Server(id=i, type='imap', port=993, socket_type='SSL', name=HORUS_IMAP, domains=horus_domains)
        i += 1
        s6 = Server(id=i, type='smtp', port=587, name=HORUS_SMTP, domains=horus_domains)
        i += 1
        s7 = Server(id=i, type='imap', port=143, name=SYS4_MAILSERVER, domains=sys4_domains)
        i += 1
        s8 = Server(id=i, type='smtp', port=587, name=SYS4_MAILSERVER, domains=sys4_domains)
        db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8])


if __name__ == '__main__':
    unittest.main()
