"""
Copyright © 2019-2025 Ralph Seichter

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

import sys
from typing import Optional

from automx2 import PLACEHOLDER_ADDRESS
from automx2 import log
from automx2.model import Davserver
from automx2.model import Domain
from automx2.model import Ldapserver
from automx2.model import Provider
from automx2.model import Server
from automx2.model import db
from automx2.util import dictget_mandatory
from automx2.util import dictget_optional
from automx2.util import from_environ
from automx2.util import unique

LDAP_BIND_PASSWORD = from_environ("LDAP_BIND_PASSWORD")
LDAP_BIND_USER = from_environ("LDAP_BIND_USER")
LDAP_HOSTNAME = from_environ("LDAP_HOSTNAME")
LDAP_PORT = from_environ("LDAP_PORT", 636)
LDAP_SEARCH_BASE = from_environ("LDAP_SEARCH_BASE", "dc=example,dc=com")

BIGCORP_NAME = "Big Corporation, Inc."
BIGCORP_SHORT = "BigCorp"
EGGS_DOMAIN = "ham-n-eggs.tld"
EGGS_NAME = "Ham & Eggs"
EGGS_SHORT = "H+E"
EXAMPLE_COM = "example.com"
EXAMPLE_NET = "example.net"
EXAMPLE_ORG = "example.org"
ORPHAN_DOMAIN = "orphan.tld"
OTHER_NAME = "Some Other Provider"
OTHER_SHORT = "SOP"
SERVERLESS_DOMAIN = "serverless.tld"

sample_server_names = {
    "cal": f"https://caldav.{unique()}.com",
    "card": f"http://carddav.{unique()}.com",
    "imap1": f"imap1.{unique()}.com",
    "imap2": f"imap2.{unique()}.com",
    "pop1": f"pop1.{unique()}.com",
    "smtp1": f"primary-smtp.{unique()}.com",
    "smtp2": f"secondary-smtp.{unique()}.com",
}


def populate_with_example_data():
    """Populate the database with some fixed samples."""
    i = 1000
    bigcorp = Provider(id=i, name=BIGCORP_NAME, short_name=BIGCORP_SHORT)
    i += 1
    eggs = Provider(id=i, name=EGGS_NAME, short_name=EGGS_SHORT)
    i += 1
    other = Provider(id=i, name=OTHER_NAME, short_name=OTHER_SHORT)
    db.session.add_all([bigcorp, eggs, other])

    if LDAP_HOSTNAME:
        ls = Ldapserver(
            id=2000,
            name=LDAP_HOSTNAME,
            port=LDAP_PORT,
            use_ssl=True,
            attr_uid="uid",
            attr_cn="cn",
            bind_password=LDAP_BIND_PASSWORD,
            bind_user=LDAP_BIND_USER,
            search_base=LDAP_SEARCH_BASE,
            search_filter="(mail={0})",
        )
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
    # orphan = Domain(id=i, name=ORPHAN_DOMAIN, provider_id=(-1 * i))
    # i += 1
    serverless = Domain(id=i, name=SERVERLESS_DOMAIN, provider=other)
    # db.session.add_all([ex_com, ex_net, ex_org, eggs, orphan, serverless])
    db.session.add_all([ex_com, ex_net, ex_org, eggs, serverless])

    i = 4000
    s1 = Server(
        id=i,
        type="smtp",
        port=587,
        name=sample_server_names["smtp1"],
        domains=[ex_com, ex_net],
    )
    i += 1
    s2 = Server(
        id=i, type="smtp", port=587, name=sample_server_names["smtp2"], domains=[ex_org]
    )
    i += 1
    s3 = Server(
        id=i, type="imap", port=143, name=sample_server_names["imap1"], domains=[ex_com]
    )
    i += 1
    s4 = Server(
        id=i, type="imap", port=143, name=sample_server_names["imap2"], domains=[ex_net]
    )
    i += 1
    s5 = Server(
        id=i, type="pop", port=143, name=sample_server_names["pop1"], domains=[ex_org]
    )
    i += 1
    s6 = Server(
        id=i, type="INVALID", port=123, name=f"{unique()}.{EGGS_DOMAIN}", domains=[eggs]
    )
    db.session.add_all([s1, s2, s3, s4, s5, s6])

    i = 4100
    d1 = Davserver(
        id=i,
        type="caldav",
        url=sample_server_names["cal"],
        port=443,
        use_ssl=True,
        domain_required=False,
        user_name=PLACEHOLDER_ADDRESS,
        domains=[ex_com],
    )
    i += 1
    d2 = Davserver(
        id=i,
        type="carddav",
        url=sample_server_names["card"],
        use_ssl=False,
        domain_required=True,
        domains=[ex_com, ex_net],
    )
    db.session.add_all([d1, d2])


def populate_with_dict(config: dict) -> None:
    name: str = dictget_mandatory(config, "provider")
    short_name = name.split(" ")[0]
    provider = Provider(id=Provider.query.count(), name=name, short_name=short_name)
    db.session.add(provider)
    domains = []
    did = Domain.query.count()
    for domain in dictget_mandatory(config, "domains"):
        domains.append(Domain(id=did, name=domain, provider=provider))
        did += 1
    if len(domains) < 1:  # pragma: no cover
        log.error("No domains specified")
        return
    db.session.add_all(domains)
    servers = []
    sid = Server.query.count()
    davservers = []
    did = Davserver.query.count()
    for server in dictget_mandatory(config, "servers"):
        type_ = dictget_mandatory(server, "type")
        if type_ == "caldav" or type_ == "carddav":
            url = dictget_mandatory(server, "url")
            if url[:6] == "https:":
                ssl = 1
            else:
                ssl = 0
            port = dictget_optional(server, "port", 0)
            davservers.append(
                Davserver(
                    id=did,
                    type=type_,
                    url=url,
                    port=port,
                    use_ssl=ssl,
                    domain_required=True,
                    user_name=PLACEHOLDER_ADDRESS,
                    domains=domains,
                )
            )
            did += 1
            continue
        elif type_ == "imap":
            port = dictget_optional(server, "port", 993)
        elif type_ == "pop":
            port = dictget_optional(server, "port", 995)
        elif type_ == "smtp":
            port = dictget_optional(server, "port", 465)
        else:
            log.error(f"Unknown server type {type_}")
            sys.exit(1)
        prio = dictget_optional(server, "prio", 10)
        if port in [465, 993, 995]:
            s = "SSL"
        else:
            s = "STARTTLS"
        name = dictget_mandatory(server, "name")
        servers.append(
            Server(
                id=sid,
                prio=prio,
                type=type_,
                port=port,
                socket_type=s,
                name=name,
                domains=domains,
            )
        )
        sid += 1
    sl = len(servers)
    if sl < 1:
        log.error("No mail servers specified")
    else:
        log.info(f"Adding {sl} mail servers")
        db.session.add_all(servers)
    dl = len(davservers)
    if dl > 0:
        log.info(f"Adding {dl} DAV servers")
        db.session.add_all(davservers)


def populate_db(data_source: Optional[dict]):
    if data_source:
        populate_with_dict(data_source)
    else:
        populate_with_example_data()


def purge_db():
    c = db.engine.connect()
    t = c.begin()
    for table in reversed(db.metadata.sorted_tables):
        x = table.delete()
        c.execute(x)
    t.commit()
    c.close()
