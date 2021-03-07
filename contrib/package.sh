#!/usr/bin/env bash
# vim:tabstop=4:noexpandtab
#
# Script to package automx2 for distribution and to handle PyPI uploads.
# You need Python modules 'wheel' and 'twine' to publish to PyPI, and
# Ruby Gems 'asciidoctor' and 'asciidoctor-diagram' to generate HTML
# documentation.

set -euo pipefail

function usage() {
	local bn
	bn="$(basename $0)"
	echo "Usage: ${bn} {clean | dist | doc}" >&2
	echo "       ${bn} upload [repository]" >&2
	echo "       ${bn} setver {version}" >&2
	exit 1
}

function do_clean() {
	/bin/rm -r build/* dist/*
}

function do_dist() {
	python setup.py sdist bdist_wheel
}

function do_doc() {
	local opts='-r asciidoctor-diagram -v automx2.adoc'
	pushd doc >/dev/null
	asciidoctor-pdf -a toc=preamble ${opts}
	asciidoctor -a toc=right -o index.html ${opts}
	popd >/dev/null
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

function do_setver() {
	[ $# -gt 0 ] || usage
	sed -E -i -e "s/^(VERSION = ).+/\1'${1}'/" automx2/__init__.py
	sed -E -i -e "s/^(:revnumber:).+/\1 ${1}/" doc/automx2.adoc
	sed -E -i -e "s/^(:revdate:).+/\1 $(date +%F)/" doc/automx2.adoc
}

[ $# -gt 0 ] || usage
arg="$1"
shift
case "$arg" in
	clean | doc)
		do_$arg
		;;
	dist | upload)
		source .venv/bin/activate
		do_$arg "$@"
		;;
	setver)
		do_$arg "$@"
		;;
	*)
		usage
		;;
esac
