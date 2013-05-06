import sys
import time
import os
import logging
import queue
import shutil
import subprocess
from PyQt4 import QtGui
from PyQt4 import QtCore
from ui import delete
from ui import edit
from ui import main
from ui import search
from ui import config
from lib.thread import DatabaseThread
from lib.thread import GenericThread
from lib import utils
from lib import configuration
from lib import database
from lib import targz


class MainProgram():
    def __init__(self):
        # Set up the main window and app.
        self.app = QtGui.QApplication(sys.argv)
        self.mainWindow = QtGui.QMainWindow()
        self.mainUi = main.Ui_MainWindow()
        self.mainUi.setupUi(self.mainWindow)
        # Set up the delete dialog.
        self.deleteDialog = QtGui.QDialog()
        self.deleteUi = delete.Ui_deleteDialog()
        self.deleteUi.setupUi(self.deleteDialog)
        self.deleteUi.buttonBox.accepted.connect(self.delete)
        # Set up the search dialog.
        self.searchDialog = QtGui.QDialog()
        self.searchUi = search.Ui_searchDialog()
        self.searchUi.setupUi(self.searchDialog)
        self.searchUi.buttonBox.accepted.connect(self.search)
        # Set up the edit dialog.
        self.editDialog = QtGui.QDialog()
        self.editUi = edit.Ui_editDialog()
        self.editUi.setupUi(self.editDialog)
        self.editUi.buttonBox.accepted.connect(self.edit)
        # Instantiate the config class.
        self.configuration = configuration.Config()
        # Set up the config dialog.
        self.configDialog = QtGui.QDialog()
        self.configUi = config.Ui_configDialog()
        self.configUi.setupUi(self.configDialog)
        self.configUi.buttonBox.accepted.connect(self.editConfig)
        # Time to connect the toolbar buttons.
        self.mainUi.actionDelete.activated.connect(self.showDelete)
        self.mainUi.actionSearch.activated.connect(self.searchDialog.show)
        self.mainUi.actionEdit.activated.connect(self.showEdit)
        self.mainUi.actionSave.activated.connect(self.updateData)
        self.mainUi.actionInstall.activated.connect(self.install)
        self.mainUi.actionPreferences.activated.connect(self.showConfig)
        self.mainUi.actionRefresh.activated.connect(self.refreshMainTable)
        self.threadPool = []
        self.db = database.Database(self.configuration.databaseFile)
        self.q = queue.Queue()
        # Prompt the user to install missing favourite packages.
        self.getFavourites()
        # Turn off logging if selected, by setting the handler to
        # a null one.
        # Logging data is still outputted to the terminal though.
        if self.configuration.loggingLevel == 0:
            handler = logging.NullHandler()
        else:
            handler = logging.FileHandler(self.configuration.logFile)
        logger = logging.getLogger()
        logger.addHandler(handler)
        # Create a custom logger with nice formatting.
        formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(filename)s - %(funcName)s - %(message)s',
                                       datefmt='%d/%m/%Y %I:%M:%S %p')
        # The logger will have two handlers, a stream handler for outputting to console
        # and either a File Handler or Null Handler, dependant on config.
        # If the user doesn't want the log to be output to console, the stream handler must be detatched from
        # the logger.
        for handler in logger.handlers:
            handler.setFormatter(formatter)
        # If the logToConsole is set to 2 then it should be logged.
        # Otherwise, remove the stream handler from the logger.
        # The stream handler can be accessed from logger.handlers[0].
        if self.configuration.logToConsole != 2:
            logger.removeHandler(logger.handlers[0])
        # The logging levels are defined with numerical values. They are as follows:
        # DEBUG = 10
        # INFO = 20
        # WARNING = 30
        # ERROR = 40
        # CRITICAL = 50
        # By multiplying the item box index of the config ui by 10,
        # it is possible to arrive at these values.
        logger.setLevel(self.configuration.loggingLevel * 10)
        handler.setLevel(self.configuration.loggingLevel * 10)

    def __del__(self):
        # The pseudo destructor that runs when the main
        # program instance is deleted.
        self.setFavouritesToFile()
        logging.debug("Main Window object being destroyed.")

    def run(self):
        # The main loop of the application.
        self.refreshMainTable()
        self.mainWindow.show()
        sys.exit(self.app.exec_())

    def getSelectedRows(self):
        # A helper function to get the row numbers of the selected rows.
        rows = []
        for item in self.mainUi.tableWidget.selectedIndexes():
            rows.append(item.row())
        # Remove the duplicate rows with the use of a set.
        rows = set(rows)
        return rows

    def install(self, favourites=None):
        # If the function is called with a list of favourites passed in, it
        # needs to download the favourite packages. The favourites are passed
        # as a list format [[details], url]
        if favourites:
            numberOfDownloads = len(favourites)
            for favourite in favourites:
                self.q.put((favourite[0], self.configuration.downloadPath,
                            self.configuration.databaseFile, self.configuration.pipLogFile,
                            self.configuration.terminalWaitTime,
                            self.configuration.makeLogFile, favourite[1]))
                self.threadPool.append(GenericThread(utils.downloadPackage, self.q))
                self.threadPool[-1].start()
        else:
            rows = self.getSelectedRows()
            numberOfDownloads = len(rows)
            for row in rows:
                # This means that the package is installed as it has a package ID.
                if self.mainUi.tableWidget.item(row, 0).text() != '':
                    QtGui.QMessageBox.warning(self.mainWindow, "Warning",
                        "You can't install a package that is already installed.")
                    logging.error('The user attempted to install an already installed'
                    ' package.')
                    return
                else:
                    # Add the arguments on the queue and then create a thread that is
                    # passed the function and queue.
                    self.q.put((self.results[row], self.configuration.downloadPath,
                                self.configuration.databaseFile, self.configuration.pipLogFile,
                                self.configuration.terminalWaitTime, self.configuration.makeLogFile))
                    self.threadPool.append(GenericThread(utils.downloadPackage, self.q))
                    self.threadPool[-1].start()
        logging.debug("Installing {0} packages.".format(numberOfDownloads))
        # Iterate through all of the downloads and grab the data the download
        # threads have placed back on the queue.
        for i in range(numberOfDownloads):
            ret = self.q.get()
            logging.debug(ret)
            # Following a C style convention- if the return value is
            # 1, then something has gone wrong.
            if ret[0] == 1:
                QtGui.QMessageBox.critical(self.mainWindow, "Error", "Installation of package {0} has failed.\n" \
                "Check log for details".format(ret[1]))
            else:
                self.mainUi.statusbar.showMessage("Installed package {0} of {1}".format(i, numberOfDownloads))
            # ret[-1] is the thread that is returned.
            ret[-1].deleteLater()
            self.threadPool.remove(ret[-1])

    def showConfig(self):
        # Grab the current config settings from the config object and display them.
        # This will be easy to expand on in the future as more config settings get
        # added.
        self.configUi.textFavouritesFile.setText(str(self.configuration.favouritesFile))
        self.configUi.textDatabaseFile.setText(self.configuration.databaseFile)
        self.configUi.textDownloadPath.setText(self.configuration.downloadPath)
        self.configUi.textLogFile.setText(self.configuration.logFile)
        self.configUi.textMakeLogFile.setText(self.configuration.makeLogFile)
        self.configUi.comboBoxLogging.setCurrentIndex(self.configuration.loggingLevel)
        self.configUi.checkBoxLogToConsole.setCheckState(self.configuration.logToConsole)
        self.configUi.textPipLogFile.setText(self.configuration.pipLogFile)
        self.configUi.textTerminalWaitTime.setText(self.configuration.terminalWaitTime)
        logging.info("Configuration dialog being displayed.")
        self.configDialog.show()

    def editConfig(self):
        # Grab the values from the text boxes and assign them to the
        # member variables. The actual writing to the config file is taken
        # care of by the class in its destructor.
        self.configuration.favouritesFile = self.configUi.textFavouritesFile.text()
        self.configuration.databaseFile = self.configUi.textDatabaseFile.text()
        self.configuration.downloadPath = self.configUi.textDownloadPath.text()
        self.configuration.logFile = self.configUi.textLogFile.text()
        self.configuration.makeLogFile = self.configUi.textMakeLogFile.text()
        self.configuration.loggingLevel = self.configUi.comboBoxLogging.currentIndex()
        self.configuration.logToConsole = self.configUi.checkBoxLogToConsole.checkState()
        self.configuration.pipLogFile = self.configUi.textPipLogFile.text()
        self.configuration.terminalWaitTime = self.configUi.textTerminalWaitTime.text()
        logging.debug("Updating configuration member variables.")

    def showDelete(self):
        # Displays the delete dialog and populates the table.
        # First, the selected rows are gathered and then they
        # are assigned to the delete dialog table.
        rows = self.getSelectedRows()
        if len(rows) == 0:
            QtGui.QMessageBox.warning(self.mainWindow, "Warning", "No package selected.")
            logging.error('The user tried to delete without selecting a package.')
            return
        # I have made this a member variable as it will be used when the application
        # actually comes around to deleting stuff.
        self.deleteTableData = []
        for row in rows:
            rowData = []
            for column in range(0, self.mainUi.tableWidget.columnCount()):
                rowData.append(self.mainUi.tableWidget.item(row, column).text())
            self.deleteTableData.append(rowData)
        self.deleteUi.tableDelete.setRowCount(len(self.deleteTableData))
        for row in range(0, len(self.deleteTableData)):
            for column in range(0, self.deleteUi.tableDelete.columnCount()):
                self.deleteUi.tableDelete.setItem(row, column, QtGui.QTableWidgetItem("{0}".format(self.deleteTableData[row][column])))
        logging.info("Deletion dialog being displayed.")
        self.deleteDialog.show()

    def showEdit(self):
        # Displays the edit screen and populates all of the fields with
        # the values that are stored in the database.
        row = self.getSelectedRows()
        if len(row) > 1:
            QtGui.QMessageBox.warning(self.mainWindow, "Warning", "You can't edit more than one package at a time.")
            return
        elif len(row) == 0:
            QtGui.QMessageBox.warning(self.mainWindow, "Warning", "You can't edit a package without selecting one.")
            return
        # After checking the length of the set returned by the function,
        # we can be sure it is only one element long and so remove the set.
        row = row.pop()
        # Grab the packageId from the table in order to later query
        # the database.
        # I am making it a member variable as it will need to be accessed by the
        # edit function later.
        self.editPackageId = self.mainUi.tableWidget.item(row, 1).text()
        if self.editPackageId == None:
            QtGui.QMessageBox.warning(self.mainWindow, "Warning", "You can't edit a package that isn't installed.")
            return
        packageData = utils.search(True, [self.editPackageId, None, False, None, None], self.configuration.databaseFile)
        # Package data is a one element list, so get rid of the list.
        packageData = packageData[0]
        # Now set each text box to the value from the database.
        if packageData[9] == 1:
            self.editUi.checkBoxFavourite.setChecked(True)
        else:
            self.editUi.checkBoxFavourite.setChecked(False)
        self.editUi.textPackageName.setText(packageData[1])
        self.editUi.textLanguage.setText(packageData[3])
        self.editUi.textVersion.setText(packageData[8])
        self.editUi.textSize.setText(str(packageData[2]))
        self.editUi.textDownloadPath.setText(packageData[6])
        self.editUi.textInstallPath.setText(packageData[5])
        self.editUi.textURL.setText(packageData[4])
        self.editUi.textInstalledDate.setText(packageData[7])
        logging.info("Editing dialog being displayed.")
        self.editDialog.show()

    def edit(self):
        # Grabs the data from the edit dialog's fields and adds it to the
        # database in a multithreaded manner.
        newDetails = []
        newDetails.append(self.editPackageId)
        newDetails.append(self.editUi.textPackageName.text())
        newDetails.append(self.editUi.textSize.text())
        newDetails.append(self.editUi.textLanguage.text())
        newDetails.append(self.editUi.textURL.text())
        newDetails.append(self.editUi.textInstallPath.text())
        newDetails.append(self.editUi.textDownloadPath.text())
        newDetails.append(self.editUi.textInstalledDate.text())
        newDetails.append(self.editUi.textVersion.text())
        # Determine whether the package is a favourite or not.
        if self.editUi.checkBoxFavourite.checkState() == 2:
            newDetails.append(1)
        else:
            newDetails.append(0)
        logging.debug(newDetails)
        # Add a tuple onto the queue and pass it to the thread.
        # Tuple expansion will take place in the thread and arrange
        # the arguments correctly.
        self.q.put((self.configuration.databaseFile, newDetails))
        self.threadPool.append(DatabaseThread("editPackage", self.q))
        logging.debug(str(self.threadPool[-1]) + '  |  ' + str(len(self.threadPool)))
        self.threadPool[-1].start()
        # The thread returns itself so that it can be removed from the threapool.
        # This doesn't matter here as we know that the last item on the thread pool will be
        # the thread we created, so it can be popped.
        self.q.get()
        self.threadPool.pop()
        self.refreshMainTable()

    def getFavourites(self):
        # This function reads from the favourites file the packages that are to be installed.
        # It then queries the database for all of the already installed packages and compares.
        # If the URL of a favourite package matches one that is already installed, then the
        # favourites is already there, otherwise it needs to be installed.
        # The URL is the only unique data about a package that can be compared with a
        # package that isn't installed.
        packagesToBeInstalled = []
        if os.path.exists(self.configuration.favouritesFile):
            # The favourites file contains the URLs of the favourited packages.
            with open(self.configuration.favouritesFile, "r") as file:
                favourites = file.readlines()
            logging.debug("Read the favourites file.")
            # Grab all of the installed packages.
            installedPackages = utils.search(True, [None, None, False, None, None], self.configuration.databaseFile)
            for favourite in favourites:
                # A flag that determines whether a package is installed or not.
                # It is set to false until proven true.
                installed = False
                # Split the line into 3 variables in order to pass them to the download function.
                details = {}
                url, details['language'], details['size'] = favourite.split()
                # The name of the package can be extracted from the URL and will need
                # to be passed to the download function.
                details['name'] = url.split('/')[-3]
                for package in installedPackages:
                    # If the URLs match, it is installed.
                    if url in package:
                        installed = True
                if not installed:
                    logging.warning("The favourite package {0} is not installed".format(details['name']))
                    # Show a message box to let the user decide if they want to install it.
                    reply = QtGui.QMessageBox.question(self.mainWindow, 'Message',
                                                       "The package {0} is not installed but is marked as a favourite. " \
                                                       "Do you wish to install it now?".format(details['name']),
                                                       QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        packagesToBeInstalled.append([details, url])
            self.install(packagesToBeInstalled)

    def setFavouritesToFile(self):
        # This function queries the database for all the packages and looks for those
        # that are favourited. It then adds the URL, language and size of the package
        # to the favourites file.

        # Query the database for all installed packages so that they can be
        # iterated through in order to check if the are favourites.
        installedPackages = utils.search(True, [None, None, False, None, None], self.configuration.databaseFile)
        favourites = []
        for package in installedPackages:
            # If the favourite field of the package is set to 1, it is a favourite
            # and can be later written to the favourites file.
            if package[9] == 1:
                # The URL, then language and finally size of the package is added to the favourites.
                # The 3 values are seperated by a tab so they can easily be split later.
                # Using a config parser style class would be too restrictive.
                favourites.append(str(package[4]) + '\t' + str(package[3]) + '\t' + str(package[2]) + '\n')
        f = open(self.configuration.favouritesFile, "w")
        for item in favourites:
            f.write(item)
        f.close()
        logging.debug("Updated the favourites file.")

    def delete(self):
        # This function iterates through the values in the member variable
        # deleteTableData. It then checks if the check box for removing downloaded
        # is checked. If so, it deletes the extract folder (if it exists), then the
        # tar.gz file and finally removes it from the database.
        deletedPackages = 0
        numberOfPackages = len(self.deleteTableData)
        for item in self.deleteTableData:
            # Item[1] refers to the package ID.
            if item[1] != '':
                # Query the database to find out where the package is downloaded to.
                # The return value is a one element list with a tuple.
                # Use [0] to get the first element (the tuple) and then use
                # [6] to get the install path.
                downloadPath = utils.search(True, [item[1], None, False, None, None], self.configuration.databaseFile)[0][6]
                tgz = targz.TarGZ(downloadPath)
                # If the tar file has a setup.py, it must be a python file.
                if tgz.getSetup():
                    # Extract from the setup.py the name with which the package
                    # was installed using. Then run a command to uninstall it.
                    name = tgz.getPipValue("name")
                    command = ["xterm", "-T", "Uninstalling {0}".format(name), "-e",
                    "sudo pip uninstall {0} --log={1}; sleep {2}".format(name,
                    self.configuration.pipLogFile, self.configuration.terminalWaitTime)]
                    try:
                        subprocess.call(command)
                    except subprocess.CalledProcessError as e:
                        logging.error(e)

                if self.deleteUi.boxRemoveDownloadedContent.checkState() == 2:
                    folderPath = os.sep.join(downloadPath.split(os.sep)[:-1] + [tgz.getFolderName()])
                    if os.path.exists(folderPath):
                        shutil.rmtree(folderPath)
                    os.remove(downloadPath)
                    logging.debug("Deleted the file {0}".format(downloadPath))
                logging.info("Deleting package with ID {0}".format(item[1]))
                self.db.deletePackage(item[1])
                deletedPackages += 1
                self.mainUi.statusbar.showMessage("Deleted package {0} of {1}".format(deletedPackages, numberOfPackages))
            else:
                QtGui.QMessageBox.warning(self.mainWindow, "Warning", "You can't delete a package that isn't installed.")
                logging.error("User tried to delete a package that isn't installed.")
                return
        self.refreshMainTable()

    def search(self):
        # Begins a search of either Github or the database.
        # Searching github can take a long time and multithreading could be useful here.
        # But I haven't implemented it as there is nothing the user would want to do
        # during a search anyway.
        self.mainUi.statusbar.showMessage("Searching")
        startTime = time.time()
        packageID = self.searchUi.textPackageID.text()
        if packageID == '':
            packageID = None
        packageName = self.searchUi.textPackageName.text()
        if packageName == '':
            packageName = None
        language = self.searchUi.textLanguage.text()
        if language == '':
            language = None
        size = self.searchUi.textSize.text()
        if size == '':
            size = None
        elif not size.strip('<>').isnumeric():
            QtGui.QMessageBox.warning(self.mainWindow, 'Warning', 'The size criteria can\'t contains letters. '
                'The application will remove the letters and attempt the search.')
            logging.error('The user attempted to search using letters in the size criteria.')
            size = ''.join([x for x in self.searchUi.textSize.text() if x in '1234567890<>'])
            
        if self.searchUi.checkBoxGithub.checkState() == 2 and packageName == None:
            self.mainUi.statusbar.showMessage("Search Failed")
            QtGui.QMessageBox.warning(self.mainWindow, "Warning", "You can't search Github without a package name.")
            logging.error("The user attempted to search Github without a package name.")
            return
        elif self.searchUi.checkBoxDatabase.checkState() == 2:
            self.app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            # Made results a member variable as I am going to only use parts of the result
            # to display in the table. Other parts of the results are vital but would end with
            # this function if it weren't for making this a member variable.
            self.results = utils.search(True, [packageID, packageName, False, language, size], self.configuration.databaseFile)
        elif self.searchUi.checkBoxGithub.checkState() == 2:
            self.app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            # Perform a search of Github.
            self.results = utils.search(False, [packageID, packageName, True, language, size], None)
        else:
            self.mainUi.statusbar.showMessage("Search Failed")
            QtGui.QMessageBox.warning(self.mainWindow, "Warning", "No search target entered.")
            logging.error("The user attempted to search without a target.")
            return
        duration = time.time() - startTime
        self.mainUi.statusbar.showMessage("Search completed in {0:.3f} seconds".format(duration))
        logging.info("The search completed in {0:.3f} seconds".format(duration))
        self.populateTable(self.mainUi.tableWidget, self.results)
        self.app.restoreOverrideCursor()

    def refreshMainTable(self):
        # Refresh the values in the table. This can be slightly buggy
        # and I have therefore added a button in the UI for the user
        # to force a refresh.
        logging.info("Refreshing the main window.")
        self.populateTable(self.mainUi.tableWidget, utils.search(True, [None, None, False, None, None],
                                                                 self.configuration.databaseFile))

    def updateData(self):
        # This function writes the table data from the UI back into the database
        # in order to allow the user to edit data without the use of the edit dialog.
        # Loop through all of the rows so that they can all be written to the
        # database. I believe this is the "Scattergun" approach but will
        # work well for only a small local database.
        newDetails = []
        if self.mainUi.tableWidget.rowCount() == 0:
            logging.error("User tried to save an empty package list.")
            QtGui.QMessageBox.warning(self.mainWindow, "Warning", "You can't save an empty package list.")
            return
        if self.mainUi.tableWidget.rowCount() == 1:
            data = []
            for column in range(0, self.mainUi.tableWidget.columnCount()):
                data.append(self.mainUi.tableWidget.item(0, column).text())
            newDetails = [data[1], data[2], data[3], data[4], None, None, None, data[5], None, data[0]]
        else:
            for row in range(0, self.mainUi.tableWidget.rowCount()):
                data = []
                # Loop through the columns of the database and grab all the item's data.
                for column in range(0, self.mainUi.tableWidget.columnCount()):
                    data.append(self.mainUi.tableWidget.item(row, column).text())
                listArgs = [data[1], data[2], data[3], data[4], None, None, None, data[5], None, data[0]]
                newDetails.append(listArgs)
        self.q.put((self.configuration.databaseFile, newDetails))
        self.threadPool.append(DatabaseThread("editPackage", self.q))
        logging.debug(str(self.threadPool[-1]) + '  |  ' + str(len(self.threadPool)))
        self.threadPool[-1].start()
        logging.debug("Updated the database.")
        self.q.get()
        self.threadPool.pop()

    def populateTable(self, table, data):
        # This functions accepts a table object and a list of data that needs to
        # be displayed. It then decides whether the data is from a local search
        # or github and displays it differently accordingly.
        table.setColumnCount(6)
        table.setRowCount(data.__len__())
        for i in range(0, data.__len__()):
            # A little hack to create a database like view.
            # Reordering the data and silently dropping the stuff
            # that isn't needed.
            if isinstance(data[i], tuple):
                data[i] = (data[i][9], data[i][0], data[i][1], data[i][2],
                data[i][3], data[i][7])
                for j in range(0, table.columnCount()):
                    table.setItem(i, j, QtGui.QTableWidgetItem("{0}".format(data[i][j])))
            # If it is a dictionary it has been returned by a github search
            # and must be ordered before being put into the table.
            elif isinstance(data[i], dict):
                # Only fill out the stuff we know.
                table.setItem(i, 0, QtGui.QTableWidgetItem("{0}".format('')))
                table.setItem(i, 1, QtGui.QTableWidgetItem("{0}".format('')))
                table.setItem(i, 2, QtGui.QTableWidgetItem("{0}".format(data[i]['name'])))
                table.setItem(i, 3, QtGui.QTableWidgetItem("{0}".format(data[i]['size'])))
                table.setItem(i, 4, QtGui.QTableWidgetItem("{0}".format(data[i]['language'])))
