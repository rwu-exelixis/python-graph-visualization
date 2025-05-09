GIT_ROOT=$(git rev-parse --show-toplevel)

set -o errexit
set -o nounset
set -o pipefail

streamlit run ${GIT_ROOT}/examples/streamlit-example.py
