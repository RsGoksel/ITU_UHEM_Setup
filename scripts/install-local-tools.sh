#!/bin/sh
set -eu
prefix=${HOME}/.local
if [ "${1:-}" = "--help" ]; then
    printf '%s\n' 'Usage: sh scripts/install-local-tools.sh [--prefix DIRECTORY]'
    exit 0
fi
if [ "$#" -gt 0 ]; then
    [ "$#" -eq 2 ] && [ "$1" = '--prefix' ] || { printf '%s\n' 'Invalid arguments' >&2; exit 2; }
    prefix=$2
fi
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_file=$script_dir/uhem-check.py
target=$prefix/bin/uhem-check
if [ -e "$target" ] || [ -L "$target" ]; then
    if [ ! -L "$target" ] && cmp -s "$source_file" "$target"; then
        printf '%s\n' "Already installed: $target"
        exit 0
    fi
    printf '%s\n' "Existing file preserved: $target; choose another --prefix or back it up explicitly." >&2
    exit 1
fi
mkdir -p "$prefix/bin"
temporary=$(mktemp "$prefix/bin/.uhem-check.XXXXXXXX")
trap 'rm -f "$temporary"' EXIT HUP INT TERM
install -m 755 "$source_file" "$temporary"
# A hard link creates the destination atomically and refuses an existing file.
ln -T "$temporary" "$target"
printf '%s\n' "Installed: $target"
