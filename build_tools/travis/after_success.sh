#!/bin/bash
# This script is meant to be called by the "after_success" step defined in
# .travis.yml. See https://docs.travis-ci.com/ for more details.

# License: 3-clause BSD

set -e

if [[ "$COVERAGE" == "true" ]]; then
    # Ignore codecov failures as the codecov server is not
    # very reliable but we don't want travis to report a failure
    # in the github UI just because the coverage report failed to
    # be published.
    codecov --root $TRAVIS_BUILD_DIR || echo "codecov upload failed"
fi
