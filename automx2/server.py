"""
Flask server application.
"""
from flask import Flask
from flask_migrate import Migrate
from werkzeug.contrib.fixers import ProxyFix

from automx2.config import config
from automx2.model import db
from automx2.views import autoconfig
from automx2.views import autodiscover
from automx2.views import mobileconfig
from automx2.views.database import InitDatabase
from automx2.views.site import SiteRoot

APPLE_CONFIG_ROUTE = '/mobileconfig/'
MOZILLA_CONFIG_ROUTE = '/mail/config-v1.1.xml'
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
app.add_url_rule(MSOFT_CONFIG_ROUTE, view_func=autodiscover.OutlookView.as_view('msoft'), methods=['POST'])
_proxy_fix()

db.init_app(app)
migrate = Migrate(app, db)
