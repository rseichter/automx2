# vim: ts=4 sw=4 noet
package 	= contrib/package.sh
test_env	?= AUTOMX2_CONF=tests/unittest.conf NETWORK_TESTS=1 RUN_LDAP_TESTS=0 PYTHONPATH=.

define usage

Available make targets:

  clean  Cleanup build artifacts
  dist   Build distribution artifacts
  docs   Generate documentation
  dtest  Developer tests
  help   Display this text
  push   Push to all configured Git remotes
  schk   Shell script check

endef

.PHONY:	clean dtest dist docs help push schk

help:
	$(info $(usage))
	@exit 0

clean:
	$(package) clean || true

dtest:
	$(test_env) coverage run --source automx2 -m unittest discover -v tests/
	coverage html --rcfile=tests/coverage.rc

dist:
	$(package) dist

docs:
	$(package) docs

push:
	for _r in $(shell git remote); do git push $$_r; done; unset _r

schk:
	shellcheck -e SC2155 -x contrib/*.sh
