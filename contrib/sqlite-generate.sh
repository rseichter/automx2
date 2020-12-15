#!/usr/bin/env bash
# vim:tabstop=4:noexpandtab
#
# Generates SQL statements to add a provider, servers, and domain.
# Adapt the configurable section below to your needs.

set -e

# User configurable section -- START
PROVIDER_NAME='Foobar Worldwide'
PROVIDER_SHORTNAME='Foobar'
PROVIDER_ID=100

DOM='foobar'
TLD='tld'
DOMAIN="${DOM}.${TLD}"

IMAP_SERVER="imap.${DOMAIN}"
POP_SERVER="pop.${DOMAIN}"
SMTP_SERVER="smtp.${DOMAIN}"
# Optional LDAP server
#LDAP_SERVER="ldap.${DOMAIN}"
# User configurable section -- END

dom_id=$((PROVIDER_ID + 10))
ldap_id=$((PROVIDER_ID + 20))
s1_id=$((PROVIDER_ID + 21))
s2_id=$((PROVIDER_ID + 22))
s3_id=$((PROVIDER_ID + 23))
s4_id=$((PROVIDER_ID + 24))

cat << EOT
BEGIN;

DELETE FROM provider;
INSERT INTO provider(id, name, short_name) VALUES(${PROVIDER_ID}, '${PROVIDER_NAME}', '${PROVIDER_SHORTNAME}');

EOT

if [[ -n "${LDAP_SERVER}" ]]; then
	root="dc=${DOM},dc=${TLD}"
	cat << EOT
-- Settings tested with OpenLDAP
DELETE FROM ldapserver;
INSERT INTO ldapserver(id, name, port, use_ssl, search_base, search_filter, attr_uid, attr_cn, bind_password, bind_user)
  VALUES(${ldap_id}, '${LDAP_SERVER}', 636, 1, '${root}', '(mail={0})', 'uid', 'cn', 'SECRET', 'cn=automx2,${root}');

EOT
else
	ldap_id='NULL'
fi

cat << EOT
DELETE FROM provider;
INSERT INTO provider(id, name, short_name) VALUES(${PROVIDER_ID}, '${PROVIDER_NAME}', '${PROVIDER_SHORTNAME}');

DELETE FROM server;
INSERT INTO server(id, port, type, name, socket_type, user_name, authentication)
  VALUES(${s1_id}, 993, 'imap', '${IMAP_SERVER}', 'SSL', '%EMAILADDRESS%', 'plain');
INSERT INTO server(id, port, type, name, socket_type, user_name, authentication)
  VALUES(${s2_id}, 995, 'pop', '${POP_SERVER}', 'SSL', '%EMAILADDRESS%', 'plain');
INSERT INTO server(id, port, type, name, socket_type, user_name, authentication)
  VALUES(${s3_id}, 110, 'pop', '${POP_SERVER}', 'STARTTLS', '%EMAILADDRESS%', 'plain');
INSERT INTO server(id, port, type, name, socket_type, user_name, authentication)
  VALUES(${s4_id}, 587, 'smtp', '${SMTP_SERVER}', 'STARTTLS', '%EMAILADDRESS%', 'plain');

DELETE FROM domain;
INSERT INTO domain(id, name, provider_id, ldapserver_id) VALUES(${dom_id}, '${DOMAIN}', ${PROVIDER_ID}, ${ldap_id});

DELETE FROM server_domain;
INSERT INTO server_domain(server_id, domain_id) VALUES(${s1_id}, ${dom_id});
INSERT INTO server_domain(server_id, domain_id) VALUES(${s2_id}, ${dom_id});
INSERT INTO server_domain(server_id, domain_id) VALUES(${s3_id}, ${dom_id});
INSERT INTO server_domain(server_id, domain_id) VALUES(${s4_id}, ${dom_id});

COMMIT;
EOT
