#!/usr/bin/env bash
set -vex

################
# DEPENDENCIES #
################

## Load modules
type module >& /dev/null || . /mnt/software/Modules/current/init/bash

module purge

module load gcc
module load git
module load samtools

module load python/2

case "${bamboo_planRepository_branchName}" in
  master)
    module load blasr/master
    ;;
  *)
    module load blasr/develop
    ;;
esac


rm -rf prebuilts build
test -d .pip/wheels && find .pip/wheels -type f ! -name '*none-any.whl' -print -delete || true

export NX3PBASEURL=http://nexus/repository/unsupported/pitchfork/gcc-6.4.0
export PATH="${PWD}/build/bin:${PATH}"
export PYTHONUSERBASE="${PWD}/build"
export PIP="pip --cache-dir=$bamboo_build_working_directory/.pip"

CUR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "${CUR_DIR}"/scripts/ci/build.sh
source "${CUR_DIR}"/scripts/ci/test.sh
