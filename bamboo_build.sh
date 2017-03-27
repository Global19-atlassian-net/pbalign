#!/bin/bash -e

PBBAM=`/bin/ls -t tarballs/pbbam*tgz|head -1`
HTSLIB=`/bin/ls -t tarballs/htslib*tgz|head -1`
BLASR=`/bin/ls -t tarballs/blasr-*tgz|head -1`
BLASR_LIBCPP=`/bin/ls -t tarballs/blasr_libcpp*tgz|head -1`
HAVE_HTSLIB=$PWD/prebuilts/`basename $HTSLIB .tgz`
HAVE_BLASR_LIBCPP=$PWD/prebuilts/`basename $BLASR_LIBCPP .tgz`
HAVE_BLASR=$PWD/prebuilts/`basename $BLASR .tgz`
HAVE_PBBAM=$PWD/prebuilts/`basename $PBBAM .tgz`
mkdir -p \
         $HAVE_HTSLIB \
         $HAVE_BLASR_LIBCPP \
         $HAVE_BLASR \
         $HAVE_PBBAM
tar zxf $HTSLIB -C $HAVE_HTSLIB
#tar zxf $PBBAM -C prebuilts
tar zxf $PBBAM -C $HAVE_PBBAM
tar zxf $BLASR_LIBCPP -C $HAVE_BLASR_LIBCPP
tar zxf $BLASR -C $HAVE_BLASR

type module >& /dev/null|| . /mnt/software/Modules/current/init/bash
module load gcc/4.9.2 git/2.8.3
module load ccache/3.2.3

cat > pitchfork/settings.mk << EOF
PREFIX            = $PWD/deployment
DISTFILES         = $PWD/.distfiles
CCACHE_DIR        = /mnt/secondary/Share/tmp/bamboo.mobs.ccachedir
# from Herb
HAVE_OPENSSL      = /mnt/software/o/openssl/1.0.2a
HAVE_PYTHON       = /mnt/software/p/python/2.7.9/bin/python
HAVE_BOOST        = /mnt/software/b/boost/1.58.0
HAVE_ZLIB         = /mnt/software/z/zlib/1.2.8
HAVE_SAMTOOLS     = /mnt/software/s/samtools/1.3.1mobs
HAVE_NCURSES      = /mnt/software/n/ncurses/5.9
# from MJ
HAVE_HDF5         = /mnt/software/a/anaconda2/4.2.0
HAVE_OPENBLAS     = /mnt/software/o/openblas/0.2.14
HAVE_CMAKE        = /mnt/software/c/cmake/3.2.2/bin/cmake
# Artifacts
HAVE_PBBAM        = $HAVE_PBBAM
HAVE_HTSLIB       = $HAVE_HTSLIB
HAVE_BLASR_LIBCPP = $HAVE_BLASR_LIBCPP
HAVE_BLASR        = $HAVE_BLASR
#
pbalign_REPO      = $PWD/repos/pbalign
PacBioTestData_REPO = $PWD/repos/PacBioTestData
EOF
cd pitchfork
cat settings.mk
echo y|make _startover
if [ -e ../tarballs/pipcache.tgz ]; then
    tar zxf ../tarballs/pipcache.tgz -C ../
fi
make pbalign
make cram nose PacBioTestData
