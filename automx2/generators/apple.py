"""
Configuration generator for Apple's property-list based mobileconfig
"""
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import tostring

from automx2 import log
from automx2.generators import ConfigGenerator
from automx2.model import Domain
from automx2.model import Provider
from automx2.util import unique

PAYLOAD_TYPE = 'com.apple.mail.managed'

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


def str_key(parent: Element, key: str, value: str = ''):
    SubElement(parent, 'key').text = key
    if value:
        SubElement(parent, 'string').text = value


def int_key(parent: Element, key: str, value: int):
    SubElement(parent, 'key').text = key
    SubElement(parent, 'integer').text = str(value)


class AppleGenerator(ConfigGenerator):
    def client_config(self, local_part, domain_name: str) -> str:
        root = Element('plist', attrib={'version': '1.0'})
        e = SubElement(root, 'dict')
        str_key(e, 'PayloadContent')
        e = SubElement(e, 'array')
        inner = SubElement(e, 'dict')
        domain: Domain = Domain.query.filter_by(name=domain_name).first()
        if domain:
            address = f'{local_part}@{domain_name}'
            uuid = unique()
            provider: Provider = domain.provider
            str_key(inner, 'EmailAccountDescription', address)
            for server in domain.servers:
                if server.type == 'imap':
                    str_key(inner, 'EmailAccountType', 'EmailTypeIMAP')
                    str_key(inner, 'EmailAddress', address)
                    str_key(inner, 'IncomingMailServerHostName', server.name)
                    int_key(inner, 'IncomingMailServerPortNumber', server.port)
                elif server.type == 'smtp':
                    str_key(inner, 'OutgoingMailServerHostName', server.name)
                    int_key(inner, 'OutgoingMailServerPortNumber', server.port)
            str_key(inner, 'PayloadDescription', f'Email hosted by {provider.name}')
            str_key(inner, 'PayloadDisplayName', f'{domain_name} mail')
            str_key(inner, 'PayloadIdentifier', f'{self.branded_id(provider)}.{uuid}')
            str_key(inner, 'PayloadType', PAYLOAD_TYPE)
            int_key(inner, 'PayloadVersion', 1)
            str_key(inner, 'PayloadUUID', uuid)
        else:
            log.error(f'No provider for domain "{domain_name}"')
        data = tostring(root, 'utf-8')
        return data
