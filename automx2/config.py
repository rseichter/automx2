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
from configparser import ConfigParser
from pathlib import Path

from automx2 import IDENTIFIER
from automx2 import log
from automx2.util import from_environ

# Changing config keys will break existing end user config files.
CONF_DB_ECHO = 'db_echo'
CONF_DB_URI = 'db_uri'
CONF_LOGLEVEL = 'loglevel'
CONF_PROXY_COUNT = 'proxy_count'

# Default values will be overridden by user-defined values.
_DEFAULT_CONF = {
    IDENTIFIER: {
        CONF_DB_ECHO: 'no',
        CONF_DB_URI: 'sqlite:///:memory:',
        CONF_LOGLEVEL: 'WARNING',
        CONF_PROXY_COUNT: 0,
    }
}


class Config:
    """Handle access to configuration information."""

    def __init__(self) -> None:
        self._parser = ConfigParser()
        self._parser.read_dict(_DEFAULT_CONF)
        file_name = f'{IDENTIFIER}.conf'
        paths = [
            Path(Path.home(), f'.{file_name}'),
            Path(f'/etc/{IDENTIFIER}', file_name),
            Path('/etc', file_name),
        ]
        path = from_environ('AUTOMX2_CONF')
        if path:
            paths.insert(0, Path(path))
        for path in paths:
            log.debug(f'Checking {path.resolve()}')
            if path.exists():
                log.debug(f'Reading {path.resolve()}')
                self._parser.read_file(path.open('rt'))
                return
        log.warning('No configuration file found')

    def get(self, option: str, fallback=None, section: str = IDENTIFIER) -> str:
        value = self._parser.get(section, option, fallback=fallback)
        log.debug(f'Config.get: {option} = {value}')
        return value

    def get_bool(self, option: str, fallback=None, section: str = IDENTIFIER) -> bool:
        value = self._parser.getboolean(section, option, fallback=fallback)
        log.debug(f'Config.get_bool: {option} = {value}')
        return value

    def get_int(self, option: str, fallback=None, section: str = IDENTIFIER) -> int:
        value = self._parser.getint(section, option, fallback=fallback)
        log.debug(f'Config.get_int: {option} = {value}')
        return value

    def db_echo(self) -> bool:
        return self.get_bool(CONF_DB_ECHO)

    def db_uri(self) -> str:
        return self.get(CONF_DB_URI)

    def loglevel(self) -> str:
        return self.get(CONF_LOGLEVEL)

    def proxy_count(self) -> int:
        return self.get_int(CONF_PROXY_COUNT)


config = Config()
log.setLevel(config.loglevel())
