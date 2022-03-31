PKG 		= contrib/package.sh
RUN_LDAP_TESTS	?= 0

.PHONY:	clean dist docs push usage

usage:
	@echo >&2 "Usage: make {clean | devtest | dist | docs | push}"
	@exit 1

clean:
	$(PKG) clean || true

devtest:
	AUTOMX2_CONF=tests/unittest.conf RUN_LDAP_TESTS=$(RUN_LDAP_TESTS) PYTHONPATH=. coverage run --source automx2 -m unittest discover -v tests/
	coverage html --rcfile=tests/coverage.rc

dist:
	$(PKG) dist

docs:
	$(PKG) docs

push:
	@for r in $(shell git remote); do git push $$r; done
