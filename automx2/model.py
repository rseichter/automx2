"""
Model classes, based on Flask-SQLAlchemy.
"""
from flask_sqlalchemy import SQLAlchemy

from automx2 import log
from automx2.config import config
from automx2.util import unique

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

    @classmethod
    def from_seed(cls, seed: dict):
        provider = cls(id=seed['id'], name=seed['name'], short_name=seed['short_name'])
        return provider


class Server(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    port = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    socket_type = db.Column(db.String, nullable=False, default='STARTTLS')
    user_name = db.Column(db.String, nullable=False, default='%EMAILADDRESS%')
    authentication = db.Column(db.String, nullable=False, default='plain')
    domains = db.relationship('Domain', secondary=server_domain_map, lazy='subquery',
                              backref=db.backref('servers', lazy='select'))

    def __repr__(self) -> str:
        return f'<Server id={self.id} type={self.type} name={self.name}>'

    @classmethod
    def from_seed(cls, seed: dict):
        provider = cls(id=seed['id'], name=seed['name'], port=seed['port'], type=seed['type'])
        return provider


class Domain(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f'<Domain id={self.id} name={self.name}>'

    @classmethod
    def from_seed(cls, seed: dict, servers_dict: dict):
        domain = cls(id=seed['id'], provider_id=seed['provider'], name=seed['name'])
        if 'servers' in seed:
            servers = []
            for key in seed['servers'].split():
                if key in servers_dict:
                    servers.append(servers_dict[key])
                else:
                    log.error(f"Unknown server '{key}' in config section {seed['section_name']}")
            if servers:
                domain.servers = servers
        return domain


def populate_db():
    """Populate the database with example data."""
    _populate_from_config()
    _populate_from_samples()


def _populate_from_config():  # pragma: no cover
    """Populate based on config file sections (seed.xyz)."""
    servers = {}
    for seed in config.seed_servers():
        server = Server.from_seed(seed)
        db.session.add(server)
        servers[server.id] = server
    for seed in config.seed_providers():
        provider = Provider.from_seed(seed)
        db.session.add(provider)
    for seed in config.seed_domains():
        domain = Domain.from_seed(seed, servers)
        db.session.add(domain)


def _populate_from_samples():
    """Populate with some fixed samples."""
    i = 1000
    bigcorp = Provider(id=i, name=BIGCORP_NAME, short_name=BIGCORP_SHORT)
    i += 1
    horus = Provider(id=i, name=HORUS_NAME, short_name=HORUS_SHORT)
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
    s1 = Server(id=i, type='smtp', port=587, name=sample_server_names['smtp1'], domains=[d1, d2])
    i += 1
    s2 = Server(id=i, type='smtp', port=587, name=sample_server_names['smtp2'], domains=[d3])
    i += 1
    s3 = Server(id=i, type='imap', port=143, name=sample_server_names['imap1'], domains=[d1])
    i += 1
    s4 = Server(id=i, type='imap', port=143, name=sample_server_names['imap2'], domains=[d2, d3])
    i += 1
    s5 = Server(id=i, type='imap', port=993, socket_type='SSL', name=HORUS_IMAP, domains=horus_domains)
    i += 1
    s6 = Server(id=i, type='smtp', port=587, name=HORUS_SMTP, domains=horus_domains)
    i += 1
    s7 = Server(id=i, type='imap', port=143, name=SYS4_MAILSERVER, domains=sys4_domains)
    i += 1
    s8 = Server(id=i, type='smtp', port=587, name=SYS4_MAILSERVER, domains=sys4_domains)
    db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8])
