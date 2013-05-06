import unittest
import tarfile
import os
from lib import targz


class TestTarGZFunctions(unittest.TestCase):
    def setUp(self):
        with open('tests/makefile', 'w') as makefile:
            makefile.write('MakeFile Test')
        
        with open('tests/setup.py', 'w') as setupFile:
            setupFile.write('version=\'1.0\'')
        
        with tarfile.open('tests/testPackage.tgz', 'w:gz') as tar:
            for name in ['makefile', 'setup.py']:
                tar.add('tests/' + name)
        
        self.tarFile = targz.TarGZ('tests/testPackage.tgz')
        
    def tearDown(self):
        for name in ['makefile', 'setup.py', 'testPackage.tgz']:
            os.remove('tests/' + name)
        
    def testGetProjectLanguage(self):
        self.assertEqual(self.tarFile.getProjectLanguage(), 'Python')
        
    def testGetPipValue(self):
        self.assertEqual(self.tarFile.getPipValue('version'), '1.0')
        
    def testGetFolderName(self):
    # Although tests/makefile/ isn't the folder, this is an acceptable result.
    # The targz library is designed to work with the Github tarfiles, which
    # have a different folder structure
        self.assertEqual(self.tarFile.getFolderName(), 'tests/')
        
    def testGetSetup(self):
        self.assertTrue(self.tarFile.getSetup())
        
    def testGetMakefile(self):
        self.assertTrue(self.tarFile.getMakefile())
        
    def testGetVersion(self):
        self.assertEqual(self.tarFile.getVersion(), '1.0')
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTarGZFunctions)
