# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'delete.ui'
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

class Ui_deleteDialog(object):
    def setupUi(self, deleteDialog):
        deleteDialog.setObjectName(_fromUtf8("deleteDialog"))
        deleteDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(deleteDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelPackagesToDelete = QtGui.QLabel(deleteDialog)
        self.labelPackagesToDelete.setObjectName(_fromUtf8("labelPackagesToDelete"))
        self.gridLayout.addWidget(self.labelPackagesToDelete, 0, 0, 1, 1)
        self.tableDelete = QtGui.QTableWidget(deleteDialog)
        self.tableDelete.setObjectName(_fromUtf8("tableDelete"))
        self.tableDelete.setColumnCount(6)
        self.tableDelete.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableDelete.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableDelete.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableDelete.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableDelete.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableDelete.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableDelete.setHorizontalHeaderItem(5, item)
        self.gridLayout.addWidget(self.tableDelete, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(deleteDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.boxRemoveDownloadedContent = QtGui.QCheckBox(deleteDialog)
        self.boxRemoveDownloadedContent.setChecked(True)
        self.boxRemoveDownloadedContent.setObjectName(_fromUtf8("boxRemoveDownloadedContent"))
        self.gridLayout.addWidget(self.boxRemoveDownloadedContent, 2, 0, 1, 1)

        self.retranslateUi(deleteDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), deleteDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), deleteDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(deleteDialog)
        deleteDialog.setTabOrder(self.tableDelete, self.boxRemoveDownloadedContent)
        deleteDialog.setTabOrder(self.boxRemoveDownloadedContent, self.buttonBox)

    def retranslateUi(self, deleteDialog):
        deleteDialog.setWindowTitle(QtGui.QApplication.translate("deleteDialog", "Delete Packages", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPackagesToDelete.setText(QtGui.QApplication.translate("deleteDialog", "Packages to be deleted", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableDelete.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("deleteDialog", "Favourite", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableDelete.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("deleteDialog", "Package ID", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableDelete.horizontalHeaderItem(2)
        item.setText(QtGui.QApplication.translate("deleteDialog", "Package Name", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableDelete.horizontalHeaderItem(3)
        item.setText(QtGui.QApplication.translate("deleteDialog", "Size", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableDelete.horizontalHeaderItem(4)
        item.setText(QtGui.QApplication.translate("deleteDialog", "Language", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableDelete.horizontalHeaderItem(5)
        item.setText(QtGui.QApplication.translate("deleteDialog", "Date Installed", None, QtGui.QApplication.UnicodeUTF8))
        self.boxRemoveDownloadedContent.setToolTip(QtGui.QApplication.translate("deleteDialog", "<html><head/><body><p>If checked, the application will delete all of the downloaded files for a package during the uninstallation process.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.boxRemoveDownloadedContent.setText(QtGui.QApplication.translate("deleteDialog", "Remove downloaded content", None, QtGui.QApplication.UnicodeUTF8))

