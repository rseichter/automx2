HERE	= $(shell pwd -P)
IMAGE	= osixia/openldap:1.4.0

.PHONY:	all run

all:
	@echo >&2 "Usage: make run"

run:
	docker run --rm --name automx2ldap --env LDAP_ORGANISATION=automx2 \
	--env LDAP_DOMAIN=example.com --env LDAP_ADMIN_PASSWORD=admin \
	-v $(HERE)/tls:/container/service/slapd/assets/certs \
	-v $(HERE)/conf:/etc/ldap/slapd.d \
	-v $(HERE)/data:/var/lib/ldap \
	-p 389:389 -p 636:636 $(IMAGE)
#	--env LDAP_TLS_CA_CRT_FILENAME=lets-encrypt-r3.pem \
#	--env LDAP_TLS_CRT_FILENAME=fullchain.pem \
#	--env LDAP_TLS_KEY_FILENAME=privkey.pem \
