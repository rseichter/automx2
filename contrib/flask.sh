#!/usr/bin/env bash
# vim:tabstop=4:noexpandtab
#
# Launches automx2 as a Flask application. Execute this script from
# within the parent directory of your Python venv. Example usage:
#
# (1) flask.sh run
# Launches application for http://127.0.0.1:5000/
#
# (2) flask.sh run --host=foo.example.com --port=1234
# Launches application for http://foo.example.com:1234/

set -e
source venv/bin/activate

# User configurable section -- START
#export AUTOMX2_CONF='/path/to/your/automx2.conf'
export AUTOMX2_CONF='local/test.conf'
export FLASK_ENV='development'
#export FLASK_ENV='production'
# User configurable section -- END

export FLASK_APP='automx2.server:app'
flask "$@"
