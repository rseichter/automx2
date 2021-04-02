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
from flask_sqlalchemy import SQLAlchemy

from automx2 import PLACEHOLDER_ADDRESS
from automx2.util import from_environ
from automx2.util import unique

BIGCORP_NAME = 'Big Corporation, Inc.'
BIGCORP_SHORT = 'BigCorp'
EGGS_DOMAIN = 'ham-n-eggs.tld'
EGGS_NAME = 'Ham & Eggs'
EGGS_SHORT = 'H+E'
EXAMPLE_COM = 'example.com'
EXAMPLE_NET = 'example.net'
EXAMPLE_ORG = 'example.org'
ORPHAN_DOMAIN = 'orphan.tld'
OTHER_NAME = 'Some Other Provider'
OTHER_SHORT = 'SOP'
SERVERLESS_DOMAIN = 'serverless.tld'

LDAP_BIND_PASSWORD = from_environ('LDAP_BIND_PASSWORD')
LDAP_BIND_USER = from_environ('LDAP_BIND_USER')
LDAP_HOSTNAME = from_environ('LDAP_HOSTNAME')
LDAP_PORT = from_environ('LDAP_PORT', 636)
LDAP_SEARCH_BASE = from_environ('LDAP_SEARCH_BASE', 'dc=example,dc=com')

sample_server_names = {
    'cal': f'https://caldav.{unique()}.com',
    'card': f'http://carddav.{unique()}.com',
    'imap1': f'imap1.{unique()}.com',
    'imap2': f'imap2.{unique()}.com',
    'pop1': f'pop1.{unique()}.com',
    'smtp1': f'primary-smtp.{unique()}.com',
    'smtp2': f'secondary-smtp.{unique()}.com',
}

db = SQLAlchemy()

davserver_domain_map = db.Table(
    'davserver_domain',
    db.Column('davserver_id', db.Integer, db.ForeignKey('davserver.id'), primary_key=True),
    db.Column('domain_id', db.Integer, db.ForeignKey('domain.id'), primary_key=True)
)
server_domain_map = db.Table(
    'server_domain',
    db.Column('server_id', db.Integer, db.ForeignKey('server.id'), primary_key=True),
    db.Column('domain_id', db.Integer, db.ForeignKey('domain.id'), primary_key=True)
)


