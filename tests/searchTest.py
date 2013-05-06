from lib.utils import search
from lib import database
from lib import configuration
import unittest
import random
import time

class TestSearchFunctions(unittest.TestCase):

    def setUp(self):
        # Load the configuration.
        self.configuration = configuration.Config()
        self.validSearchTerms = [[None, 'Python', True, None, None],
        [None, 'Python', True, None, None],
        [None, 'Python', True, 'Python', None],
        [None, 'Python', True, 'Python', None],
        [None, 'Python', True, 'Python', '>100'],
        [None, 'Python', True, 'Python', '>100'],
        [None, 'linux', True, None, None],
        [None, 'linux', True, None, None],
        [None, 'linux', True, 'C', None],
        [None, 'linux', True, 'C', None],
        [None, 'linux', True, 'C', '>100'],
        [None, 'linux', True, 'C', '>100']]

        # Some test data to be added to the database to allow the testing of the search functions.

        self.dbPackages = [['Python', 1235, 'Python', 'TESTURL', 'INSTALLPATH', 'DOWNLOADPATH',
                    time.ctime(), '1.2', True],
                    ['Python', 12, 'Python', 'TESTURL', 'INSTALLPATH', 'DOWNLOADPATH',
                    time.ctime(), '1.2a', False],
                    ['linux', 1235, 'Python', 'TESTURL', 'INSTALLPATH', 'DOWNLOADPATH',
                    time.ctime(), '1.2', True],
                    ['linux', 1235, 'c', 'TESTURL', 'INSTALLPATH', 'DOWNLOADPATH',
                    time.ctime(), '11.342', False],
                    ['linux', 1235, 'C', 'TESTURL', 'INSTALLPATH', 'DOWNLOADPATH',
                    time.ctime(), '1', True]]

        # A list of the package IDs in the DB.
        # Will be used in the teardown procedure.
        self.ids = []
        # Add the test data to the DB.
        self.db = database.Database(self.configuration.databaseFile)
        for item in self.dbPackages:
            self.ids.append(self.db.addEntry(item))

    def tearDown(self):
        for id in self.ids:
            self.db.deletePackage(id)

    def testNoPackageNameGithub(self):
        self.assertRaises(ValueError, search, False,
        [None, None, True, 'Python', '>12'], self.configuration.databaseFile)

    def testNoSearchCriteriaLocal(self):
        self.assertRaises(ValueError, search, True, None,
                            self.configuration.databaseFile)

    def testNoSearchCriteriaGithub(self):
        self.assertRaises(ValueError, search, False, None,
                            self.configuration.databaseFile)

    def testSearchGithub(self):
        # Only send one request, to stop my IP from being banned  :(
        term = random.choice(self.validSearchTerms)
        result = search(False, term, self.configuration.databaseFile)
        self.assertIsNotNone(result)

    def testSearchDatabase(self):
        for item in self.validSearchTerms:
            result = search(True, item, self.configuration.databaseFile)
            self.assertIsNotNone(result)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSearchFunctions)

