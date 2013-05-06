#!/usr/bin/python3
import argparse
import unittest
import logging
from tests import searchTest
from tests import dbTest
from tests import tgzTest
from lib import gui

def main():
    # A simple function to run the main program and parse any input in
    # case the user wishes to try tests.
    parser = argparse.ArgumentParser(description =
    'A lightweight package manager written in Python 3 that is designed to deal with source code.')

    parser.add_argument('-t', '--test', help = 'Run test scripts',
    type = str)

    args = parser.parse_args()

    if args.test:
        if args.test == 'searchTest':
            logging.info("Beginning search unit test.")
            suite = unittest.TestLoader().loadTestsFromTestCase(searchTest.TestSearchFunctions)
        elif args.test == 'tgzTest':
            logging.info("Beginning targz unit test.")
            suite = unittest.TestLoader().loadTestsFromTestCase(tgzTest.TestTarGZFunctions)
        elif args.test == 'dbTest':
            logging.info("Beginning database unit test.")
            suite = unittest.TestLoader().loadTestsFromTestCase(dbTest.TestDatabaseFunctions)
        else:
            return False
        unittest.TextTestRunner(verbosity=5).run(suite)
    else:
        program = gui.MainProgram()
        program.run()

if __name__ == '__main__':
    logging.info("Application started.")
    main()

