#!/usr/bin/env bash

cd python-wrapper

set -o errexit
set -o nounset
set -o pipefail

python -m ruff check .
python -m ruff format --check .
mypy .
