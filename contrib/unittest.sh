#!/usr/bin/env bash
# vim:tabstop=4:noexpandtab
#
# Runs unittests for automx2. Example usage:
#
# (1) unittest.sh
# Run all unittests without collecting coverage data.
#
# (2) unittest.sh coverage
# Run all unittests and collect coverage data.
#
# (3) unittest.sh report
# Generate coverage report based on data collected with (2).

set -e

source venv/bin/activate
export AUTOMX2_CONF='tests/unittest.conf'
if [ ! -f ${AUTOMX2_CONF} ]; then
	echo "Missing config file ${AUTOMX2_CONF}" >&2
	exit 1
fi

function usage() {
	echo "Usage: $(basename $0) [coverage|report]" >&2
	exit 1
}

function run_coverage() {
	coverage "$@" --rcfile=tests/coverage.rc
}

function run_tests() {
	local cmd="$1"
	shift
	PYTHONPATH=".:${PYTHONPATH}" $cmd -m unittest discover tests/ "$@"
}

cmd='python'
if [ $# -gt 0 ]; then
	arg="$1"
	shift
	case "$arg" in
		coverage):
			run_tests 'coverage run --source automx2 --rcfile=tests/coverage.rc'
			;;
		report):
			run_coverage html
			;;
		*)
			usage
	esac
else
	run_tests python
fi
