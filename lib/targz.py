import tarfile
import os.path
import re
import logging
from collections import Counter

# Declare some constants
PYTHON = "Python"
C = "C"
CPP = "C++"


class TarGZ():
    # This is a class that handles everything to do with Tar Gz files.
    def __init__(self, filename):
        # Create a tgz file object at startup.
        self.filename = filename
        self.file = tarfile.open(self.filename, 'r')
        # The package directory is the filepath less the filename.
        self.packageDirectory = os.sep.join(filename.split(os.sep)[:-1])
        logging.debug("Initialised TarGZ class with the file {0}".format(self.file))

    def getProjectLanguage(self):
        # Returns the language of a downloaded package by working out which file extension
        # occurs most.
        counter = Counter()
        for name in self.file.getnames():
            if os.path.splitext(name)[1] != "":
                counter[os.path.splitext(name)[1]] += 1
        # We return 3 extensions, in case something such as .html
        # is the most common.
        extensions = counter.most_common(3)
        for ext in extensions:
            if ext[0] == '.py':
                return PYTHON
            elif ext[0] == '.cpp':
                return CPP
            elif ext[0] == '.c':
                return C

    def getPipValue(self, field):
        # Oh, the indenting!
        for member in self.file.getmembers():
            if os.path.split(member.name.lower())[-1] == "setup.py":
                setupFile = self.file.extractfile(member)
                for line in setupFile.readlines():
                    line = str(line)
                    if field in line.split("=")[0]:
                        value = line.split("=")[1]
                        pipValue = "".join([x for x in value if not x in ["\\", "n", "\'", ",", "\""]])
                        return pipValue

    def getFolderName(self):
        # Return the folder name of the file. This is
        # particularly important for the make utility
        # but is also used when deleting a package.
        return self.file.getnames()[0] + os.sep

    def extractPackage(self):
        # This extracts a package to the package directory,
        # as defined by the configuration file.
        self.file.extractall(self.packageDirectory)

    def getSetup(self):
        # This checks whether or not a tar gz file contains a setup.py
        # file, as required by pip.
        for name in self.file.getnames():
            if os.path.split(name)[-1].lower().__contains__('setup.py'):
                return True
        return False

    def getMakefile(self):
        # This function checks to see if a tar gz file contains
        # a make file.
        for name in self.file.getnames():
            if os.path.split(name)[-1].lower().__contains__('makefile'):
                return True
        return False

    def getVersion(self):
        # This function attempts to calculate the version of the package,
        # with mixed results.

        # If the package has a setup.py, then chances are that there is a
        # bit of version information in it that can be extracted.
        if self.getSetup():
            version = self.getPipValue("version")
            logging.debug("Calculated the version from the setup.py file.")
            if version:
                return version
        # Iterate through the members of the archive.
        for member in self.file.getmembers():
            # Split the members by the / seperator and then
            # check the filename using regular expressions.
            if re.compile(".*VERSION", re.IGNORECASE).match(os.path.split(
                                                member.name.upper())[-1]):
                # Extract only the version file for security reasons.
                versionFile = self.file.extractfile(member)
                # List comprehension to remove all aside from numbers and .
                # Neater than a regular expression.
                if versionFile:
                    versionNumber = "".join([x for x in str(versionFile.readline()) if x.isdigit() or x == "."])
                    logging.debug("Calculated the version from the version file.")
                    return versionNumber
