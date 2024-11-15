#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
set -o xtrace

python -m ruff check . --fix
python -m ruff format .
