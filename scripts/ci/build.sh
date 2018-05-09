#!/usr/bin/env bash
set -vex

#########
# BUILD #
#########

${PIP} install --user \
  $NX3PBASEURL/pythonpkgs/pysam-0.13-cp27-cp27mu-linux_x86_64.whl \
  $NX3PBASEURL/pythonpkgs/xmlbuilder-1.0-cp27-none-any.whl \
  $NX3PBASEURL/pythonpkgs/avro-1.7.7-cp27-none-any.whl \
  iso8601 \
  $NX3PBASEURL/pythonpkgs/tabulate-0.7.5-cp27-none-any.whl \
  cram \
  nose

ln -sfn ../data repos/PacBioTestData/pbtestdata/data
${PIP} install --user -e repos/PacBioTestData
${PIP} install --user -e repos/pbcore
${PIP} install --user -e repos/pbcommand
${PIP} install --user -e repos/pbalign