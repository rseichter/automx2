# vim: ts=4 sw=4 noet
package 	= contrib/package.sh
test_env	?= AUTOMX2_CONF=tests/unittest.conf NETWORK_TESTS=1 RUN_LDAP_TESTS=0 PYTHONPATH=src

define usage

Available make targets:

clean   Cleanup build artifacts.
dist    Build distribution artifacts.
docs    Generate documentation.
dtest   Developer tests.
fmt     Format Python code.
help    Display this text.
shc     Shell script care.

endef

.PHONY:	clean dist docs dtest fmt help shc

help:
	$(info $(usage))
	@exit 0

clean:
	$(package) clean || true

dtest:
	$(test_env) coverage run --source automx2 -m unittest discover -v tests/
	coverage html --rcfile=tests/coverage.rc

dist:
	$(package) $@

docs:
	$(package) $@

fmt:
	black **/*.py

shc:
	shcare contrib/*.sh || shellcheck -x contrib/*.sh
