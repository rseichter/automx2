# vim: ts=4 sw=4 noet
package 	= contrib/package.sh
test_env	?= AUTOMX2_CONF=tests/unittest.conf NETWORK_TESTS=1 RUN_LDAP_TESTS=0 PYTHONPATH=.

define usage

Available make targets:

clean   Cleanup build artifacts
distro  Build distribution artifacts
docs    Generate documentation
dtest   Developer tests
help    Display this text
push    Push to all configured Git remotes
shc     Shell script care

endef

.PHONY:	clean distro docs dtest help shc

help:
	$(info $(usage))
	@exit 0

clean:
	$(package) clean || true

dtest:
	$(test_env) coverage run --source automx2 -m unittest discover -v tests/
	coverage html --rcfile=tests/coverage.rc

distro:
	$(package) $@

docs:
	$(package) $@

shc:
	shcare contrib/*.sh || shellcheck -x contrib/*.sh
