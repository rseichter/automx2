#!/usr/bin/env bash
# vim: ts=4 sw=4 noet
#
# Creates a Python 3 virtual environment. The target directory can be passed
# as a parameter. The default path is '.venv' in the current directory.

venv="${1:-.venv}"

set -e
if [ -r "${venv}" ]; then
	echo >&2 "${venv} already exists, exiting."
	exit 1
fi
python3 -m venv "${venv}"
# shellcheck disable=SC1091
. "${venv}/bin/activate"

set +e
pip install -U pip setuptools wheel || true
unset venv
