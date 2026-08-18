#!/usr/bin/env bash
set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
export PYTHONPATH="$script_dir/src${PYTHONPATH:+:$PYTHONPATH}"
if command -v python >/dev/null 2>&1; then
    python_command=python
elif command -v python3 >/dev/null 2>&1; then
    python_command=python3
else
    echo "python or python3 is required" >&2
    exit 127
fi

"$python_command" -m esm2_fitness.pipeline "$@"
