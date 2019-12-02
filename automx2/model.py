"""
Model classes, based on Flask-SQLAlchemy.
"""
from flask_sqlalchemy import SQLAlchemy

from automx2 import log
from automx2.config import config

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


def populate_db(session):  # pragma: no cover
    """Populate the database with example data."""
    _populate_from_config(session)
    _populate_from_samples(session)


def _populate_from_config(session):  # pragma: no cover
    """Populate based on config file sections (seed.xyz)."""
    servers = {}
    for seed in config.seed_servers():
        server = Server.from_seed(seed)
        session.add(server)
        servers[server.id] = server
    for seed in config.seed_providers():
        provider = Provider.from_seed(seed)
        session.add(provider)
    for seed in config.seed_domains():
        domain = Domain.from_seed(seed, servers)
        session.add(domain)


def _populate_from_samples(session):  # pragma: no cover
    """Populate with some fixed samples."""
    base = 1000
    p1 = Provider(id=base + 1, name='Example Provider #1', short_name='Provider1')
    p2 = Provider(id=base + 2, name='Example Provider #2', short_name='Provider2')
    horus = Provider(id=base + 3, name='HORUS-IT Ralph Seichter', short_name='HORUS-IT')
    sys4 = Provider(id=base + 4, name='sys4 AG', short_name='sys4')
    session.add_all([p1, p2, horus, sys4])

    base = 1100
    d1 = Domain(id=base + 1, name='example.com', provider=p2)
    d2 = Domain(id=base + 2, name='example.net', provider=p2)
    d3 = Domain(id=base + 3, name='example.org', provider=p1)
    d4 = Domain(id=base + 4, name='4titu.de', provider=horus)
    d5 = Domain(id=base + 5, name='horus-it.de', provider=horus)
    d6 = Domain(id=base + 6, name='horus-it.com', provider=horus)
    d7 = Domain(id=base + 7, name='sys4.de', provider=sys4)
    session.add_all([d1, d2, d3, d4, d5, d6, d7])
    horus_domains = [d4, d5, d6]
    sys4_domains = [d7]

    base = 1200
    s1 = Server(id=base + 1, type='smtp', port=587, name='smtp1.provider.com', domains=[d1, d2])
    s2 = Server(id=base + 2, type='smtp', port=587, name='smtp2.provider.com', domains=[d3])
    s3 = Server(id=base + 3, type='imap', port=143, name='imap-a.provider.com', domains=[d2, d3])
    s4 = Server(id=base + 4, type='imap', port=143, name='imap-b.provider.com', domains=[d1])
    s5 = Server(id=base + 5, type='imap', port=993, socket_type='SSL', name='imap.horus-it.com',
                domains=horus_domains)
    s6 = Server(id=base + 6, type='smtp', port=587, name='smtp.horus-it.com', domains=horus_domains)
    s7 = Server(id=base + 7, type='imap', port=143, name='mail.sys4.de', domains=sys4_domains)
    s8 = Server(id=base + 8, type='smtp', port=587, name='mail.sys4.de', domains=sys4_domains)
    session.add_all([s1, s2, s3, s4, s5, s6, s7, s8])
