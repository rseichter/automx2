"""
Copyright © 2019 Ralph Seichter

Graciously sponsored by sys4 AG <https://sys4.de/>

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
from flask_sqlalchemy import SQLAlchemy

from automx2 import PLACEHOLDER_ADDRESS
from automx2 import PLACEHOLDER_LOCALPART
from automx2.util import unique

AUTOMX_DOMAIN = 'automx.org'
EGGS_NAME = 'Ham & Eggs'
EGGS_SHORT = 'H+E'
EGGS_DOMAIN = 'ham-n-eggs.tld'
BIGCORP_NAME = 'Big Corporation, Inc.'
BIGCORP_SHORT = 'BigCorp'
EXAMPLE_COM = 'example.com'
EXAMPLE_NET = 'example.net'
EXAMPLE_ORG = 'example.org'
HORUS_IMAP = 'imap.horus-it.com'
HORUS_NAME = 'HORUS-IT Ralph Seichter'
HORUS_SHORT = 'HORUS-IT'
HORUS_SMTP = 'smtp.horus-it.com'
ORPHAN_DOMAIN = 'orphan.tld'
OTHER_NAME = 'Some Other Provider'
OTHER_SHORT = 'SOP'
SERVERLESS_DOMAIN = 'serverless.tld'
SYS4_MAILSERVER = 'mail.sys4.de'
SYS4_NAME = 'sys4 AG'
SYS4_SHORT = 'sys4'

sample_server_names = {
    'imap1': f'imap1.{unique()}.com',
    'imap2': f'imap2.{unique()}.com',
    'smtp1': f'primary-smtp.{unique()}.com',
    'smtp2': f'secondary-smtp.{unique()}.com',
}

db = SQLAlchemy()

server_domain_map = db.Table('server_domain',
                             db.Column('server_id', db.Integer, db.ForeignKey('server.id'), primary_key=True),
                             db.Column('domain_id', db.Integer, db.ForeignKey('domain.id'), primary_key=True))


class Provider(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    short_name = db.Column(db.String, nullable=False)
    domains = db.relationship('Domain', lazy='select', backref=db.backref('provider', lazy='joined'))

    def __repr__(self) -> str:
        return f'<Provider id={self.id} name={self.short_name}>'


class Server(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    port = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    socket_type = db.Column(db.String, nullable=False, default='STARTTLS')
    user_name = db.Column(db.String, nullable=False, default=PLACEHOLDER_ADDRESS)
    authentication = db.Column(db.String, nullable=False, default='plain')
    domains = db.relationship('Domain', secondary=server_domain_map, lazy='subquery',
                              backref=db.backref('servers', lazy='select'))

    def __repr__(self) -> str:
        return f'<Server id={self.id} type={self.type} name={self.name}>'


class Domain(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f'<Domain id={self.id} name={self.name}>'


# noinspection DuplicatedCode
def populate_db():
    """Populate the database some fixed samples."""
    i = 1000
    bigcorp = Provider(id=i, name=BIGCORP_NAME, short_name=BIGCORP_SHORT)
    i += 1
    eggs = Provider(id=i, name=EGGS_NAME, short_name=EGGS_SHORT)
    i += 1
    horus = Provider(id=i, name=HORUS_NAME, short_name=HORUS_SHORT)
    i += 1
    other = Provider(id=i, name=OTHER_NAME, short_name=OTHER_SHORT)
    i += 1
    sys4 = Provider(id=i, name=SYS4_NAME, short_name=SYS4_SHORT)
    db.session.add_all([bigcorp, horus, sys4])

    i = 2000
    d1 = Domain(id=i, name=EXAMPLE_COM, provider=bigcorp)
    i += 1
    d2 = Domain(id=i, name=EXAMPLE_NET, provider=bigcorp)
    i += 1
    d3 = Domain(id=i, name=EXAMPLE_ORG, provider=bigcorp)
    i += 1
    d_automx = Domain(id=i, name=AUTOMX_DOMAIN, provider=sys4)
    i += 1
    d1_horus = Domain(id=i, name='horus-it.de', provider=horus)
    i += 1
    d2_horus = Domain(id=i, name='horus-it.com', provider=horus)
    i += 1
    d1_sys4 = Domain(id=i, name='sys4.de', provider=sys4)
    i += 1
    eggs_domain = Domain(id=i, name=EGGS_DOMAIN, provider=eggs)
    i += 1
    providerless_domain = Domain(id=i, name=ORPHAN_DOMAIN, provider_id=(-1 * i))
    i += 1
    serverless_domain = Domain(id=i, name=SERVERLESS_DOMAIN, provider=other)
    horus_domains = [d1_horus, d2_horus]
    sys4_domains = [d1_sys4]
    db.session.add_all([d1, d2, d3, d_automx])
    db.session.add_all(horus_domains)
    db.session.add_all(sys4_domains)
    db.session.add_all([eggs_domain, providerless_domain, serverless_domain])

    i = 3000
    s1 = Server(id=i, type='smtp', port=587, name=sample_server_names['smtp1'], domains=[d1, d2])
    i += 1
    s2 = Server(id=i, type='smtp', port=587, name=sample_server_names['smtp2'], domains=[d3])
    i += 1
    s3 = Server(id=i, type='imap', port=143, name=sample_server_names['imap1'], domains=[d1])
    i += 1
    s4 = Server(id=i, type='imap', port=143, name=sample_server_names['imap2'], domains=[d2, d3])
    i += 1
    s5 = Server(id=i, type='imap', port=993, socket_type='SSL', name=HORUS_IMAP, user_name=PLACEHOLDER_LOCALPART,
                domains=horus_domains)
    i += 1
    s6 = Server(id=i, type='smtp', port=587, name=HORUS_SMTP, user_name=PLACEHOLDER_LOCALPART, domains=horus_domains)
    i += 1
    s7 = Server(id=i, type='imap', port=143, name=SYS4_MAILSERVER, domains=sys4_domains)
    i += 1
    s8 = Server(id=i, type='smtp', port=587, name=SYS4_MAILSERVER, domains=sys4_domains)
    i += 1
    s9 = Server(id=i, type='INVALID', port=123, name=f'{unique()}.{EGGS_DOMAIN}', domains=[eggs_domain])
    i += 1
    s10 = Server(id=i, type='imap', port=993, socket_type='SSL', name=f'imap.{AUTOMX_DOMAIN}', domains=[d_automx])
    i += 1
    s11 = Server(id=i, type='smtp', port=587, name=f'smtp.{AUTOMX_DOMAIN}', domains=[d_automx])
    db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11])
