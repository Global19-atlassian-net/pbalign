"""Test pbalign.forquiverservice.repack."""
from __future__ import print_function
import unittest
from os import path, remove
from shutil import copyfile
from pbalign.forquiverservice.repack import RepackService
from tempfile import mkstemp
from test_setpath import DATA_DIR


class Test_RepackService(unittest.TestCase):
    """Test pbalign.forquiverservice.repack."""
    def setUp(self):
        """Set up the tests."""
        self.inCmpFile = path.join(DATA_DIR, "testrepack.cmp.h5")
        self.outCmpFile = mkstemp(suffix=".cmp.h5")[1]
        self.tmpCmpFile = self.outCmpFile + ".tmp"

        copyfile(self.inCmpFile, self.outCmpFile)
        self.options = {}
        self.obj = RepackService(self.outCmpFile, self.tmpCmpFile)

    def tearDown(self):
        remove(self.outCmpFile)

    def test_run(self):
        """Test LoadPulsesService.__init__()."""
        print(self.obj.cmd)
        _output, errCode, _errMsg = self.obj.run()
        self.assertEqual(errCode, 0)

if __name__ == "__main__":
    unittest.main()
