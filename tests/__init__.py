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

import unittest

from flask import Response

from automx2.generators.outlook import NS_REQUEST
from automx2.generators.outlook import NS_RESPONSE_PAYLOAD
from automx2.database import LDAP_BIND_PASSWORD
from automx2.database import LDAP_BIND_USER
from automx2.database import LDAP_HOSTNAME
from automx2.database import LDAP_PORT
from automx2.database import LDAP_SEARCH_BASE
from automx2.database import populate_db
from automx2.model import Ldapserver
from automx2.model import db
from automx2.server import APPLE_CONFIG_ROUTE
from automx2.server import MOZILLA_CONFIG_ROUTE
from automx2.server import MSOFT_CONFIG_ROUTE
from automx2.server import app
from automx2.util import from_environ
from automx2.views import CONTENT_TYPE_XML
from automx2.views import EMAIL_MOZILLA
from automx2.views import EMAIL_OUTLOOK

RUN_LDAP_TESTS = from_environ("RUN_LDAP_TESTS") == "1"
NETWORK_TESTS = from_environ("NETWORK_TESTS") == "1"


def body(response: Response) -> str:
    return str(response.data, encoding="utf-8", errors="strict")


class TestCase(unittest.TestCase):
    """Test case base class."""

    create_db = True

    def setUp(self) -> None:
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            if self.create_db:
                db.create_all()
                populate_db(None)
                if RUN_LDAP_TESTS:
                    ls = Ldapserver(
                        id=LDAP_PORT,
                        name=LDAP_HOSTNAME,
                        port=LDAP_PORT,
                        use_ssl=True,
                        attr_uid="uid",
                        attr_cn="cn",
                        bind_user=LDAP_BIND_USER,
                        bind_password=LDAP_BIND_PASSWORD,
                        search_base=LDAP_SEARCH_BASE,
                        search_filter="(mail={0})",
                    )
                    db.session.add(ls)
                db.session.commit()

    def tearDown(self) -> None:
        with app.app_context():
            db.drop_all()
            db.session.commit()

    def get(self, *args, **kwargs) -> Response:
        kwargs["follow_redirects"] = True
        return self.app.get(*args, **kwargs)

    def post(self, *args, **kwargs) -> Response:
        kwargs["follow_redirects"] = True
        return self.app.post(*args, **kwargs)

    def get_apple_config(self, address: str) -> Response:
        return self.get(f"{APPLE_CONFIG_ROUTE}?{EMAIL_MOZILLA}={address}")

    def get_mozilla_config(self, address: str) -> Response:
        return self.get(f"{MOZILLA_CONFIG_ROUTE}?{EMAIL_MOZILLA}={address}")

    def get_msoft_config(
        self, address: str, route: str = MSOFT_CONFIG_ROUTE
    ) -> Response:
        data = (
            f'<Autodiscover xmlns="{NS_REQUEST}">'
            f"<AcceptableResponseSchema>{NS_RESPONSE_PAYLOAD}</AcceptableResponseSchema>"
            "<Request>"
            f"<{EMAIL_OUTLOOK}>{address}</{EMAIL_OUTLOOK}>"
            "</Request>"
            "</Autodiscover>"
        )
        return self.post(route, data=data, content_type=CONTENT_TYPE_XML)


if __name__ == "__main__":
    unittest.main()
