import urllib.request
import json
import time
import logging
import subprocess
import os
from lib import database
from lib import targz


# SearchCriteria is as follows: [packageID, packageName, github, language, size].
def search(localSearch, searchCriteria, databaseFile):
    # A search function that can search either github or a database.
    # It was planned that the search function would support searching
    # Launchpad, however, this hasn't happened due to limited time and
    # a very poor web API.
    if not searchCriteria:
        raise ValueError("No search criteria supplied.")
        logging.error("No search criteria supplied.")
    # Convert all strings to lowercase
    if searchCriteria[3]:
        searchCriteria[3] = searchCriteria[3].lower()
    if searchCriteria[1]:
        searchCriteria[1] = searchCriteria[1].lower()
    # Need to add in database stuff.
    if localSearch is True:
        db = database.Database(databaseFile)
        # Get rid of the GitHub field.
        searchCriteria.__delitem__(2)
        # The database class takes charge of the < or > symbols in
        # the size criteria.
        data = db.getPackageData(searchCriteria)
        logging.info("Completed a database search.")
        return data

    elif localSearch is False and searchCriteria[2] is True:
            # Criteria[1] refers to the packageName
            if not searchCriteria[1]:
                raise ValueError("No package name supplied.")
            # Delete the github and packageID fields.
            searchCriteria.__delitem__(0)
            # Github was originally stored at [2] but as packageID has been removed
            # the number is reduced.
            searchCriteria.__delitem__(1)
            url = 'https://api.github.com/legacy/repos/search/' + searchCriteria[0]
            response = urllib.request.urlopen(url)
            # Need some error checking here.
            jsonObject = json.loads(response.read().decode())
            jsonDict = jsonObject['repositories']
            results = []
            for item in jsonDict:
                # Each time criteria matches, add one to the matchCount.
                # If the matchCount == the number of criteria, the search result
                # must have matched to everything.
                # We can use the fact that Python considers True == 1 to add
                # 1 to the matchCount as opposed to lots of ifs.
                matchCount = 0
                matchCount += searchCriteria[0] in item['name']
                if item['language']:
                    matchCount += item['language'].lower() in searchCriteria[1]
                # The size criteria can have a greater/less than symbol in front of it.
                # e.g. >1232
                # This needs to be stripped before converting to an integer, hence the [1:].
                if searchCriteria[2] is not None:
                    if searchCriteria[2].__contains__('>'):
                        matchCount += item['size'] > int(searchCriteria[2][1:])
                    elif searchCriteria[2].__contains__('<'):
                        matchCount += item['size'] < int(searchCriteria[2][1:])
                    else:
                        matchCount += item['size'] == int(searchCriteria[2])
                searchCriteriaCount = 0
                # Calculate how many search criteria were used.
                # Check the data type of each item.
                for i in range(0, searchCriteria.__len__()):
                        searchCriteriaCount += searchCriteria[i] is not None
                if matchCount == searchCriteriaCount:
                    results.append(item)
            logging.info("Completed a github search.")
            return results


def downloadPackage(package, downloadPath, databaseFile, pipLogFile, waitTime, makeInstallLog, url=None):
    # This is a function to download and install a package. It takes care of adding
    # information to the database as well as allowing the user to install a package
    # using root permissions without the scary idea of running the entire program as
    # root.
    # This functions expects a list of package details, as returned by the search function.
    db = database.Database(databaseFile)
        # If a URL isn't supplied by the caller, then make one.
    downloadPath = downloadPath + package['name'] + '.tgz'
    if url is None:
        url = 'https://github.com/' + package['username'] + '/' + \
            package['name'] + '/tarball/master'
    installedPackages = search(True, [None, None, False, None, None], databaseFile)
    for item in installedPackages:
        if url in item:
            return [1, package['name']]
    urllib.request.urlretrieve(url, downloadPath)
    logging.debug("Downloading a package from {0} to {1}".format(url, downloadPath))
    tgz = targz.TarGZ(downloadPath)
    version = tgz.getVersion()
    if not package['language']:
        package['language'] = tgz.getProjectLanguage()
    p = [package['name'], package['size'], package['language'], url,
        None, downloadPath, time.ctime(), version, 0]
    db.addEntry(p)

    if package['language'] == 'Python':
        # If it contains a setup.py file, then pip can do the rest.
        if tgz.getSetup() is True:
            # The " needs to be escaped so that it is passed to the shell as single string.
            message = "\"Please check that the title of the terminal is a valid path name." \
                "The pip program will install the package and report any errors " \
                "both to the console and to the pip log file.\""
            try:
                command = ["xterm", "-T", "{0}".format(downloadPath), "-e",
                "./installer.sh {0} {1} {2} {3}".format(message, downloadPath, pipLogFile, waitTime)]
                ret = subprocess.call(command)
            except subprocess.CalledProcessError as e:
                logging.error(e)
            if ret == 0:
                logging.info("Installed a package using pip with the name {0}".format(package['name']))
            else:
                logging.error("Installation of the package {0} using pip has failed.".format(package['name']))
            return [ret, package['name']]
        else:
            logging.error("The python package {0} could not be installed due "
                 "to it containing no setup.py".format(package['name']))
            return [1, package['name']]
    elif package['language'] == "C" or package['language'] == "C++":
        tgz.extractPackage()
        # Remove the file name part of the download path and instead add
        # the folder name to the end.
        folderPath = os.sep.join(downloadPath.split(os.sep)[:-1] + [tgz.getFolderName()])
        # The " needs to be escaped so that it is passed to the shell as single string.
        message = "\"The package is going to be installed using the make utility.\""
        command = ["xterm", "-T", "Making {0}".format(folderPath), "-e",
        "./installer.sh {0} {1} {2} {3}".format(message, folderPath, makeInstallLog, waitTime)]
        try:
            ret = subprocess.call(command)
        except subprocess.CalledProcessError as e:
            logging.error(e)
        if ret == 0:
            logging.info("Installed a package using the make utility.")
        else:
            logging.error("Installation of the package {0} using the make utility had failed.".format(package['name']))
        return [ret, package['name']]
    else:
        logging.error("Unsupported language, installation has been abandoned.")
