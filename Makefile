PKG 		= contrib/package.sh
RUN_LDAP_TESTS	?= 0

define usage

Available make targets:

  clean
  devtest
  dist
  docs
  help
  push
  scheck

endef

.PHONY:	clean devtest dist docs help push scheck

help:
	$(info $(usage))
	@exit 0

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

scheck:
	shellcheck -e SC2155 -x contrib/*.sh
