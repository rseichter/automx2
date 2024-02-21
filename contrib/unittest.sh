#!/usr/bin/env bash
# vim: ts=4 sw=4 noet
#
# Runs unittests for automx2. Example usage:
#
# (1) unittest.sh
# Run all unittests without collecting coverage data.
#
# (2) unittest.sh coverage
# Run all unittests and collect coverage data. This will also
# generate a HTML-based coverage report.

set -euo pipefail

. .venv/bin/activate
[[ ! -r local/secrets ]] || . local/secrets

export AUTOMX2_CONF='tests/unittest.conf'
if [ ! -f ${AUTOMX2_CONF} ]; then
	echo "Missing config file ${AUTOMX2_CONF}" >&2
	exit 1
fi

function usage() {
	echo "Usage: $(basename "${0}") [coverage]" >&2
	exit 1
}

function run_tests() {
	local env_=(
		NETWORK_TESTS=0
		RUN_LDAP_TESTS=0
		PYTHONPATH=.
	)
	local cmd=${1}
	shift
	# shellcheck disable=SC2086
	env "${env_[@]}" ${cmd} -m unittest discover tests/ "$@"
}

function run_coverage() {
	local rcf="--rcfile=tests/coverage.rc"
	local opt="${rcf} --precision=1 --skip-empty"
	run_tests "coverage run ${rcf} --source=automx2"
	coverage report "${opt}"
	coverage html "${opt}"
}

if [ $# -gt 0 ]; then
	case "${1}" in
		coverage)
			run_"${1}"
			;;
		*)
			usage
	esac
else
	run_tests python
fi
