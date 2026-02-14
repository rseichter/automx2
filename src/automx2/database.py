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
from automx2.util import truthy
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
    bigcorp = Provider(name=BIGCORP_NAME, short_name=BIGCORP_SHORT)
    eggs = Provider(name=EGGS_NAME, short_name=EGGS_SHORT)
    other = Provider(name=OTHER_NAME, short_name=OTHER_SHORT)
    db.session.add_all([bigcorp, eggs, other])

    if LDAP_HOSTNAME:
        ls = Ldapserver(
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

    ex_com = Domain(name=EXAMPLE_COM, provider=bigcorp, ldapserver=ls)
    ex_net = Domain(name=EXAMPLE_NET, provider=bigcorp)
    ex_org = Domain(name=EXAMPLE_ORG, provider=bigcorp)
    eggs = Domain(name=EGGS_DOMAIN, provider=eggs)
    serverless = Domain(name=SERVERLESS_DOMAIN, provider=other)
    db.session.add_all([ex_com, ex_net, ex_org, eggs, serverless])

    s1 = Server(
        type="smtp",
        port=587,
        name=sample_server_names["smtp1"],
        domains=[ex_com, ex_net],
    )
    s2 = Server(type="smtp", port=587, name=sample_server_names["smtp2"], domains=[ex_org])
    s3 = Server(type="imap", port=143, name=sample_server_names["imap1"], domains=[ex_com])
    s4 = Server(type="imap", port=143, name=sample_server_names["imap2"], domains=[ex_net])
    s5 = Server(type="pop", port=143, name=sample_server_names["pop1"], domains=[ex_org])
    s6 = Server(type="INVALID", port=123, name=f"{unique()}.{EGGS_DOMAIN}", domains=[eggs])
    db.session.add_all([s1, s2, s3, s4, s5, s6])

    d1 = Davserver(
        type="caldav",
        url=sample_server_names["cal"],
        port=443,
        use_ssl=True,
        domain_required=False,
        user_name=PLACEHOLDER_ADDRESS,
        domains=[ex_com],
    )
    d2 = Davserver(
        type="carddav",
        url=sample_server_names["card"],
        use_ssl=False,
        domain_required=True,
        domains=[ex_com, ex_net],
    )
    db.session.add_all([d1, d2])


def dictget_ldapservers(config: dict):
    servers = []
    if "ldapservers" in config:
        for ss in config["ldapservers"]:
            name = dictget_mandatory(ss, "name")
            port = dictget_optional(ss, "port", LDAP_PORT)
            attr_uid = dictget_optional(ss, "attr_uid", "uid")
            attr_cn = dictget_optional(ss, "attr_cn", "cn")
            bind_password = dictget_mandatory(ss, "bind_password")
            bind_user = dictget_mandatory(ss, "bind_user")
            search_base = dictget_mandatory(ss, "search_base")
            search_filter = dictget_optional(ss, "search_filter", "(mail={0})")
            use_ssl = truthy(dictget_optional(ss, "use_ssl", port == 636))
            ls = Ldapserver(
                name=name,
                port=port,
                use_ssl=use_ssl,
                attr_uid=attr_uid,
                attr_cn=attr_cn,
                bind_password=bind_password,
                bind_user=bind_user,
                search_base=search_base,
                search_filter=search_filter,
            )
            servers.append(ls)
    return servers


def populate_with_dict(config: dict) -> None:
    name: str = dictget_mandatory(config, "provider")
    short_name = name.split(" ")[0]
    provider = Provider(name=name, short_name=short_name)
    db.session.add(provider)
    ldapservers = dictget_ldapservers(config)
    n = len(ldapservers)
    if n > 0:
        log.info(f"Adding {n} LDAP servers")
        db.session.add_all(ldapservers)
    domains = []
    for domain in dictget_mandatory(config, "domains"):
        use_ldap = truthy(dictget_optional(domain, "use_ldap"))
        if use_ldap and len(ldapservers) > 0:
            dom = Domain(name=domain, provider=provider, ldapserver=ldapservers[0])
        elif use_ldap:
            log.error("No LDAP server defined")
            return
        else:
            dom = Domain(name=domain, provider=provider)
        domains.append(dom)
    if len(domains) < 1:  # pragma: no cover
        log.error("No domains specified")
        return
    db.session.add_all(domains)
    servers = []
    davservers = []
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
                    type=type_,
                    url=url,
                    port=port,
                    use_ssl=ssl,
                    domain_required=True,
                    user_name=PLACEHOLDER_ADDRESS,
                    domains=domains,
                )
            )
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
                prio=prio,
                type=type_,
                port=port,
                socket_type=s,
                name=name,
                domains=domains,
            )
        )
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
