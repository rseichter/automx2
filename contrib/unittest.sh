#!/usr/bin/env bash
# vim:tabstop=4:noexpandtab
#
# Runs unittests for automx2.

set -e
source venv/bin/activate
export AUTOMX2_CONF='tests/unittest.conf'
if [ ! -f ${AUTOMX2_CONF} ]; then
	echo "Missing config file ${AUTOMX2_CONF}" >&2
	exit 1
fi
PYTHONPATH=".:${PYTHONPATH}" python -m unittest discover tests/ "$@"
