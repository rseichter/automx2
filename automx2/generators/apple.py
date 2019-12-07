"""
Configuration generator for Apple's property-list based mobileconfig
"""
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import tostring

from automx2 import log
from automx2.generators import ConfigGenerator
from automx2.generators import branded_id
from automx2.model import Domain
from automx2.model import Provider
from automx2.util import unique

type_direction_map = {
    'imap': 'Incoming',
    'smtp': 'Outgoing',
}

"""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>PayloadContent</key>
        <array>
            <dict>
                <key>EmailAccountDescription</key>
                <string>willexplo.de</string>
                <key>EmailAccountName</key>
                <string>John Doe</string>
                <key>EmailAccountType</key>
                <string>EmailTypeIMAP</string>
                <key>EmailAddress</key>
                <string>jd@willexplo.de</string>
                <key>IncomingMailServerAuthentication</key>
                <string>EmailAuthPassword</string>
                <key>IncomingMailServerHostName</key>
                <string>imap.horus-it.com</string>
                <key>IncomingMailServerPortNumber</key>
                <integer>993</integer>
                <key>IncomingMailServerUseSSL</key>
                <true/>
                <key>IncomingMailServerUsername</key>
                <string>jd</string>
                <key>IncomingPassword</key>
                <string>SECR3T</string>
                <key>OutgoingMailServerAuthentication</key>
                <string>EmailAuthPassword</string>
                <key>OutgoingMailServerHostName</key>
                <string>smtp.horus-it.com</string>
                <key>OutgoingMailServerPortNumber</key>
                <integer>587</integer>
                <key>OutgoingMailServerUseSSL</key>
                <true/>
                <key>OutgoingMailServerUsername</key>
                <string>jd</string>
                <key>OutgoingPasswordSameAsIncomingPassword</key>
                <true/>
                <key>PayloadDescription</key>
                <string>Konfiguriert die E-Mail-Einstellungen</string>
                <key>PayloadDisplayName</key>
                <string>willexplo.de</string>
                <key>PayloadIdentifier</key>
                <string>com.apple.mail.managed.3A9E183A-0991-4D3C-9FB6-D09AF971A577</string>
                <key>PayloadType</key>
                <string>com.apple.mail.managed</string>
                <key>PayloadUUID</key>
                <string>3A9E183A-0991-4D3C-9FB6-D09AF971A577</string>
                <key>PayloadVersion</key>
                <integer>1</integer>
                <key>SMIMEEnablePerMessageSwitch</key>
                <false/>
                <key>SMIMEEnabled</key>
                <false/>
                <key>SMIMEEncryptionEnabled</key>
                <false/>
                <key>SMIMESigningEnabled</key>
                <false/>
                <key>allowMailDrop</key>
                <false/>
                <key>disableMailRecentsSyncing</key>
                <false/>
            </dict>
        </array>
        <key>PayloadDisplayName</key>
        <string>Mail willexplo.de</string>
        <key>PayloadIdentifier</key>
        <string>Argon.64D2666A-49C5-4F1E-8ACD-CFB3F39E4CC7</string>
        <key>PayloadRemovalDisallowed</key>
        <false/>
        <key>PayloadType</key>
        <string>Configuration</string>
        <key>PayloadUUID</key>
        <string>0CA0D726-9A9B-4876-8759-B2C0D9B52A00</string>
        <key>PayloadVersion</key>
        <integer>1</integer>
    </dict>
</plist>
"""


def bool_key(parent: Element, key: str, value: bool):
    SubElement(parent, 'key').text = key
    if value:
        v = 'true'
    else:
        v = 'false'
    SubElement(parent, v)


def int_key(parent: Element, key: str, value: int):
    SubElement(parent, 'key').text = key
    SubElement(parent, 'integer').text = str(value)


def str_key(parent: Element, key: str, value: str = ''):
    SubElement(parent, 'key').text = key
    if value:
        SubElement(parent, 'string').text = value


def subtree(parent: Element, key: str, value):
    if isinstance(value, bool):
        bool_key(parent, key, value)
    elif isinstance(value, dict):
        p = SubElement(parent, 'dict')
        for k, v in value.items():
            subtree(p, k, v)
    elif isinstance(value, int):
        int_key(parent, key, value)
    elif isinstance(value, list):
        str_key(parent, key)
        p = SubElement(parent, 'array')
        for v in value:
            subtree(p, 'dunno', v)
    else:
        str_key(parent, key, value)


def _payload_dicts(address: str):
    uuid = unique()
    inner = {
        'EmailAccountDescription': address,
        'EmailAccountName': 'John Doe',
        'EmailAccountType': 'EmailTypeIMAP',
        'EmailAddress': address,
        'IncomingMailServerAuthentication': 'EmailAuthPassword',
        'IncomingMailServerHostName': 'imap.horus-it.com',
        'IncomingMailServerPortNumber': 0,
        'IncomingMailServerUseSSL': True,
        'IncomingMailServerUsername': 'jd',
        'IncomingPassword': 'SECR3T',
        'OutgoingMailServerAuthentication': 'EmailAuthPassword',
        'OutgoingMailServerHostName': 'smtp.horus-it.com',
        'OutgoingMailServerPortNumber': 0,
        'OutgoingMailServerUseSSL': True,
        'OutgoingMailServerUsername': 'jd',
        'OutgoingPasswordSameAsIncomingPassword': True,
        'PayloadDescription': 'Email account configuration',
        'PayloadDisplayName': 'willexplo.de',
        'PayloadIdentifier': f'com.apple.mail.managed.{uuid}',
        'PayloadType': 'com.apple.mail.managed',
        'PayloadUUID': uuid,
        'PayloadVersion': 1,
        'SMIMEEnablePerMessageSwitch': False,
        'SMIMEEnabled': False,
        'SMIMEEncryptionEnabled': False,
        'SMIMESigningEnabled': False,
        'allowMailDrop': False,
        'disableMailRecentsSyncing': False,
    }
    uuid = unique()
    outer = {
        'PayloadContent': [inner],
        'PayloadDisplayName': 'UNDEFINED',
        'PayloadIdentifier': branded_id(uuid),
        'PayloadRemovalDisallowed': False,
        'PayloadType': 'Configuration',
        'PayloadUUID': uuid,
        'PayloadVersion': 1,
    }
    return inner, outer


class AppleGenerator(ConfigGenerator):
    def client_config(self, local_part, domain_name: str) -> str:
        plist = Element('plist', attrib={'version': '1.0'})
        domain: Domain = Domain.query.filter_by(name=domain_name).first()
        if domain:
            inner, outer = _payload_dicts(f'{local_part}@{domain_name}')
            provider: Provider = domain.provider
            if provider:
                for server in domain.servers:
                    if server.type in type_direction_map:
                        direction = type_direction_map[server.type]
                        inner[f'{direction}MailServerHostName'] = server.name
                        inner[f'{direction}MailServerPortNumber'] = server.port
                    else:
                        log.error(f'Unexpected server type "{server.type}"')
                if domain.servers:
                    inner['PayloadDescription'] = f'Hosted by {provider.name}'
                    inner['PayloadDisplayName'] = domain_name
                    outer['PayloadDisplayName'] = f'{domain_name} mobile email'
                    subtree(plist, '', outer)
            else:
                log.error(f'No provider for domain "{domain_name}"')
        else:
            log.error(f'Domain "{domain_name}" not found')
        data = tostring(plist, 'utf-8')
        return data
