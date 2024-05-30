#!/usr/bin/env bash
# vim: ts=4 sw=4 noet
#
# Launches automx2 as a Flask application. Execute this script from
# within the parent directory of your Python venv. Example usage:
#
# (1) flask.sh run --port=4243
# Launches application for http://127.0.0.1:4243/ . This is the typical
# production configuration when running behind a proxy server.
#
# (2) flask.sh run --host=somehost.example.com --port=80
# Launches application for http://somehost.example.com/ . This allows
# automx2 to run without a proxy server.

# User configurable section -- START

# If you want to override the paths where automx2 searches for configuration
# files, set the following environment variable to an absolute path.
#export AUTOMX2_CONF='/path/to/your/automx2.conf'
# Set the following to either 'development' or 'production'.
export FLASK_ENV=production

# User configurable section -- END

export FLASK_APP=automx2.server:app
"$(dirname "$0")/flask" "$@"
