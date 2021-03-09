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
from flask import Flask
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix

from automx2.config import config
from automx2.model import db
from automx2.views import autoconfig
from automx2.views import autodiscover
from automx2.views import mobileconfig
from automx2.views.database import InitDatabase
from automx2.views.site import SiteRoot

APPLE_CONFIG_ROUTE = '/mobileconfig/'
MOZILLA_CONFIG_ROUTE = '/mail/config-v1.1.xml'
MSOFT_ALTERNATE_ROUTE = '/AutoDiscover/AutoDiscover.xml'
MSOFT_CONFIG_ROUTE = '/autodiscover/autodiscover.xml'


def _proxy_fix():
    """Use a fix for Werkzeug if automx2 is running behind a proxy.
    This enables support for X-Forwarded-* headers.
    """
    p = int(config.proxy_count())
    if p > 0:  # pragma: no cover (Tests don't use a proxy)
        # See https://werkzeug.palletsprojects.com/en/0.15.x/middleware/proxy_fix/
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=p, x_host=p, x_port=p, x_prefix=p, x_proto=p)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.db_uri()
app.config['SQLALCHEMY_ECHO'] = config.db_echo()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.add_url_rule('/', view_func=SiteRoot.as_view('root'), methods=['GET'])
app.add_url_rule('/initdb/', view_func=InitDatabase.as_view('initdb'), methods=['GET'])
app.add_url_rule(APPLE_CONFIG_ROUTE, view_func=mobileconfig.AppleView.as_view('apple'), methods=['GET'])
app.add_url_rule(MOZILLA_CONFIG_ROUTE, view_func=autoconfig.MozillaView.as_view('mozilla'), methods=['GET'])
app.add_url_rule(MSOFT_ALTERNATE_ROUTE, view_func=autodiscover.OutlookView.as_view('ms2'), methods=['POST'])
app.add_url_rule(MSOFT_CONFIG_ROUTE, view_func=autodiscover.OutlookView.as_view('ms1'), methods=['POST'])
_proxy_fix()

db.init_app(app)
migrate = Migrate(app, db)
