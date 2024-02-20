#!/usr/bin/env bash
# vim: ts=4 sw=4 noet
#
# Creates a Python 3 virtual environment. The target directory can be passed
# as a parameter. The default path is '.venv' in the current directory.

_dir="${1:-.venv}"

set -e
if [ -r "${_dir}" ]; then
	echo >&2 "${_dir} already exists, exiting."
	exit 1
fi
python3 -m venv "${_dir}"
. "${_dir}/bin/activate"

set +e
pip install -U pip setuptools wheel || true
unset _dir
