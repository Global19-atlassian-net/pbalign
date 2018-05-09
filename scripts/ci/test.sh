#!/usr/bin/env bash
set -vex

########
# TEST #
########

rm -rf test-reports
mkdir test-reports

cd repos/pbalign
nosetests  \
  --verbose --with-xunit \
  --xunit-file=${bamboo_build_working_directory}/test-reports/pbalign_xunit.xml \
  tests/unit/*.py
cram \
  --xunit-file=${bamboo_build_working_directory}/test-reports/pbalign_cramunit.xml \
  tests/cram
chmod +w -R .
