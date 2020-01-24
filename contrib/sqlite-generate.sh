#!/usr/bin/env bash
# vim:tabstop=4:noexpandtab
#
# Generates SQL statements to add a provider, servers, and domain.
# Adapt the configurable section below to your needs.

set -e

# User configurable section -- START
PROVIDER_NAME='Foobar Worldwide'
PROVIDER_SHORTNAME='Foobar'
PROVIDER_ID=123

DOM='foobar'
TLD='tld'
DOMAIN="${DOM}.${TLD}"

IMAP_SERVER="imap.${DOMAIN}"
SMTP_SERVER="smtp.${DOMAIN}"
# Optional LDAP server
#LDAP_SERVER="ldap.${DOMAIN}"
# User configurable section -- END

s1_id=$((PROVIDER_ID + 1))
s2_id=$((PROVIDER_ID + 2))
s3_id=$((PROVIDER_ID + 3))
dom_id=$((PROVIDER_ID + 4))

if [[ -n "${LDAP_SERVER}" ]]; then
	root="dc=${DOM},dc=${TLD}"
	cat << EOT
-- Settings tested with OpenLDAP
INSERT INTO ldapserver(id, name, port, use_ssl, search_base,
search_filter, attr_uid, attr_cn, bind_password, bind_user)
VALUES(${s3_id}, '${LDAP_SERVER}', 636, 1, '${root}',
'(mail={0})', 'uid', 'cn', 'SECRET', 'cn=automx2,${root}');

EOT
else
	s3_id='NULL'
fi

cat << EOT
INSERT INTO provider(id, name, short_name) VALUES(${PROVIDER_ID}, '${PROVIDER_NAME}', '${PROVIDER_SHORTNAME}');
INSERT INTO server(id, port, type, name, socket_type, user_name, authentication)
VALUES(${s1_id}, 993, 'imap', '${IMAP_SERVER}', 'SSL', '%EMAILLOCALPART%', 'plain');
INSERT INTO server(id, port, type, name, socket_type, user_name, authentication)
VALUES(${s2_id}, 587, 'smtp', '${SMTP_SERVER}', 'STARTTLS', '%EMAILLOCALPART%', 'plain');
INSERT INTO domain(id, name, provider_id, ldapserver_id) VALUES(${dom_id}, '${DOMAIN}', ${PROVIDER_ID}, ${s3_id});
INSERT INTO server_domain(server_id, domain_id) VALUES(${s1_id}, ${dom_id});
INSERT INTO server_domain(server_id, domain_id) VALUES(${s2_id}, ${dom_id});
EOT
