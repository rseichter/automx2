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
lint    Lint JSON files, check scripts.
ltest   LDAP related tests.
setup   Setup development venv.

endef

.PHONY:	clean dist docs dtest fmt help lint ltest setup

help:
	$(info $(usage))
	@exit 0

setup:
	@if [[ -e .venv ]]; then echo >&2 Found existing .venv; exit 1; fi
	python3 -m venv .venv
	.venv/bin/pip install -U pip wheel
	.venv/bin/pip install -r requirements.txt -r requirements-ci.txt -r requirements-psql.txt

clean:
	rm -fr *.log dist/* src/*.egg-info ./**/__pycache__

dtest:
	$(test_env) coverage run --source automx2 -m unittest discover -v tests/
	coverage html --rcfile=tests/coverage.rc

ltest:
	local/unittest-with-ldap.sh

dist:	clean fmt lint docs
	python -m build

docs:
	$(package) $@

lint:
	scare contrib/*.sh || shellcheck -x contrib/*.sh
	$(package) $@

fmt:
	isort src/automx2 tests
	black **/*.py
