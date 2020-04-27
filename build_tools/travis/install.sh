#!/bin/bash
set -e

gcc --version

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

SETUP_OPTS="--with-coverage"
if [ "$CHECK_WARNINGS" == "true" ]; then
  SETUP_OPTS="$SETUP_OPTS --warnings"
fi
if [ "$WITH_CYTHON" == "true" ]; then
  SETUP_OPTS="$SETUP_OPTS --with-cython"
fi

# travis has gcc 5.4 as of now which does not compile cpp14 by default
# so setting CFALGS which will be included by setupinfo.py as extra_compile_args
# in Extension.
export CFLAGS="-std=c++14"
export CPPFLAGS="-std=c++14"

python setup.py develop $SETUP_OPTS

