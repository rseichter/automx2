"""
App views: Database related.
"""
from flask import url_for
from flask.views import MethodView

from automx2.model import Provider
from automx2.model import db
from automx2.model import populate_db


class InitDatabase(MethodView):
    # noinspection PyMethodMayBeStatic
    def get(self):
        db.create_all()
        if Provider.query.count() == 0:
            populate_db(db.session)
            db.session.commit()
        url = url_for('root')
        return f'Database is now prepared. <a href="{url}">Click here</a> to go back.'
