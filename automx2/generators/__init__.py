"""
Copyright © 2019 Ralph Seichter

Graciously sponsored by sys4 AG <https://sys4.de/>

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
from automx2 import IDENTIFIER


def branded_id(id_: str) -> str:
    return f'{IDENTIFIER}-{id_}'


class ConfigGenerator:
    def client_config(self, user_name, domain_name: str, realname: str, password: str) -> str:
        raise NotImplementedError
