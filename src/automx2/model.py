"""
Copyright © 2019-2026 Ralph Seichter

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

import sqlalchemy as sq
from flask_sqlalchemy_lite import SQLAlchemy
from sqlalchemy import orm

from automx2 import PLACEHOLDER_ADDRESS

db = SQLAlchemy()


class Base(orm.DeclarativeBase):
    pass


davserver_domain_map = sq.Table(
    "davserver_domain",
    Base.metadata,
    sq.Column(
        "davserver_id", sq.Integer, sq.ForeignKey("davserver.id"), primary_key=True
    ),
    sq.Column("domain_id", sq.Integer, sq.ForeignKey("domain.id"), primary_key=True),
)

server_domain_map = sq.Table(
    "server_domain",
    Base.metadata,
    sq.Column("server_id", sq.Integer, sq.ForeignKey("server.id"), primary_key=True),
    sq.Column("domain_id", sq.Integer, sq.ForeignKey("domain.id"), primary_key=True),
)


class Provider(Base):
    __tablename__ = "provider"
    id = sq.Column(sq.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = sq.Column(sq.String(128), nullable=False)
    short_name = sq.Column(sq.String(32), nullable=False)
    domains = orm.relationship("Domain", lazy="select", back_populates="provider")

    def __repr__(self) -> str:
        return f"<Provider id={self.id} name={self.short_name}>"


class Server(Base):
    __tablename__ = "server"
    id = sq.Column(sq.Integer, nullable=False, primary_key=True, autoincrement=True)
    prio = sq.Column(sq.Integer, nullable=False, server_default="10")
    name = sq.Column(sq.String(128), nullable=False)
    port = sq.Column(sq.Integer, nullable=False)
    type = sq.Column(sq.String(32), nullable=False)
    socket_type = sq.Column(sq.String(32), nullable=False, default="STARTTLS")
    user_name = sq.Column(sq.String(64), nullable=False, default=PLACEHOLDER_ADDRESS)
    authentication = sq.Column(sq.String(32), nullable=False, default="plain")
    domains = orm.relationship(
        "Domain", secondary=server_domain_map, lazy="subquery", back_populates="servers"
    )

    def __repr__(self) -> str:
        return (
            f"<Server id={self.id} prio={self.prio} type={self.type} name={self.name}>"
        )


class Davserver(Base):
    __tablename__ = "davserver"
    id = sq.Column(sq.Integer, nullable=False, primary_key=True, autoincrement=True)
    url = sq.Column(sq.String(128), nullable=False)
    port = sq.Column(sq.Integer, nullable=False, default=0)
    type = sq.Column(sq.String(32), nullable=False)
    use_ssl = sq.Column(sq.Boolean, nullable=False)
    domain_required = sq.Column(sq.Boolean, nullable=False)
    user_name = sq.Column(sq.String(64), nullable=True)
    domains = orm.relationship(
        "Domain",
        secondary=davserver_domain_map,
        lazy="subquery",
        back_populates="davservers",
    )

    def __repr__(self) -> str:
        return f"<Davserver id={self.id} type={self.type} url={self.url}>"


class Ldapserver(Base):
    __tablename__ = "ldapserver"
    id = sq.Column(sq.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = sq.Column(sq.String(128), nullable=False)
    port = sq.Column(sq.Integer, nullable=False)
    use_ssl = sq.Column(sq.Boolean, nullable=False)
    search_base = sq.Column(sq.String(128), nullable=False)
    search_filter = sq.Column(sq.String(128), nullable=False)
    attr_uid = sq.Column(sq.String(32), nullable=False)
    attr_cn = sq.Column(sq.String(32), nullable=True)
    bind_password = sq.Column(sq.String(128), nullable=True)
    bind_user = sq.Column(sq.String(128), nullable=True)
    domains = orm.relationship("Domain", lazy="select", back_populates="ldapserver")

    def __repr__(self) -> str:
        return f"<Ldapserver id={self.id} name={self.name}>"


class Domain(Base):
    __tablename__ = "domain"
    id = sq.Column(sq.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = sq.Column(sq.String(128), nullable=False, unique=True)
    provider_id = sq.Column(sq.Integer, sq.ForeignKey("provider.id"), nullable=False)
    ldapserver_id = sq.Column(sq.Integer, sq.ForeignKey("ldapserver.id"), nullable=True)
    provider = orm.relationship("Provider", lazy="select", back_populates="domains")
    ldapserver = orm.relationship("Ldapserver", lazy="select", back_populates="domains")
    servers = orm.relationship(
        "Server", secondary=server_domain_map, lazy="select", back_populates="domains"
    )
    davservers = orm.relationship(
        "Davserver",
        secondary=davserver_domain_map,
        lazy="select",
        back_populates="domains",
    )

    def __repr__(self) -> str:
        return f"<Domain id={self.id} name={self.name}>"
