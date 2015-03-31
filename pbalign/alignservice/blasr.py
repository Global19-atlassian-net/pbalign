#!/usr/bin/env python
###############################################################################
# Copyright (c) 2011-2013, Pacific Biosciences of California, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of Pacific Biosciences nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY
# THIS LICENSE.  THIS SOFTWARE IS PROVIDED BY PACIFIC BIOSCIENCES AND ITS
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL PACIFIC BIOSCIENCES OR
# ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################

"""This script defines class BalserService which calls blasr to align reads."""

# Author: Yuan Li

from __future__ import absolute_import
from pbalign.alignservice.align import AlignService
from pbalign.utils.fileutil import FILE_FORMATS, real_upath, getFileFormat
import logging


class BlasrService(AlignService):
    """Class BlasrService calls blasr to align reads."""

    @property
    def name(self):
        """Blasr Service name."""
        return "BlasrService"

    @property
    def progName(self):
        """Program to call."""
        return "blasr"

    @property
    def scoreSign(self):
        """score sign for blasr is -1, the lower the better."""
        return -1

    def __parseAlgorithmOptionItems(self, optionstr):
        """Given a string of algorithm options, reconstruct option items.
        First, split the string by white space, then reconstruct path with
        white spaces.
        """
        items = optionstr.split(' ')
        ret = []
        for index, item in enumerate(items):
            if item.endswith('\\'):
                item =  '{x} '.format(x=item)
            if index > 0 and items[index-1].endswith('\\'):
                ret[-1] = "{x}{y}".format(x=ret[-1], y=item)
            else:
                ret.append(item)
        return ret

    def _resolveAlgorithmOptions(self, options, fileNames):
        """ Resolve options specified within --algorithmOptions with
            options parsed from the command-line or the config file.
            Return updated options.
            If find conflicting values of the following options, error out.
               (1) --maxHits       and blasr -bestn
               (2) --maxAnchorSize and blasr -minMatch
               (3) --useccs        and blasr -useccs/-useccsall/useccsdenovo
            If find conflicting values of sawriter, regionTable and nproc,
            it does not matter which value is used.
            Input:
                options  : the original pbalign options from argumentList
                           and configFile.
                fileNames: an PBAlignFiles object
            Output:
                new options by resolving options specified within
                --algorithmOptions and the original pbalign options
        """
        if options.algorithmOptions is None:
            return options

        ignoredBinaryOptions = ['-m', '-out', '-V']
        ignoredUnitaryOptions = ['-h', '--help', '--version',
                                 '-v', '-vv', '-sam', '-bam']

        items = self.__parseAlgorithmOptionItems(options.algorithmOptions)
        i = 0
        try:
            while i < len(items):
                infoMsg, errMsg, item = "", "", items[i]
                if item == "-sa":
                    val = real_upath(items[i+1])
                    if fileNames.sawriterFileName != val:
                        infoMsg = "Over write sa file with {0}".format(val)
                        fileNames.sawriterFileName = val
                elif item == "-regionTable":
                    val = real_upath(items[i+1])
                    if fileNames.regionTable != val:
                        infoMsg = "Over write regionTable with {0}.\n"\
                                  .format(val)
                        fileNames.regionTable = val
                elif item == "-bestn":
                    val = int(items[i+1])
                    if options.maxHits is not None and \
                            int(options.maxHits) != val:
                        errMsg = "blasr -bestn specified within " + \
                                 "--algorithmOptions is equivalent to " + \
                                 "--maxHits. Conflicting values of " + \
                                 "--algorithmOptions '-bestn' and " +\
                                 "--maxHits have been found."
                    else:
                        options.maxHits = val
                elif item == "-minMatch":
                    val = int(items[i+1])
                    if options.minAnchorSize is not None and \
                            int(options.minAnchorSize) != val:
                        errMsg = "blasr -minMatch specified within " + \
                                 "--algorithmOptions is equivalent to " + \
                                 "--minAnchorSize. Conflicting values " + \
                                 "of --algorithmOptions '-minMatch' and " + \
                                 "--minAnchorSize have been found."
                    else:
                        options.minAnchorSize = val
                elif item == "-nproc":
                    val = int(items[i+1])
                    # The number of threads is not critical.
                    if options.nproc is None or \
                            int(options.nproc) != val:
                        infoMsg = "Over write nproc with {n}.".format(n=val)
                        options.nproc = val
                elif item == "-noSplitSubreads":
                    if not options.noSplitSubreads:
                        infoMsg = "Over write noSplitSubreads with True."
                        logging.info(self.name +
                                     ": Resolve algorithmOptions. " + infoMsg)
                        options.noSplitSubreads = True
                    del items[i]
                    continue
                elif item == "-concordant":
                    if not options.concordant:
                        infoMsg = "Over writer concordant with True."
                        logging.info(self.name +
                                     ": Resolve algorithmOptions. " + infoMsg)
                        options.concordant = True
                    del items[i]
                elif "-useccs" in item:  # -useccs, -useccsall, -useccsdenovo
                    val = item.lstrip('-')
                    if options.useccs != val and options.useccs is not None:
                        errMsg = "Found conflicting options in " + \
                            "--algorithmOptions '{v}' \nand --useccs={u}"\
                            .format(v=item, u=options.useccs)
                    else:
                        options.useccs = val
                elif item == "-seed" or item == "-randomSeed":
                    val = int(items[i+1])
                    if options.seed is None or int(options.seed) != val:
                        infoMsg = "Overwrite random seed with {0}.".format(val)
                        options.seed = val
                elif item in ignoredBinaryOptions:
                    pass
                elif item in ignoredUnitaryOptions:
                    del items[i:i+1]
                    continue
                else:
                    i += 1
                    continue

                if errMsg != "":
                    logging.error(errMsg)
                    raise ValueError(errMsg)

                if infoMsg != "":
                    logging.info(self.name + ": Resolve algorithmOptions. " +
                                 infoMsg)

                del items[i:i+2]
        except Exception as e:
            errMsg = "An error occured during parsing algorithmOptions " + \
                     "'{ao}': ".format(ao=options.algorithmOptions)
            logging.error(errMsg + str(e))
            raise ValueError(errMsg + str(e))

        # Update algorithmOptions when resolve is done
        options.algorithmOptions = " ".join(items)
        return options

    def _toCmd(self, options, fileNames, tempFileManager):
        """ Generate a command line for blasr based on options and
            PBAlignFiles, and return a command-line string which can
            be used in bash.
            Input:
                options  : arguments parsed from the command-line, the
                           config file and --algorithmOptions.
                fileNames: an PBAlignFiles object.
                tempFileManager: temporary file manager.
            Output:
                a command-line string which can be used in bash.
        """
        cmdStr = "blasr {queryFile} {targetFile} -out {outFile} ".format(
            queryFile=fileNames.queryFileName,
            targetFile=fileNames.targetFileName,
            outFile=fileNames.alignerSamOut)

        if getFileFormat(fileNames.outputFileName) == FILE_FORMATS.BAM:
            cmdStr += " -bam "
        else:
            cmdStr += " -sam "

        if ((fileNames.sawriterFileName is not None) and
                (fileNames.sawriterFileName != "")):
            cmdStr += " -sa {sawriter} ".format(
                sawriter=fileNames.sawriterFileName)

        if ((fileNames.regionTable != "") and
                (fileNames.regionTable is not None)):
            cmdStr += " -regionTable {regionTable} ".format(
                regionTable=fileNames.regionTable)

        if options.maxHits is not None and options.maxHits != "":
            cmdStr += " -bestn {n}".format(n=options.maxHits)

        if (options.minAnchorSize is not None and
                options.minAnchorSize != ""):
            cmdStr += " -minMatch {0} ".format(options.minAnchorSize)

        if options.nproc is not None and options.nproc != "":
            cmdStr += " -nproc {0} ".format(options.nproc)

        if options.minLength is not None:
            cmdStr += " -minSubreadLength {n} -minReadLength {n} ".\
                    format(n=options.minLength)

        if options.noSplitSubreads:
            cmdStr += " -noSplitSubreads "

        if options.concordant:
            cmdStr += " -concordant "

        if options.seed is not None and options.seed != 0:
            cmdStr += " -randomSeed {0} ".format(options.seed)

        if options.hitPolicy == "randombest":
            cmdStr += " -placeRepeatsRandomly "

        if options.useccs is not None and options.useccs != "":
            cmdStr += " -{0} ".format(options.useccs)

        # When input is a FASTA file, blasr -clipping = soft
        if fileNames.inputFileFormat == FILE_FORMATS.FASTA:
            cmdStr += " -clipping soft "

        if options.algorithmOptions is not None:
            cmdStr += " {0} ".format(options.algorithmOptions)

        return cmdStr

    def _preProcess(self, inputFileName, referenceFile=None,
                    regionTable=None, noSplitSubreads=None,
                    tempFileManager=None, isWithinRepository=None):
        """Preprocess input files.
            Input:
                inputFilieName : a PacBio BASE/PULSE/FOFN file.
                referenceFile  : a FASTA reference file.
                regionTable    : a region table RGN.H5/FOFN file.
                noSplitSubreads: whether to split subreads or not.
                tempFileManager: temporary file manager.
            Output:
                string, a file which can be used by blasr.
        """
        # For blasr, nothing needs to be done, return the input PacBio
        # PULSE/BASE/FOFN reads directly.
        return inputFileName

    def _postProcess(self):
        """ Postprocess after alignment is done. """
        logging.debug(self.name + ": Postprocess after alignment is done. ")
