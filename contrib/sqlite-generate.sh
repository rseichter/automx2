#!/usr/bin/env bash
# vim:tabstop=4:noexpandtab
#
# Generates SQL statements to add a provider, servers, and domain.
# Adapt the configurable section below to your needs.

set -e

# User configurable section -- START
PROVIDER_NAME='Me, myself and I'
PROVIDER_SHORTNAME='Me'
PROVIDER_ID=123
DOMAIN='example.com'
IMAP_SERVER="imap.${DOMAIN}"
SMTP_SERVER="smtp.${DOMAIN}"
# User configurable section -- END

s1id=$((PROVIDER_ID+1))
s2id=$((PROVIDER_ID+2))
domid=$((PROVIDER_ID+3))

cat <<EOT
INSERT INTO provider VALUES(${PROVIDER_ID}, '${PROVIDER_NAME}', '${PROVIDER_SHORTNAME}');
INSERT INTO server VALUES(${s1id}, 993, 'imap', '${IMAP_SERVER}', 'SSL', '%EMAILLOCALPART%', 'plain');
INSERT INTO server VALUES(${s2id}, 587, 'smtp', '${SMTP_SERVER}', 'STARTTLS', '%EMAILLOCALPART%', 'plain');
INSERT INTO domain VALUES(${domid}, ${PROVIDER_ID}, '${DOMAIN}');
INSERT INTO server_domain VALUES(${s1id}, ${domid});
INSERT INTO server_domain VALUES(${s2id}, ${domid});
EOT