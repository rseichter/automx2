"""
App views: The site's root page.
"""
from flask import url_for
from flask.views import MethodView
from sqlalchemy.exc import OperationalError

from automx2 import ADDRESS_KEY
from automx2 import log
from automx2.model import Provider


class SiteRoot(MethodView):
    # noinspection PyMethodMayBeStatic
    def get(self):
        try:
            Provider.query.count()
        except OperationalError as e:
            log.error(e)
            url = url_for('initdb')
            return f'Operational error. Did you remember to <a href="{url}">initialise</a> the database?'
        address = 'alice@example.com'
        url = f'{url_for("mailcfg")}?{ADDRESS_KEY}={address}'
        return f'Show Thunderbird <a href="{url}">XML configuration</a> for {address}.'
