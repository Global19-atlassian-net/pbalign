from __future__ import print_function

import tempfile
from argparse import *
from os import path
import os
import filecmp
import unittest

from pbalign.options import *


def get_argument_parser():
    return get_contract_parser().arg_parser.parser

def writeConfigFile(configFile, configOptions):
    """Write configs to a file."""
    with open (configFile, 'w') as f:
        f.write("\n".join(configOptions))

def parseOptions(args):
    return get_argument_parser().parse_args(args)

class Test_Options(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.infiles = ["tmp_readfile.bam", "tmp_reffile.fasta"]
        for file_name in cls.infiles:
            open(file_name, "w").write("\n")
        cls.configFile = tempfile.NamedTemporaryFile(suffix=".config").name
        cls.configFile3 = tempfile.NamedTemporaryFile(suffix=".config").name

    @classmethod
    def tearDownClass(cls):
        for file_name in cls.infiles:
            os.remove(file_name)

    def test_importConfigOptions(self):
        """Test importConfigOptions()."""
        configOptions = ("--minAccuracy     = 40",
                         "--maxHits         = 20")
        writeConfigFile(self.configFile, configOptions)
        options = Namespace(configFile=self.configFile,
                            minAccuracy=10,
                            maxHits=12)

        newOptions, infoMsg = importConfigOptions(options)

        self.assertEqual(int(newOptions.maxHits),     20)
        self.assertEqual(int(newOptions.minAccuracy), 40)

    def test_get_argument_parser(self):
        """Test get_argument_parser()."""
        ret = get_argument_parser()
        self.assertTrue(isinstance(ret, argparse.ArgumentParser))

    def test_parseOptions(self):
        """Test parseOptions with a config file."""
        configOptions = (
            "--maxHits       = 20",
            "--minAnchorSize = 15",
            "--minLength     = 100",
            "--algorithmOptions = '--noSplitSubreads " + \
            "--maxMatch 30 --nCandidates 30'",
            "# Some comments",
            #"--scoreFunction = blasr",
            "--hitPolicy     = random",
            "--maxDivergence = 40",
            "--debug")
        writeConfigFile(self.configFile, configOptions)
        argumentList = [
            '--configFile', self.configFile,
            '--maxHits', '30',
            '--minAccuracy', '50',
        ] + self.infiles + ['outfile']
        options = parseOptions(argumentList)

        self.assertTrue(filecmp.cmp(options.configFile, self.configFile))
        self.assertEqual(int(options.maxHits),       30)
        self.assertEqual(int(options.minAccuracy),   50)

        self.assertEqual("".join(options.algorithmOptions),
                         "--noSplitSubreads --maxMatch 30 --nCandidates 30")
        #self.assertEqual(options.scoreFunction,      "blasr")
        self.assertEqual(options.hitPolicy,          "random")
        self.assertEqual(int(options.maxDivergence), 40)

    def test_parseOptions_without_config(self):
        """Test parseOptions without any config file."""
        argumentList = ['--maxHits=30',
                        '--minAccuracy=50'
        ] + self.infiles + ['outfile']
        options = parseOptions(argumentList)

        self.assertIsNone(options.configFile)
        self.assertEqual(int(options.maxHits),       30)
        self.assertEqual(int(options.minAccuracy),   50)
        self.assertIsNone(options.algorithmOptions)
        self.assertIsNone(options.minAnchorSize)

    def test_parseOptions_multi_algorithmOptions(self):
        """Test parseOptions with multiple algorithmOptions."""
        algo1 = " --holeNumbers 1"
        algo2 = " --nCandidate 25"
        algo3 = " ' --bestn 11 '"
        argumentList = [
            '--algorithmOptions=%s' % algo1,
            '--algorithmOptions=%s' % algo2,
        ] + self.infiles + ["outfile"]
        print(argumentList)
        options = parseOptions(argumentList)
        # Both algo1 and algo2 should be in algorithmOptions.
        print(options.algorithmOptions)
        #self.assertTrue(algo1 in options.algorithmOptions)
        #self.assertTrue(algo2 in options.algorithmOptions)

        # Construct a config file.
        configOptions = ("--algorithmOptions = \"%s\"" % algo3)
        writeConfigFile(self.configFile3, [configOptions])

        argumentList.append("--configFile={0}".format(self.configFile3))
        print(argumentList)
        options = parseOptions(argumentList)
        # Make sure algo3 have been overwritten.
        print(options.algorithmOptions)
        self.assertTrue(algo1 in options.algorithmOptions)
        self.assertTrue(algo2 in options.algorithmOptions)
        self.assertFalse(algo3 in options.algorithmOptions)

    def test_parseOptions_without_some_options(self):
        """Test parseOptions without specifying maxHits and minAccuracy."""
        # Test if maxHits and minAccuracy are not set,
        # whether both options.minAnchorSize and maxHits are None
        argumentList = ["--minAccuracy", "50"] + self.infiles + ["outfile.bam"]
        options = parseOptions(argumentList)
        self.assertIsNone(options.minAnchorSize)
        self.assertIsNone(options.maxHits)

    def test_importDefaultOptions(self):
        """Test importDefaultOptions"""
        options = Namespace(minAccuracy=10,
                            maxHits=12)
        defaultOptions = {"minAccuracy":30, "maxHits":14}
        newOptions, infoMsg = importDefaultOptions(options, defaultOptions)
        self.assertEqual(newOptions.minAccuracy,     10)
        self.assertEqual(newOptions.maxHits,         12)


if __name__ == "__main__":
    unittest.main()

