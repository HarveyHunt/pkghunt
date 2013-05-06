import sqlite3
import os.path
import logging


class Database:

    def __init__(self, databaseFile):
        # Only try to create the database if it doesn't exist.
        self.databaseFile = databaseFile
        if not os.path.isfile(self.databaseFile):
            cur = self.connect()
            command = """CREATE TABLE Packages(
            packageID INTEGER primary key autoincrement,
            packageName TEXT NOT NULL, size INTEGER, language TEXT,
            url TEXT, installPath TEXT, downloadPath TEXT,
            installedDate TEXT, version TEXT, favourite INTEGER)"""
            cur.execute(command)
            self.conn.commit()
            self.disconnect(cur)
            logging.warning("Created a new database.")

    def connect(self):
        # Create a connection to the database and return
        # the cursor for that connection.
        self.conn = sqlite3.connect(self.databaseFile)
        logging.debug("Connecting to database.")
        return self.conn.cursor()

    def disconnect(self, cur):
        # Disconnect the cursor that is passed in.
        logging.debug("Disconnecting from database.")
        cur.close()

    def addEntry(self, p):
        # A function to add an entry to the database.
        # It expects a list of values relating to a package
        # that it then iterates over.
        cur = self.connect()
        if not p[0]:
            raise ValueError('PackageName required.')
        command = "INSERT into Packages values (NULL, " + "?," * (len(p) - 1) + "?)"
        # The function that calls this is responsible for the capitalisation of words.
        cur.execute(command, [x for x in p])
        self.conn.commit()
        logging.debug("Adding the following package to the database: {0}".format(p[0]))
        # Return the last inserted ID, to allow the program to keep track of the
        # current index in the DB.
        # This is only really necessary for cleaning up after a unit test
        # and isn't utilised by the main program.
        lastId = cur.lastrowid
        self.disconnect(cur)
        return lastId

    def getPackageData(self, criteria):
        # Accepts search criteria passed to it by the utils.search function.
        # It then returns the matching criteria in the form of a tuple.
        cur = self.connect()
        packageID = criteria[0]
        packageName = criteria[1]
        language = criteria[2]
        size = criteria[3]
        # Store the list items in variables and then delete the list.
        # Fill the criteria list with the criteria used and then
        # execute it on the database.
        criteria = []
        if packageID is None:
            query = 'SELECT * FROM Packages WHERE packageName like ? and language like ?'
            # Remove packageID from the criteria. Allows for searching without preference
            # for packageID.
            criteria = [packageName, language]
        else:
            query = 'SELECT * FROM Packages WHERE packageID = ? and \
                packageName like ? and language like ?'
            criteria = [packageID, packageName, language]
        if size:
            if size.__contains__('>'):
                query += ' and size > ?'
                # Remove the signs from the size query.
                size = size.replace('>', '')
                criteria.append(size)
            elif size.__contains__('<'):
                query += ' and size < ?'
                size = size.replace('<', '')
                criteria.append(size)
            else:
                query += ' and size like ?'
                criteria.append(size)
        # A list comprehension to execute the query.
        # The percentage signs are wildcards.
        # Use a wildcard if the criteria is none, allow a string to be matched
        # with wildcards e.g. python matches to %python%, otherwise use the size
        # criteria
        cur.execute(query, ['%' if x is None else
                    '%' + x + '%' if not x.strip('><').isnumeric() else x for x in criteria])
        logging.debug("Fetching package data for the search"
                    "criteria: {0}".format(str(criteria)))
        results = cur.fetchall()
        self.disconnect(cur)
        return results

    def deletePackage(self, packageID):
        # Deletes a package from the database.
        # This is called as the last step in the deletion process
        # in case the deletion of files fails.
        cur = self.connect()
        cur.execute("DELETE FROM Packages WHERE packageID = ?", (packageID, ))
        logging.debug("Deleting the package with ID {0}".format(packageID))
        self.conn.commit()
        self.disconnect(cur)

    def editPackage(self, detailsList):
        # Avoiding the use of a dictionary to keep the input to this
        # function uniform to others. The unordered nature of a dictionary
        # could also cause issues, and it isn't worth creating a custom, ordered
        # dictionary.
        cur = self.connect()
        columns = ['packageName', 'size', 'language', 'url', 'installPath',
                'downloadPath', 'installedDate', 'version', 'favourite']
        # If the first instance isn't a list then this isn't a list of lists
        # and so should be treated accordingly.
        if not isinstance(detailsList[0], list):
            packageID = detailsList.pop(0)
            for n in range(0, len(detailsList)):
                if detailsList[n] is not None:
                    # Building my own query manually as I am sick of Sqlite3
                    # doing it so opaquely.
                    query = "UPDATE Packages SET {0} = \'{1}\' \
                            WHERE packageID = {2}".format(columns[n],
                                detailsList[n], packageID)
                    cur.execute(query)
        else:
            for newDetails in detailsList:
                # Remove the packageID from the list of details and assign it.
                # This makes it easier to recurse through a large list of
                # new details.
                packageID = newDetails.pop(0)
                for n in range(0, len(newDetails)):
                    if newDetails[n] is not None:
                        # Building my own query manually as I am sick of Sqlite3 doing it
                        # so opaquely.
                        query = "UPDATE Packages SET {0} = \'{1}\' \
                        WHERE packageID = {2}".format(columns[n], newDetails[n], packageID)
                        cur.execute(query)
        self.conn.commit()
        self.disconnect(cur)
