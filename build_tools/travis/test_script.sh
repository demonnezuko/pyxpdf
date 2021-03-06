#!/bin/bash
# This script is meant to be called by the "script" step defined in
# .travis.yml. See https://docs.travis-ci.com/ for more details.
# The behavior of the script is controlled by environment variabled defined
# in the .travis.yml in the top level folder of the project.

# License: 3-clause BSD

set -e

python --version

run_tests() {
    TEST_CMD="test.py -vv"
    
    if [[ "$COVERAGE" == "true" ]]; then
      TEST_CMD="$TEST_CMD --coverage"
    fi
    python $TEST_CMD
}

run_tests
