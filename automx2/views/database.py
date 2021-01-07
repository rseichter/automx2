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
from flask import url_for
from flask.views import MethodView

from automx2.model import Provider
from automx2.model import db
from automx2.model import populate_db


class InitDatabase(MethodView):
    """Initialise database."""

    # noinspection PyMethodMayBeStatic
    def get(self):
        db.create_all()
        if Provider.query.count() == 0:
            populate_db()
            db.session.commit()
        url = url_for('root')
        return f'Database is now prepared. <a href="{url}">Click here</a> to go back.'
