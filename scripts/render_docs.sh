#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
set -o xtrace


GIT_ROOT=$(git rev-parse --show-toplevel)

(
    cd "${GIT_ROOT}/docs"
    make clean html
)

sphinx-build -M html "${GIT_ROOT}/docs/source/" "${GIT_ROOT}docs/build/" --fresh-env --exception-on-warning

python3 -m http.server 8000 -d "${GIT_ROOT}/docs/build/html"
