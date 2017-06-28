from pbalign.utils.fileutil import ReferenceInfo
import unittest

class Test_ReferenceInfo(unittest.TestCase):

    def test_init(self):
        """Test ReferenceInfo.__init__() with a valid reference.info.xml."""
        rootDir = "/pbi/analysis/smrtportal/beta/userdata/references/lambda/"
        r = ReferenceInfo(rootDir + "reference.info.xml")
        self.assertEqual(r.refFastaFile, rootDir + "sequence/lambda.fasta")
        self.assertEqual(r.refSawriterFile, rootDir + "sequence/lambda.fasta.sa")

    def test_init_with_errors(self):
        with self.assertRaises(ValueError) as cm:
            r2 = ReferenceInfo("noexist.txt")

        with self.assertRaises(IOError) as cm:
            r2 = ReferenceInfo("noexist.xml")

if __name__ == "__main__":
    unittest.main()
