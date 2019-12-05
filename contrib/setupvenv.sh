#!/usr/bin/env bash
# vim:tabstop=4:noexpandtab
#
# Creates a Python 3 virtual environment. The target directory can be passed
# as a parameter. The default path is 'venv' in the current directory.

dir="${1:-venv}"

set -e
if [ -d "${dir}" ]; then
	echo "Directory '${dir}' already exists, exiting." >&2
	exit 1
fi
python3 -m venv "${dir}"
source "${dir}/bin/activate"

set +e
pip install -U pip setuptools || true
