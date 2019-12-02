"""
Configuration generator for Outlook et al.
See https://support.microsoft.com/en-us/help/3211279/outlook-2016-implementation-of-autodiscover
"""
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import tostring

from automx2 import log
from automx2.generators import ConfigGenerator
from automx2.model import Domain
from automx2.model import Server

NS_AUTODISCOVER = 'http://schemas.microsoft.com/exchange/autodiscover/responseschema/2006'
NS_RESPONSE = 'http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a'

type_map = {
    'imap': 'IMAP',
    'smtp': 'SMTP',
}

"""
<Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/responseschema/2006">
    <Response xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a">
        <Account>
            <AccountType>email</AccountType>
            <Action>settings</Action>
            <Protocol>
                <Type>IMAP</Type>
                <Server>mailbox.mein-edv-blog.de</Server>
                <Port>993</Port>
                <LoginName><? echo $kennung ?></LoginName>
                <DomainRequired>off</DomainRequired>
                <SPA>off</SPA>
                <SSL>on</SSL>
                <AuthRequired>on</AuthRequired>
            </Protocol>
            <Protocol>
                <Type>SMTP</Type>
                <Server>relay.mein-edv-blog.de</Server>
                <Port>465</Port>
                <LoginName><? echo $kennung ?></LoginName>
                <DomainRequired>off</DomainRequired>
                <SPA>off</SPA>
                <SSL>on</SSL>
                <AuthRequired>on</AuthRequired>
            </Protocol>
        </Account>
    </Response>
</Autodiscover>
"""


class OutlookGenerator(ConfigGenerator):
    @staticmethod
    def on_off(o: object):
        if o:
            return 'on'
        return 'off'

    def protocol_element(self, parent: Element, server: Server) -> Element:
        element = SubElement(parent, 'Protocol')
        SubElement(element, 'Type').text = type_map[server.type]
        SubElement(element, 'Server').text = server.name
        SubElement(element, 'Port').text = str(server.port)
        SubElement(element, 'LoginName').text = server.user_name
        SubElement(element, 'SSL').text = self.on_off('SSL' == server.authentication)
        SubElement(element, 'AuthRequired').text = self.on_off(True)
        return element

    def client_config(self, domain_name: str) -> str:
        domain: Domain = Domain.query.filter_by(name=domain_name).first()
        autodiscover = Element('Autodiscover', attrib={'xmlns': NS_AUTODISCOVER})
        response = SubElement(autodiscover, 'Response', attrib={'xmlns': NS_RESPONSE})
        if domain is not None:
            account = SubElement(response, 'Account')
            SubElement(account, 'AccountType').text = 'email'
            SubElement(account, 'Action').text = 'settings'
            if domain:
                for server in domain.servers:
                    if server.type in type_map:
                        self.protocol_element(account, server)
                    else:
                        log.error(f'Unexpected server type "{server.type}"')
        data = tostring(autodiscover, 'utf-8')
        return data
