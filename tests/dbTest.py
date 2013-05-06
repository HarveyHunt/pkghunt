from lib import database
from lib import configuration
import unittest
import time

class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        self.configuration = configuration.Config()
        self.db = database.Database(self.configuration.databaseFile)
        self.newPackages = [['New Package 1', 123, 'Python', 'www.testurl.co.uk',
                              '/install/path', '/download/path', time.ctime(), '1.2', 1],
                            ['New Package 2', 534, 'C', 'www.testurl.co.uk',
                             '/install/path', '/download/path', time.ctime(), '2.3a', 0],
                            ['New Package 3', 12343, 'C++', 'www.testurl.co.uk',
                             '/install/path', '/download/path', time.ctime(), '12.1a', 1],
                            ['Python Package', 212, 'Python', 'www.testurl.co.uk',
                             '/install/path', '/download/path', time.ctime(), '12.31', 0]]

    def getIDRange(self):
        # A nasty hack to find the initial package ID and allow the
        # test to iterate over all of them.
        items = self.db.getPackageData([None, None, None, None])
        firstID = items[0][0]
        return range(firstID, firstID + items.__len__())

    def testAddEntry(self):
        for item in self.newPackages:
            self.assertRaises(self.db.addEntry(item))

    def testAddEntryNoData(self):
        self.assertRaises(ValueError, self.db.addEntry,
        [None, None, None, None, None, None, None, None, None, None])

    def testEditPackage(self):
        for i in self.getIDRange():
            self.assertRaises(self.db.editPackage([i, 'Edited',
                None, None, None, None, None, None, None]))
                
    def testRemovePackage(self):
        for i in self.getIDRange():
            self.assertRaises(self.db.deletePackage(i))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabaseFunctions)

