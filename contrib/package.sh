#!/usr/bin/env bash
# vim:tabsize=4:noexpandtab
#
# Utility script to package automx2 for distribution
# and to handle PyPI uploads. You need Python modules
# 'wheel' and 'twine' to use this script.

set -e

function usage() {
	echo "Usage: $(basename $0) {clean|dist|upload}" >&2
	exit 1
}

function do_clean() {
	for d in build dist; do
		if [ -d $d ]; then
			rm -r $d
		fi
	done
}

function do_dist() {
	python setup.py sdist bdist_wheel
}

function do_upload() {
	local opt=(
		'-sign'
		'-i'
		'D3DCBBA4EFA680A1C5C85708593AAE2E98E2219D'
		'-r'
		'testpypi'
	)
	twine upload "${opt[@]}" dist/*
}

test "$#" -gt 0 || usage
case "$1" in
	clean|dist|upload)
		source venv/bin/activate
		do_$1
		;;
	*)
		usage
		;;
esac
