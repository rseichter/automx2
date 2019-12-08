"""
Provides access methods for configuration information.
"""
from configparser import ConfigParser
from pathlib import Path
from typing import List

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

    def seed_filter_sections(self, prefix: str) -> List[dict]:
        sections = []
        section: str
        for section in self._parser.sections():
            if section.startswith(prefix):
                sections.append({
                    'section_name': section,
                    'id': section[len(prefix):],
                })
        return sections

    def seed_domains(self) -> List[dict]:
        sections = self.seed_filter_sections('seed.domain.')
        d: dict
        for d in sections:
            d['name'] = self.get('name', section=d['section_name'])
            d['provider'] = self.get('provider', section=d['section_name'])
            d['servers'] = self.get('servers', section=d['section_name'])
        return sections

    def seed_providers(self) -> List[dict]:
        sections = self.seed_filter_sections('seed.provider.')
        d: dict
        for d in sections:
            d['name'] = self.get('name', section=d['section_name'])
            d['short_name'] = self.get('short_name', section=d['section_name'])
        return sections

    def seed_servers(self) -> List[dict]:
        sections = self.seed_filter_sections('seed.server.')
        d: dict
        for d in sections:
            d['name'] = self.get('name', section=d['section_name'])
            d['port'] = self.get('port', section=d['section_name'])
            d['type'] = self.get('type', section=d['section_name'])
        return sections


config = Config()
log.setLevel(config.loglevel())
