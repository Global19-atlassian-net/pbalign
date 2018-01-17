"""Test pbalign.forquiverservice.sort."""
from __future__ import print_function
import unittest
from os import path, remove
from shutil import copyfile
from pbalign.forquiverservice.sort import SortService
from tempfile import mkstemp
from test_setpath import DATA_DIR


class Opt(object):
    """Simulate pbalign options."""
    def __init__(self):
        """Option class."""
        self.verbosity = 2

class Test_SortService(unittest.TestCase):
    """Test pbalign.forquiverservice.sort."""
    def setUp(self):
        """Set up tests."""
        self.inCmpFile = path.join(DATA_DIR, "testsort.cmp.h5")
        self.outCmpFile = mkstemp(suffix=".cmp.h5")[1]

        copyfile(self.inCmpFile, self.outCmpFile)
        self.options = Opt()
        self.obj = SortService(self.outCmpFile, self.options)

    def tearDown(self):
        remove(self.outCmpFile)

    def test_run(self):
        """Test SortService.__init__()."""
        print(self.obj.cmd)
        _output, errCode, _errMsg = self.obj.run()
        self.assertEqual(errCode, 0)

if __name__ == "__main__":
    unittest.main()
