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
CONF_SECTION_DEFAULT = 'DEFAULT'

# Default values will be overridden by user-defined values.
_DEFAULT_CONF = {
    CONF_SECTION_DEFAULT: {
        CONF_DB_ECHO: 'no',
        CONF_DB_URI: 'sqlite:///:memory:',
        CONF_LOGLEVEL: 'WARNING',
    }
}


class Config:
    def __init__(self) -> None:
        self._parser = ConfigParser()
        self._parser.read_dict(_DEFAULT_CONF)
        file_name = f'{IDENTIFIER}.conf'
        paths = [
            Path('/etc', file_name),
            Path(Path.home(), file_name),
        ]
        env = from_environ('AUTOMX2_CONF')
        if env:
            paths.insert(0, Path(env))
        for path in paths:
            log.debug(f'Checking {path.resolve()}')
            if path.exists():
                log.debug(f'Reading {path.resolve()}')
                self._parser.read_file(path.open('rt'))
                return
        log.warning('No configuration file found')

    def get(self, option: str, fallback=None, section: str = CONF_SECTION_DEFAULT) -> str:
        value = self._parser.get(section, option, fallback=fallback)
        log.debug(f'Config.get: {option} = {value}')
        return value

    def get_bool(self, option: str, fallback=None, section: str = CONF_SECTION_DEFAULT) -> bool:
        value = self._parser.getboolean(section, option, fallback=fallback)
        log.debug(f'Config.get_bool: {option} = {value}')
        return value

    def db_echo(self) -> bool:
        return self.get_bool(CONF_DB_ECHO)

    def db_uri(self) -> str:
        return self.get(CONF_DB_URI)

    def loglevel(self) -> str:
        return self.get(CONF_LOGLEVEL)

    def _filter_sections(self, prefix: str) -> List[dict]:
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
        sections = self._filter_sections('seed.domain.')
        d: dict
        for d in sections:
            d['name'] = self.get('name', section=d['section_name'])
            d['provider'] = self.get('provider', section=d['section_name'])
            d['servers'] = self.get('servers', section=d['section_name'])
        return sections

    def seed_providers(self) -> List[dict]:
        sections = self._filter_sections('seed.provider.')
        d: dict
        for d in sections:
            d['name'] = self.get('name', section=d['section_name'])
            d['short_name'] = self.get('short_name', section=d['section_name'])
        return sections

    def seed_servers(self) -> List[dict]:
        sections = self._filter_sections('seed.server.')
        d: dict
        for d in sections:
            d['name'] = self.get('name', section=d['section_name'])
            d['port'] = self.get('port', section=d['section_name'])
            d['type'] = self.get('type', section=d['section_name'])
        return sections


config = Config()
log.setLevel(config.loglevel())

if __name__ == '__main__':
    print(config.seed_providers())
