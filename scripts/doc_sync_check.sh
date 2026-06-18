#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON_SCRIPT="$SCRIPT_DIR/doc_sync_check.py"

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$PYTHON_SCRIPT" "$@"
fi

if command -v python >/dev/null 2>&1; then
    exec python "$PYTHON_SCRIPT" "$@"
fi

echo "python3 or python not found. Please install Python and try again." >&2
exit 1
