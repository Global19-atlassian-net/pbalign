
import unittest
import tempfile
import filecmp
import shutil
from os import path

from pbalign.pbalignfiles import PBAlignFiles

from test_setpath import ROOT_DIR

class Test_PbAlignFiles_Ecoli(unittest.TestCase):
    def setUp(self):
        self.rootDir = ROOT_DIR
        self.inputFileName    = path.join(self.rootDir, "data/ecoli.fasta")
        self.referencePath    = "/pbi/analysis/smrtportal/beta/userdata//references/Ecoli_K12_MG1655"
        self.targetFileName   = path.join(self.referencePath,
                                          "sequence/Ecoli_K12_MG1655.fasta")
        self.sawriterFileName = self.targetFileName + ".sa"
        self.OUT_DIR = tempfile.mkdtemp()
        self.outputFileName   = path.join(self.OUT_DIR, "tmp.sam")

    def tearDown(self):
        shutil.rmtree(self.OUT_DIR)

    def test_init(self):
        """Test PBAlignFiles.__init__() with a reference repository."""
        # Without region table
        p = PBAlignFiles(self.inputFileName,
                         self.referencePath,
                         self.outputFileName)
        self.assertTrue(filecmp.cmp(p.inputFileName, self.inputFileName))
        self.assertTrue(p.referencePath, path.abspath(path.expanduser(self.referencePath)))
        self.assertTrue(filecmp.cmp(p.targetFileName, self.targetFileName))
        self.assertTrue(filecmp.cmp(p.outputFileName, self.outputFileName))
        self.assertIsNone(p.regionTable)



class Test_PbAlignFiles(unittest.TestCase):
    def setUp(self):
        self.rootDir = ROOT_DIR
        self.inputFileName = path.join(self.rootDir, "data/lambda_bax.fofn")
        self.referenceFile = "/pbi/dept/secondary/siv/references/lambda/sequence/lambda.fasta"
        self.OUT_DIR = tempfile.mkdtemp()
        self.outputFileName = path.join(self.OUT_DIR, "tmp.sam")

    def tearDown(self):
        shutil.rmtree(self.OUT_DIR)

    def test_init(self):
        """Test PBAlignFiles.__init__()."""
        # Without region table
        p = PBAlignFiles(self.inputFileName,
                         self.referenceFile,
                         self.outputFileName)
        self.assertTrue(filecmp.cmp(p.inputFileName, self.inputFileName))
        self.assertTrue(filecmp.cmp(p.referencePath, self.referenceFile))
        self.assertTrue(filecmp.cmp(p.targetFileName, self.referenceFile))
        self.assertTrue(filecmp.cmp(p.outputFileName, self.outputFileName))
        self.assertIsNone(p.regionTable)

    def test_init_region_table(self):
        """Test PBAlignFiles.__init__() with a region table."""
        # With an artifical region table
        regionTable = path.join(self.rootDir, "data/lambda.rgn.h5")
        p = PBAlignFiles(self.inputFileName,
                         self.referenceFile,
                         self.outputFileName,
                         regionTable)
        self.assertTrue(filecmp.cmp(p.regionTable, regionTable))


    def test_setInOutFiles(self):
        """Test PBAlignFiles.SetInOutFiles()."""
        p = PBAlignFiles()
        self.assertIsNone(p.inputFileName)
        self.assertIsNone(p.outputFileName)
        self.assertIsNone(p.referencePath)

        p.SetInOutFiles(self.inputFileName,
                        self.referenceFile,
                        self.outputFileName,
                        None)
        self.assertTrue(filecmp.cmp(p.inputFileName, self.inputFileName))
        self.assertTrue(filecmp.cmp(p.referencePath, self.referenceFile))
        self.assertTrue(filecmp.cmp(p.targetFileName, self.referenceFile))
        self.assertTrue(filecmp.cmp(p.outputFileName, self.outputFileName))
        self.assertIsNone(p.regionTable)


if __name__ == "__main__":
    unittest.main()

