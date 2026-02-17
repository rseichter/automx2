#!/usr/bin/env bash
# vim: ts=4 sw=4 noet
# shellcheck disable=1091,2155
#
# Script to package automx2 for distribution and to handle PyPI uploads.
# You need Python modules 'wheel' and 'twine' to publish to PyPI, and
# Ruby Gems 'asciidoctor' and 'asciidoctor-diagram' to generate HTML
# documentation.

set -euo pipefail

function usage() {
	local n="$(basename "${0}")"
	cat >&2 <<EOT
Usage: ${n} {docs | lint | pypi}
       ${n} setver {version}
EOT
	exit 1
}

function _docs() {
	local ad=asciidoctor
	# local ad="$HOME"/.local/share/gem/ruby/3.3.0/bin/asciidoctor
	local opt=(
		'-r' 'asciidoctor-diagram'
		'-v'
		'automx2.adoc'
	)
	pushd docs >/dev/null
	"${ad}-pdf" -a toc=preamble "${opt[@]}"
	"${ad}" -a toc=right -o index.html "${opt[@]}"
	popd >/dev/null
}

function _lint() {
	local fn tmp=$(mktemp)
	# shellcheck disable=2064
	trap "rm $tmp" EXIT
	for fn in contrib/*.json; do
		jsonlint --strict --format --sort preserve "$fn" |
			sed -e 's/" :/":/g' -e 's/[[:space:]]\+$//' >"$tmp"
		catto "$fn" "$tmp"
	done
	flake8 . --select=E9,F63,F7,F82 --show-source
	flake8 . --exit-zero
}

function _pypi() {
	twine upload dist/*
}

function _setver() {
	[[ $# -gt 0 ]] || usage
	sed -E -i"" "s/^(__version__ =).*/\1 \"${1}\"/" src/automx2/__init__.py
	sed -E -i"" "s/^(version =).*/\1 \"${1}\"/" pyproject.toml
	sed -E -i"" "s/^(:revnumber:).+/\1 ${1}/" docs/automx2.adoc
	sed -E -i"" "s/^(:revdate:).+/\1 $(date +%F)/" docs/automx2.adoc
}

[[ $# -gt 0 ]] || usage
declare -r verb="${1}"
shift
case "${verb}" in
docs | lint | setver)
	_"${verb}" "$@"
	;;
pypi)
	. .venv/bin/activate
	_"${verb}" "$@"
	;;
*)
	usage
	;;
esac
