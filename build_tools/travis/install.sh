#!/bin/bash
set -e

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

SETUP_OPTS="--with-coverage"
if [ "$CHECK_WARNINGS" == "true" ]; then
  SETUP_OPTS="$SETUP_OPTS --warnings"
fi
if [ "$WITH_CYTHON" == "true" ]; then
  SETUP_OPTS="$SETUP_OPTS --with-cython"
fi
python setup.py develop $SETUP_OPTS

