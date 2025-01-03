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

import os
import errno
import socket
from flask import Flask
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix

from automx2.config import config
from automx2.model import db
from automx2.views import autoconfig
from automx2.views import autodiscover
from automx2.views import mobileconfig
from automx2.views.initdb import InitDatabase
from automx2.views.site import SiteRoot

APPLE_CONFIG_ROUTE = "/mobileconfig/"
INITDB_ROUTE = "/initdb/"
MOZILLA_CONFIG_ROUTE = "/mail/config-v1.1.xml"
MSOFT_ALTERNATE_ROUTE = "/AutoDiscover/AutoDiscover.xml"
MSOFT_CONFIG_ROUTE = "/autodiscover/autodiscover.xml"


def _proxy_fix():
    """Use a fix for Werkzeug if automx2 is running behind a proxy.
    This enables support for X-Forwarded-* headers.
    """
    p = int(config.proxy_count())
    if p > 0:  # pragma: no cover (Tests don't use a proxy)
        # See https://werkzeug.palletsprojects.com/en/0.15.x/middleware/proxy_fix/
        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=p, x_host=p, x_port=p, x_prefix=p, x_proto=p
        )


def _sd_notify(message: str) -> bool:
    """
    Send notification message to systemd. Based on the sample implementation
    at https://www.freedesktop.org/software/systemd/man/latest/sd_notify.html .
    Returns True on success, False otherwise.
    """
    sock_path = os.environ.get("NOTIFY_SOCKET")
    if not sock_path:
        # No notification socket defined.
        return True
    elif sock_path[0] == "@":
        # Abstract socket, replace first byte with NUL.
        sock_path = "\0" + sock_path[1:]
    elif sock_path[0] != "/":
        raise OSError(errno.EAFNOSUPPORT, f"Unsupported socket path {sock_path}")
    with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as sock:
        if sock.connect_ex(sock_path) == 0:
            sock.sendall(message.encode())
            sock.close()
            return True
    return False


_sd_notify(f"STATUS=Starting {__name__}")
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.db_uri()
app.config["SQLALCHEMY_ECHO"] = config.db_echo()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.add_url_rule("/", view_func=SiteRoot.as_view("root"), methods=["GET"])
app.add_url_rule(
    APPLE_CONFIG_ROUTE,
    view_func=mobileconfig.AppleView.as_view("apple"),
    methods=["GET"],
)
app.add_url_rule(
    INITDB_ROUTE,
    view_func=InitDatabase.as_view("initdb"),
    methods=["DELETE", "GET", "POST"],
)
app.add_url_rule(
    MOZILLA_CONFIG_ROUTE,
    view_func=autoconfig.MozillaView.as_view("mozilla"),
    methods=["GET"],
)
app.add_url_rule(
    MSOFT_ALTERNATE_ROUTE,
    view_func=autodiscover.OutlookView.as_view("ms2"),
    methods=["POST"],
)
app.add_url_rule(
    MSOFT_CONFIG_ROUTE,
    view_func=autodiscover.OutlookView.as_view("ms1"),
    methods=["POST"],
)
_proxy_fix()
db.init_app(app)
migrate = Migrate(app, db)
_sd_notify(f"STATUS=Started {__name__}")
_sd_notify("READY=1")
