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
from flask import abort
from flask import request
from flask.views import MethodView

from automx2 import AutomxException
from automx2 import NotFoundException
from automx2 import log
from automx2.generators.apple import AppleGenerator
from automx2.views import EMAIL_MOZILLA
from automx2.views import MailConfig

CONTENT_TYPE_APPLE = 'application/x-apple-aspen-config'


class AppleView(MailConfig, MethodView):
    """Autoconfigure mail, Apple-style."""

    @staticmethod
    def response_type() -> str:
        return CONTENT_TYPE_APPLE

    def get(self):
        """GET request is expected to contain ?emailaddress=user@example.com"""
        address = request.args.get(EMAIL_MOZILLA, '')
        realname = request.args.get('name', '')
        if not address:
            message = f'Missing request argument "{EMAIL_MOZILLA}"'
            log.error(message)
            return message, 400
        try:
            return self.config_from_address(address, realname)
        except NotFoundException:
            return '', 204
        except AutomxException as e:
            log.exception(e)
            abort(400)

    def config_response(self, local_part, domain_part: str, realname: str, password: str) -> str:
        data = AppleGenerator().client_config(local_part, domain_part, realname)
        return data
