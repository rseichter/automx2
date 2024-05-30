#!/usr/bin/env bash
# vim: ts=4 sw=4 noet ft=sh
#
# Copyright © 2019-2024 Ralph Seichter
#
# This file is part of automx2.
#
# automx2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# automx2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with automx2. If not, see <https://www.gnu.org/licenses/>.

set -euo pipefail

# shellcheck disable=2155
declare -r BN=$(basename "$0")

function die {
	echo >&2 "$@"
	exit 1
}

function usage {
	die "Usage: $BN [venv-path]"
}

function download {
	local url=$1 dest=$2
	if type -f curl; then
		curl -so "$dest" "$url"
	elif type -f wget; then
		wget -qO "$dest" "$url"
	else
		die "Found neither curl nor wget in PATH, exiting."
	fi
}

function main {
	local flask pip venv
	if [[ $# -eq 0 ]]; then
		venv=.venv
	elif [[ $# -eq 1 ]]; then
		venv=$1
	else
		usage
	fi
	[[ ! -r "$venv" ]] || die "$venv already exists, exiting."
	echo "Create Python virtual environment"
	python3 -m venv "$venv"
	flask="$venv/bin/flask.sh"
	echo "Download wrapper script $flask"
	download https://raw.githubusercontent.com/rseichter/automx2/master/contrib/flask.sh "$flask"
	chmod 0755 "$flask"
	pip="$venv/bin/pip"
	"$pip" install -U pip wheel setuptools
	"$pip" install automx2
	echo "Installation complete"
}

main "$@"
