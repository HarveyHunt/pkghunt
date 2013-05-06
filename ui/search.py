# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'search.ui'
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

class Ui_searchDialog(object):
    def setupUi(self, searchDialog):
        searchDialog.setObjectName(_fromUtf8("searchDialog"))
        searchDialog.resize(400, 300)
        searchDialog.setAutoFillBackground(False)
        self.gridLayout = QtGui.QGridLayout(searchDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textPackageID = QtGui.QLineEdit(searchDialog)
        self.textPackageID.setInputMethodHints(QtCore.Qt.ImhNone)
        self.textPackageID.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.textPackageID.setObjectName(_fromUtf8("textPackageID"))
        self.gridLayout.addWidget(self.textPackageID, 0, 1, 1, 1)
        self.textLanguage = QtGui.QLineEdit(searchDialog)
        self.textLanguage.setObjectName(_fromUtf8("textLanguage"))
        self.gridLayout.addWidget(self.textLanguage, 2, 1, 1, 1)
        self.labelPackageID = QtGui.QLabel(searchDialog)
        self.labelPackageID.setObjectName(_fromUtf8("labelPackageID"))
        self.gridLayout.addWidget(self.labelPackageID, 0, 0, 1, 1)
        self.textSize = QtGui.QLineEdit(searchDialog)
        self.textSize.setObjectName(_fromUtf8("textSize"))
        self.gridLayout.addWidget(self.textSize, 3, 1, 1, 1)
        self.labelPackageName = QtGui.QLabel(searchDialog)
        self.labelPackageName.setObjectName(_fromUtf8("labelPackageName"))
        self.gridLayout.addWidget(self.labelPackageName, 1, 0, 1, 1)
        self.textPackageName = QtGui.QLineEdit(searchDialog)
        self.textPackageName.setObjectName(_fromUtf8("textPackageName"))
        self.gridLayout.addWidget(self.textPackageName, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(searchDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 1)
        self.checkBoxGithub = QtGui.QCheckBox(searchDialog)
        self.checkBoxGithub.setChecked(True)
        self.checkBoxGithub.setObjectName(_fromUtf8("checkBoxGithub"))
        self.gridLayout.addWidget(self.checkBoxGithub, 4, 0, 1, 1)
        self.labelSize = QtGui.QLabel(searchDialog)
        self.labelSize.setObjectName(_fromUtf8("labelSize"))
        self.gridLayout.addWidget(self.labelSize, 3, 0, 1, 1)
        self.checkBoxDatabase = QtGui.QCheckBox(searchDialog)
        self.checkBoxDatabase.setObjectName(_fromUtf8("checkBoxDatabase"))
        self.gridLayout.addWidget(self.checkBoxDatabase, 4, 1, 1, 1)
        self.labelLanguage = QtGui.QLabel(searchDialog)
        self.labelLanguage.setObjectName(_fromUtf8("labelLanguage"))
        self.gridLayout.addWidget(self.labelLanguage, 2, 0, 1, 1)

        self.retranslateUi(searchDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), searchDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), searchDialog.reject)
        QtCore.QObject.connect(self.checkBoxGithub, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.textPackageID.setDisabled)
        QtCore.QObject.connect(self.checkBoxGithub, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.textPackageID.clear)
        QtCore.QObject.connect(self.checkBoxGithub, QtCore.SIGNAL(_fromUtf8("clicked()")), self.checkBoxDatabase.toggle)
        QtCore.QObject.connect(self.checkBoxDatabase, QtCore.SIGNAL(_fromUtf8("clicked()")), self.checkBoxGithub.toggle)
        QtCore.QMetaObject.connectSlotsByName(searchDialog)
        searchDialog.setTabOrder(self.textPackageID, self.textPackageName)
        searchDialog.setTabOrder(self.textPackageName, self.textLanguage)
        searchDialog.setTabOrder(self.textLanguage, self.textSize)
        searchDialog.setTabOrder(self.textSize, self.checkBoxGithub)
        searchDialog.setTabOrder(self.checkBoxGithub, self.checkBoxDatabase)
        searchDialog.setTabOrder(self.checkBoxDatabase, self.buttonBox)

    def retranslateUi(self, searchDialog):
        searchDialog.setWindowTitle(QtGui.QApplication.translate("searchDialog", "Search Github and Database", None, QtGui.QApplication.UnicodeUTF8))
        self.textPackageID.setToolTip(QtGui.QApplication.translate("searchDialog", "<html><head/><body><p>The ID of the package (not applicable to a GitHub search).</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.textLanguage.setToolTip(QtGui.QApplication.translate("searchDialog", "<html><head/><body><p>The language of the package.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPackageID.setText(QtGui.QApplication.translate("searchDialog", "Package ID", None, QtGui.QApplication.UnicodeUTF8))
        self.textSize.setToolTip(QtGui.QApplication.translate("searchDialog", "<html><head/><body><p>The size of the package, the operators &lt; and &gt; are supported.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPackageName.setText(QtGui.QApplication.translate("searchDialog", "Package Name", None, QtGui.QApplication.UnicodeUTF8))
        self.textPackageName.setToolTip(QtGui.QApplication.translate("searchDialog", "<html><head/><body><p>The name of the package.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxGithub.setToolTip(QtGui.QApplication.translate("searchDialog", "<html><head/><body><p>Search GitHub.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxGithub.setText(QtGui.QApplication.translate("searchDialog", "Github", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSize.setText(QtGui.QApplication.translate("searchDialog", "Size", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxDatabase.setToolTip(QtGui.QApplication.translate("searchDialog", "<html><head/><body><p>Search the database.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxDatabase.setText(QtGui.QApplication.translate("searchDialog", "Database", None, QtGui.QApplication.UnicodeUTF8))
        self.labelLanguage.setText(QtGui.QApplication.translate("searchDialog", "Language", None, QtGui.QApplication.UnicodeUTF8))

