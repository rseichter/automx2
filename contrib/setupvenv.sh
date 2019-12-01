#!/usr/bin/env bash
#
# Creates a Python virtual environment in the current directory.

set -e
if [ -d venv ]; then
	echo "Directory 'venv' already exists, exiting." >&2
	exit 1
fi
python3.7 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -U setuptools
