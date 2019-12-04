#!/usr/bin/env bash
# vim:tabstop=4:noexpandtab
#
# Script to package automx2 for distribution and to handle PyPI uploads.
# You need Python modules 'wheel' and 'twine' to use this script.

set -e

function usage() {
	local bn
	bn="$(basename $0)"
	echo "Usage: ${bn} {clean | dist}" >&2
	echo "       ${bn} upload [repository]" >&2
	exit 1
}

function do_dist() {
	python setup.py sdist bdist_wheel
}

function do_upload() {
	if [ $# -gt 0 ]; then
		repo="$1"
	fi
	local opt=(
		'-sign'
		'-i'
		'D3DCBBA4EFA680A1C5C85708593AAE2E98E2219D'
		'-r'
		"${repo:-testpypi}"
	)
	twine upload "${opt[@]}" dist/*
}

[ $# -gt 0 ] || usage
arg="$1"
shift
case "$arg" in
	clean)
		rm -r build/* dist/*
		;;
	dist | upload)
		source venv/bin/activate
		do_$arg "$@"
		;;
	*)
		usage
		;;
esac