class Provider(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    short_name = db.Column(db.String, nullable=False)
    domains = db.relationship('Domain', lazy='select', backref=db.backref('provider', lazy='joined'))

    def __repr__(self) -> str:
        return f'<Provider id={self.id} name={self.short_name}>'


class Server(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    prio = db.Column(db.Integer, nullable=False, server_default='10')
    name = db.Column(db.String, nullable=False)
    port = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String, nullable=False)
    socket_type = db.Column(db.String, nullable=False, default='STARTTLS')
    user_name = db.Column(db.String, nullable=False, default=PLACEHOLDER_ADDRESS)
    authentication = db.Column(db.String, nullable=False, default='plain')
    domains = db.relationship('Domain', secondary=server_domain_map, lazy='subquery',
                              backref=db.backref('servers', lazy='select'))

    def __repr__(self) -> str:
        return f'<Server id={self.id} type={self.type} name={self.name}>'


class Davserver(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    url = db.Column(db.String, nullable=False)
    port = db.Column(db.Integer, nullable=False, default=0)
    type = db.Column(db.String, nullable=False)
    use_ssl = db.Column(db.Boolean, nullable=False)
    domain_required = db.Column(db.Boolean, nullable=False)
    user_name = db.Column(db.String, nullable=True)
    domains = db.relationship('Domain', secondary=davserver_domain_map, lazy='subquery',
                              backref=db.backref('davservers', lazy='select'))

    def __repr__(self) -> str:
        return f'<Davserver id={self.id} type={self.type} url={self.url}>'


class Ldapserver(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    port = db.Column(db.Integer, nullable=False)
    use_ssl = db.Column(db.Boolean, nullable=False)
    search_base = db.Column(db.String, nullable=False)
    search_filter = db.Column(db.String, nullable=False)
    attr_uid = db.Column(db.String, nullable=False)
    attr_cn = db.Column(db.String, nullable=True)
    bind_password = db.Column(db.String, nullable=True)
    bind_user = db.Column(db.String, nullable=True)
    domains = db.relationship('Domain', lazy='select', backref=db.backref('ldapserver', lazy='joined'))

    def __repr__(self) -> str:
        return f'<Ldapserver id={self.id} name={self.name}>'


class Domain(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    ldapserver_id = db.Column(db.Integer, db.ForeignKey('ldapserver.id'), nullable=True)

    def __repr__(self) -> str:
        return f'<Domain id={self.id} name={self.name}>'


# noinspection DuplicatedCode
def populate_db():
    """Populate the database with some fixed samples."""
    i = 1000
    bigcorp = Provider(id=i, name=BIGCORP_NAME, short_name=BIGCORP_SHORT)
    i += 1
    eggs = Provider(id=i, name=EGGS_NAME, short_name=EGGS_SHORT)
    i += 1
    other = Provider(id=i, name=OTHER_NAME, short_name=OTHER_SHORT)
    db.session.add_all([bigcorp, eggs, other])

    if LDAP_HOSTNAME:
        ls = Ldapserver(id=2000, name=LDAP_HOSTNAME, port=LDAP_PORT, use_ssl=True, attr_uid='uid', attr_cn='cn',
                        bind_password=LDAP_BIND_PASSWORD, bind_user=LDAP_BIND_USER, search_base=LDAP_SEARCH_BASE,
                        search_filter='(mail={0})')
        db.session.add_all([ls])
    else:  # pragma: no cover
        ls = None

    i = 3000
    ex_com = Domain(id=i, name=EXAMPLE_COM, provider=bigcorp, ldapserver=ls)
    i += 1
    ex_net = Domain(id=i, name=EXAMPLE_NET, provider=bigcorp)
    i += 1
    ex_org = Domain(id=i, name=EXAMPLE_ORG, provider=bigcorp)
    i += 1
    eggs = Domain(id=i, name=EGGS_DOMAIN, provider=eggs)
    i += 1
    orphan = Domain(id=i, name=ORPHAN_DOMAIN, provider_id=(-1 * i))
    i += 1
    serverless = Domain(id=i, name=SERVERLESS_DOMAIN, provider=other)
    db.session.add_all([ex_com, ex_net, ex_org, eggs, orphan, serverless])

    i = 4000
    s1 = Server(id=i, type='smtp', port=587, name=sample_server_names['smtp1'], domains=[ex_com, ex_net])
    i += 1
    s2 = Server(id=i, type='smtp', port=587, name=sample_server_names['smtp2'], domains=[ex_org])
    i += 1
    s3 = Server(id=i, type='imap', port=143, name=sample_server_names['imap1'], domains=[ex_com])
    i += 1
    s4 = Server(id=i, type='imap', port=143, name=sample_server_names['imap2'], domains=[ex_net])
    i += 1
    s5 = Server(id=i, type='pop', port=143, name=sample_server_names['pop1'], domains=[ex_org])
    i += 1
    s6 = Server(id=i, type='INVALID', port=123, name=f'{unique()}.{EGGS_DOMAIN}', domains=[eggs])
    db.session.add_all([s1, s2, s3, s4, s5, s6])

    i = 4100
    d1 = Davserver(id=i, type='caldav', url=sample_server_names['cal'], port=443, use_ssl=True,
                   domain_required=False, user_name=PLACEHOLDER_ADDRESS, domains=[ex_com])
    i += 1
    d2 = Davserver(id=i, type='carddav', url=sample_server_names['card'], use_ssl=False,
                   domain_required=True, domains=[ex_com, ex_net])
    db.session.add_all([d1, d2])
