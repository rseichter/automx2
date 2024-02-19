#!/usr/bin/env bash
# vim:ts=4:sw=4:noet
#
# Script to package automx2 for distribution and to handle PyPI uploads.
# You need Python modules 'wheel' and 'twine' to publish to PyPI, and
# Ruby Gems 'asciidoctor' and 'asciidoctor-diagram' to generate HTML
# documentation.

set -euo pipefail

function usage() {
	local n="$(basename $0)"
	cat >&2 <<EOT
Usage: ${n} {clean | dist | docs}
       ${n} upload [repository]
       ${n} setver {version}
EOT
	exit 1
}

function do_clean() {
	/bin/rm -r build/* dist/*
}

function do_dist() {
	python -m build --no-isolation
}

function do_docs() {
	local ad="${HOME}/.gem/ruby/3.0.0/bin/asciidoctor"
	local opt=(
		'-r' 'asciidoctor-diagram'
		'-v'
		'automx2.adoc'
	)
	pushd docs >/dev/null
	"${ad}-pdf" -a toc=preamble "${opt[@]}"
	${ad} -a toc=right -o index.html "${opt[@]}"
	popd >/dev/null
}

function do_upload() {
	twine upload dist/*
}

function do_setver() {
	[ $# -gt 0 ] || usage
	sed -E -i -e "s/^(VERSION =).*/\1 '${1}'/" automx2/__init__.py
	sed -E -i -e "s/^(version =).*/\1 ${1}/" setup.cfg
	sed -E -i -e "s/^(:revnumber:).+/\1 ${1}/" docs/automx2.adoc
	sed -E -i -e "s/^(:revdate:).+/\1 $(date +%F)/" docs/automx2.adoc
}

[ $# -gt 0 ] || usage
arg="$1"
shift
case "$arg" in
	clean | docs)
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
