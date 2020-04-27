#!/bin/bash
# adapted from https://github.com/scikit-learn/scikit-learn/tree/master/build_tools/travis/install.sh
# This script is meant to be called by the "install" step defined in
# .travis.yml. See https://docs.travis-ci.com/ for more details.
# The behavior of the script is controlled by environment variabled defined
# in the .travis.yml in the top level folder of the project.

# License: 3-clause BSD

set -e

# Fail fast
build_tools/travis/travis_fastfail.sh

echo "List files from cached directories"
echo "pip:"
ls $HOME/.cache/pip

export CC=/usr/lib/ccache/gcc
export CXX=/usr/lib/ccache/g++
# Useful for debugging how ccache is used
# export CCACHE_LOGFILE=/tmp/ccache.log
# ~60M is used by .ccache when compiling from scratch at the time of writing
ccache --max-size 100M --show-stats

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

python setup.py develop

ccache --show-stats
# Useful for debugging how ccache is used
# cat $CCACHE_LOGFILE

