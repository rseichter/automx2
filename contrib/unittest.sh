#!/usr/bin/env bash
#
# Runs unittests for automx2.

set -e
conf="$(mktemp)"
trap 'rm ${conf}' EXIT

# Generate temporary configuration file for this test run
cat > ${conf} <<EOT
[DEFAULT]
db_echo = no
db_uri = sqlite:///:memory:
loglevel = FATAL
EOT

source venv/bin/activate
export AUTOMX2_CONF=${conf}
export PYTHONPATH=".:${PYTHONPATH}"
python -m unittest discover tests/ "$@"
