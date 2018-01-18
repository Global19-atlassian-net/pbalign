"""Test pbalign.util/fileutil.py"""
from __future__ import print_function

import tempfile
import unittest
import filecmp
import shutil
from os import path

from pbcore.io import DataSet

from pbalign.utils.fileutil import getFileFormat, \
    isValidInputFormat, isValidOutputFormat, getFilesFromFOFN, \
    checkInputFile, checkOutputFile, checkReferencePath, \
    real_upath, real_ppath, isExist

from test_setpath import ROOT_DIR, DATA_DIR


class Test_fileutil(unittest.TestCase):
    """Test pbalign.util/fileutil.py"""
    def setUp(self):
        self.rootDir = ROOT_DIR
        self.outDir = tempfile.mkdtemp()
        self.dataDir = path.join(DATA_DIR,
                                 "testLoadPulses/Analysis_Results/")

    def tearDown(self):
        shutil.rmtree(self.outDir)

    def test_isValidInputFormat(self):
        """Test isValidInputFormat()."""
        self.assertTrue(isValidInputFormat( getFileFormat("ab.fasta")) )
        self.assertTrue(isValidInputFormat( getFileFormat("ab.fa")) )
        self.assertTrue(isValidInputFormat( getFileFormat("ab.pls.h5")) )
        self.assertTrue(isValidInputFormat( getFileFormat("ab.plx.h5")) )
        self.assertTrue(isValidInputFormat( getFileFormat("ab.bas.h5")) )
        self.assertTrue(isValidInputFormat( getFileFormat("ab.bax.h5")) )
        self.assertTrue(isValidInputFormat( getFileFormat("ab.fofn")) )
        self.assertFalse(isValidInputFormat( getFileFormat("ab.sam")) )
        self.assertFalse(isValidInputFormat( getFileFormat("ab.cmp.h5")) )
        self.assertFalse(isValidInputFormat( getFileFormat("ab.xyz")) )

    def test_isValidOutputFormat(self):
        """Test isOutputFormat()."""
        self.assertFalse(isValidOutputFormat( getFileFormat("ab.fasta")) )
        self.assertFalse(isValidOutputFormat( getFileFormat("ab.fa")) )
        self.assertFalse(isValidOutputFormat( getFileFormat("ab.pls.h5")) )
        self.assertFalse(isValidOutputFormat( getFileFormat("ab.plx.h5")) )
        self.assertFalse(isValidOutputFormat( getFileFormat("ab.bas.h5")) )
        self.assertFalse(isValidOutputFormat( getFileFormat("ab.bax.h5")) )
        self.assertFalse(isValidOutputFormat( getFileFormat("ab.fofn")) )
        self.assertTrue(isValidOutputFormat( getFileFormat("ab.sam")) )
        self.assertTrue(isValidOutputFormat( getFileFormat("ab.cmp.h5")) )
        self.assertFalse(isValidOutputFormat( getFileFormat("ab.xyz")) )

    def test_getFilesFromFOFN(self):
        """Test getFilesFromFOFN()."""
        fofnFN = path.join(self.rootDir, "data/ecoli_lp.fofn")
        fns = [self.dataDir +
               "m121215_065521_richard_c100425710150000001823055001121371_s1_p0.pls.h5",
               self.dataDir +
               "m121215_065521_richard_c100425710150000001823055001121371_s2_p0.pls.h5"]
        self.assertEqual(fns, getFilesFromFOFN(fofnFN))

    def test_checkInputFile(self):
        """Test checkInputFile()."""
        fastaFN = path.join(self.rootDir,  "data/ecoli.fasta")
        plsFN = self.dataDir + \
                "m121215_065521_richard_c100425710150000001823055001121371_s1_p0.pls.h5"
        self.assertTrue(filecmp.cmp(fastaFN, checkInputFile(fastaFN)))
        self.assertTrue(filecmp.cmp(plsFN, checkInputFile(plsFN)))

        fofnFN = path.join(self.rootDir,  "data/ecoli_lp.fofn")
        self.assertTrue(filecmp.cmp(fofnFN, checkInputFile(fofnFN)))

        xmlFN = path.join(self.rootDir,  "data/subreads_dataset1.xml")
        ret = checkInputFile(xmlFN)
        self.assertTrue(ret.endswith('.xml'))
        fs = DataSet(ret).toExternalFiles()
        self.assertTrue(fs[0].endswith("m140905_042212_sidney_c100564852550000001823085912221377_s1_X0.1.subreads.bam"))
        self.assertTrue(fs[1].endswith("m130406_011850_42141_c100513442550000001823074308221310_s1_p0.1.subreads.bam"))


    def test_checkOutputFile(self):
        """Test checkOutputFile()."""
        samFN = path.join(self.outDir, "lambda_out.sam")
        cmpFN = path.join(self.outDir, "lambda_out.cmp.h5")
        self.assertTrue(filecmp.cmp(samFN, checkOutputFile(samFN)))
        self.assertTrue(filecmp.cmp(cmpFN, checkOutputFile(cmpFN)))

    def test_checkReferencePath(self):
        """Test checkReferencePath()."""
        refDir = "/pbi/analysis/smrtportal/beta/userdata/references"
        refPath = path.join(refDir, "lambda")
        refPath, refFastaOut, refSaOut, isWithinRepository, annotation = \
            checkReferencePath(refPath)
        self.assertTrue(filecmp.cmp(refFastaOut,
                                    path.join(refPath,
                                              "sequence/lambda.fasta")))
        self.assertTrue(filecmp.cmp(refSaOut,
                                    path.join(refPath,
                                              "sequence/lambda.fasta.sa")))
        self.assertTrue(isWithinRepository)

        refpath, refFastaOut, refSaOut, isWithinRepository, annotation = \
                checkReferencePath(refFastaOut)
        self.assertTrue(filecmp.cmp(refFastaOut,
                                    path.join(refPath,
                                              "sequence/lambda.fasta")))
        self.assertTrue(filecmp.cmp(refSaOut,
                                    path.join(refPath,
                                              "sequence/lambda.fasta.sa")))
        self.assertTrue(isWithinRepository)

        fastaFN = "{0}/data/ecoli.fasta".format(self.rootDir)

        refpath, refFastaOut, refSaOut, isWithinRepository, annotation = \
                checkReferencePath(fastaFN)
        self.assertTrue(filecmp.cmp(refpath, refFastaOut))
        self.assertIsNone(refSaOut)
        self.assertFalse(isWithinRepository)

        refPathWithAnnotation = path.join(DATA_DIR, "references/H1_6_Scal_6x/")
        _refPath, _refFaOut, _refSaOut, _isWithinRepository, annotation = \
            checkReferencePath(refPathWithAnnotation)
        self.assertEqual(path.abspath(annotation),
            path.abspath(path.join(refPathWithAnnotation,
            "annotations/H1_6_Scal_6x_adapters.gff")))

        xmlFN = path.join(self.rootDir,  "data/reference_lambda.xml")
        refpath, refFastaOut, refSaOut, isWithinRepository, annotation = \
                checkReferencePath(xmlFN)
        self.assertTrue(filecmp.cmp(refFastaOut,
            "/pbi/dept/secondary/siv/testdata/pbalign-unittest/data/lambda_ref.fasta"))

    def test_isExist(self):
        """Test isExist(ff)."""
        self.assertFalse(isExist(None))

    def test_realpath(self):
        """Test real_upath and real_ppath."""
        print(real_upath("ref with space"))
        self.assertTrue(real_upath("ref with space").endswith("ref\ with\ space"))
        self.assertTrue(real_upath("ref\ with\ space").endswith("ref\ with\ space"))
        self.assertTrue(real_ppath("ref with space").endswith("ref with space"))
        self.assertTrue(real_ppath("ref\ with\ space").endswith("ref with space"))


if __name__ == "__main__":
    unittest.main()

