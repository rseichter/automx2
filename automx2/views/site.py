"""
App views: The site's root page.
"""
from flask import url_for
from flask.views import MethodView
from sqlalchemy.exc import OperationalError

from automx2.views import EMAIL_MOZILLA
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
        address = 'abc@example.com'
        url = f'{url_for("mozilla")}?{EMAIL_MOZILLA}={address}'
        return f'Show Thunderbird <a href="{url}">XML configuration</a> for {address}.'
