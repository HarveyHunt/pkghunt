# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config.ui'
#
# Created: Mon Mar 18 16:13:58 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_configDialog(object):
    def setupUi(self, configDialog):
        configDialog.setObjectName(_fromUtf8("configDialog"))
        configDialog.resize(563, 378)
        self.gridLayout = QtGui.QGridLayout(configDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelFavouritesFile = QtGui.QLabel(configDialog)
        self.labelFavouritesFile.setObjectName(_fromUtf8("labelFavouritesFile"))
        self.gridLayout.addWidget(self.labelFavouritesFile, 0, 1, 1, 1)
        self.textFavouritesFile = QtGui.QLineEdit(configDialog)
        self.textFavouritesFile.setObjectName(_fromUtf8("textFavouritesFile"))
        self.gridLayout.addWidget(self.textFavouritesFile, 0, 2, 1, 1)
        self.labelDownloadPath = QtGui.QLabel(configDialog)
        self.labelDownloadPath.setObjectName(_fromUtf8("labelDownloadPath"))
        self.gridLayout.addWidget(self.labelDownloadPath, 2, 1, 1, 1)
        self.textDatabaseFile = QtGui.QLineEdit(configDialog)
        self.textDatabaseFile.setObjectName(_fromUtf8("textDatabaseFile"))
        self.gridLayout.addWidget(self.textDatabaseFile, 1, 2, 1, 1)
        self.textDownloadPath = QtGui.QLineEdit(configDialog)
        self.textDownloadPath.setObjectName(_fromUtf8("textDownloadPath"))
        self.gridLayout.addWidget(self.textDownloadPath, 2, 2, 1, 1)
        self.labelDatabaseFile = QtGui.QLabel(configDialog)
        self.labelDatabaseFile.setObjectName(_fromUtf8("labelDatabaseFile"))
        self.gridLayout.addWidget(self.labelDatabaseFile, 1, 1, 1, 1)
        self.comboBoxLogging = QtGui.QComboBox(configDialog)
        self.comboBoxLogging.setObjectName(_fromUtf8("comboBoxLogging"))
        self.comboBoxLogging.addItem(_fromUtf8(""))
        self.comboBoxLogging.addItem(_fromUtf8(""))
        self.comboBoxLogging.addItem(_fromUtf8(""))
        self.comboBoxLogging.addItem(_fromUtf8(""))
        self.comboBoxLogging.addItem(_fromUtf8(""))
        self.comboBoxLogging.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBoxLogging, 5, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(configDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 10, 2, 1, 1)
        self.labelLoggingLevel = QtGui.QLabel(configDialog)
        self.labelLoggingLevel.setObjectName(_fromUtf8("labelLoggingLevel"))
        self.gridLayout.addWidget(self.labelLoggingLevel, 5, 1, 1, 1)
        self.textLogFile = QtGui.QLineEdit(configDialog)
        self.textLogFile.setObjectName(_fromUtf8("textLogFile"))
        self.gridLayout.addWidget(self.textLogFile, 3, 2, 1, 1)
        self.labelLogToConsole = QtGui.QLabel(configDialog)
        self.labelLogToConsole.setObjectName(_fromUtf8("labelLogToConsole"))
        self.gridLayout.addWidget(self.labelLogToConsole, 7, 1, 1, 1)
        self.checkBoxLogToConsole = QtGui.QCheckBox(configDialog)
        self.checkBoxLogToConsole.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBoxLogToConsole.setText(_fromUtf8(""))
        self.checkBoxLogToConsole.setObjectName(_fromUtf8("checkBoxLogToConsole"))
        self.gridLayout.addWidget(self.checkBoxLogToConsole, 7, 2, 1, 1)
        self.textPipLogFile = QtGui.QLineEdit(configDialog)
        self.textPipLogFile.setObjectName(_fromUtf8("textPipLogFile"))
        self.gridLayout.addWidget(self.textPipLogFile, 8, 2, 1, 1)
        self.labelPipLogFile = QtGui.QLabel(configDialog)
        self.labelPipLogFile.setObjectName(_fromUtf8("labelPipLogFile"))
        self.gridLayout.addWidget(self.labelPipLogFile, 8, 1, 1, 1)
        self.labelTerminalWaitTime = QtGui.QLabel(configDialog)
        self.labelTerminalWaitTime.setObjectName(_fromUtf8("labelTerminalWaitTime"))
        self.gridLayout.addWidget(self.labelTerminalWaitTime, 9, 1, 1, 1)
        self.textTerminalWaitTime = QtGui.QLineEdit(configDialog)
        self.textTerminalWaitTime.setObjectName(_fromUtf8("textTerminalWaitTime"))
        self.gridLayout.addWidget(self.textTerminalWaitTime, 9, 2, 1, 1)
        self.labelMakeLogFile = QtGui.QLabel(configDialog)
        self.labelMakeLogFile.setObjectName(_fromUtf8("labelMakeLogFile"))
        self.gridLayout.addWidget(self.labelMakeLogFile, 4, 1, 1, 1)
        self.textMakeLogFile = QtGui.QLineEdit(configDialog)
        self.textMakeLogFile.setObjectName(_fromUtf8("textMakeLogFile"))
        self.gridLayout.addWidget(self.textMakeLogFile, 4, 2, 1, 1)
        self.labelLogFile = QtGui.QLabel(configDialog)
        self.labelLogFile.setObjectName(_fromUtf8("labelLogFile"))
        self.gridLayout.addWidget(self.labelLogFile, 3, 1, 1, 1)

        self.retranslateUi(configDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), configDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), configDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(configDialog)
        configDialog.setTabOrder(self.textFavouritesFile, self.textDatabaseFile)
        configDialog.setTabOrder(self.textDatabaseFile, self.textDownloadPath)
        configDialog.setTabOrder(self.textDownloadPath, self.textLogFile)
        configDialog.setTabOrder(self.textLogFile, self.textMakeLogFile)
        configDialog.setTabOrder(self.textMakeLogFile, self.comboBoxLogging)
        configDialog.setTabOrder(self.comboBoxLogging, self.checkBoxLogToConsole)
        configDialog.setTabOrder(self.checkBoxLogToConsole, self.textPipLogFile)
        configDialog.setTabOrder(self.textPipLogFile, self.textTerminalWaitTime)
        configDialog.setTabOrder(self.textTerminalWaitTime, self.buttonBox)

    def retranslateUi(self, configDialog):
        configDialog.setWindowTitle(QtGui.QApplication.translate("configDialog", "Edit Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFavouritesFile.setText(QtGui.QApplication.translate("configDialog", "Favourites File", None, QtGui.QApplication.UnicodeUTF8))
        self.textFavouritesFile.setToolTip(QtGui.QApplication.translate("configDialog", "<html><head/><body><p>The location and name of the favourites file.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.textFavouritesFile.setWhatsThis(QtGui.QApplication.translate("configDialog", "<html><head/><body><p><br/></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelDownloadPath.setText(QtGui.QApplication.translate("configDialog", "Package \n"
"Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.textDatabaseFile.setToolTip(QtGui.QApplication.translate("configDialog", "<html><head/><body><p>The location and name of the database file.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.textDownloadPath.setToolTip(QtGui.QApplication.translate("configDialog", "<html><head/><body><p>The location that the packages will be downloaded to.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelDatabaseFile.setText(QtGui.QApplication.translate("configDialog", "Database\n"
"File", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxLogging.setToolTip(QtGui.QApplication.translate("configDialog", "<html><head/><body><p>The logging level that the application will use.</p><p>The application will log information of importance equal to or greater than the selected level.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxLogging.setItemText(0, QtGui.QApplication.translate("configDialog", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxLogging.setItemText(1, QtGui.QApplication.translate("configDialog", "Debug", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxLogging.setItemText(2, QtGui.QApplication.translate("configDialog", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxLogging.setItemText(3, QtGui.QApplication.translate("configDialog", "Warning", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxLogging.setItemText(4, QtGui.QApplication.translate("configDialog", "Error", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxLogging.setItemText(5, QtGui.QApplication.translate("configDialog", "Critical", None, QtGui.QApplication.UnicodeUTF8))
        self.labelLoggingLevel.setText(QtGui.QApplication.translate("configDialog", "Logging\n"
"Level", None, QtGui.QApplication.UnicodeUTF8))
        self.textLogFile.setToolTip(QtGui.QApplication.translate("configDialog", "<html><head/><body><p>The name and location of the application log file.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelLogToConsole.setText(QtGui.QApplication.translate("configDialog", "Output logging\n"
"in console", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxLogToConsole.setToolTip(QtGui.QApplication.translate("configDialog", "<html><head/><body><p>Output the logging information to the terminal.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.textPipLogFile.setToolTip(QtGui.QApplication.translate("configDialog", "<html><head/><body><p>The name and location of the log file generated by pip.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPipLogFile.setText(QtGui.QApplication.translate("configDialog", "Pip Log File", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTerminalWaitTime.setText(QtGui.QApplication.translate("configDialog", "Terminal wait\n"
"time (Seconds)", None, QtGui.QApplication.UnicodeUTF8))
        self.textTerminalWaitTime.setToolTip(QtGui.QApplication.translate("configDialog", "<html><head/><body><p>The amount of time the terminal waits after installing a package, to give the user time to read any output.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMakeLogFile.setText(QtGui.QApplication.translate("configDialog", "Make Log\n"
"File", None, QtGui.QApplication.UnicodeUTF8))
        self.textMakeLogFile.setToolTip(QtGui.QApplication.translate("configDialog", "<html><head/><body><p>The name and location of the log generated by the make install utility.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelLogFile.setText(QtGui.QApplication.translate("configDialog", "Application\n"
"Log File", None, QtGui.QApplication.UnicodeUTF8))

