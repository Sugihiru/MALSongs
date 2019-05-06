# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_import_dialog.ui',
# licensing of '.\ui_import_dialog.ui' applies.
#
# Created: Mon May  6 18:00:08 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ImportDialog(object):
    def setupUi(self, ImportDialog):
        ImportDialog.setObjectName("ImportDialog")
        ImportDialog.resize(500, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(ImportDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(ImportDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.malTab = QtWidgets.QWidget()
        self.malTab.setObjectName("malTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.malTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.instructionsLabel = QtWidgets.QLabel(self.malTab)
        self.instructionsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.instructionsLabel.setOpenExternalLinks(True)
        self.instructionsLabel.setObjectName("instructionsLabel")
        self.verticalLayout_3.addWidget(self.instructionsLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fromXmlLabel = QtWidgets.QLabel(self.malTab)
        self.fromXmlLabel.setObjectName("fromXmlLabel")
        self.horizontalLayout.addWidget(self.fromXmlLabel)
        self.fromXmlLineEdit = QtWidgets.QLineEdit(self.malTab)
        self.fromXmlLineEdit.setObjectName("fromXmlLineEdit")
        self.horizontalLayout.addWidget(self.fromXmlLineEdit)
        self.browsePushButton = QtWidgets.QPushButton(self.malTab)
        self.browsePushButton.setObjectName("browsePushButton")
        self.horizontalLayout.addWidget(self.browsePushButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.reimportCheckBox = QtWidgets.QCheckBox(self.malTab)
        self.reimportCheckBox.setObjectName("reimportCheckBox")
        self.verticalLayout_3.addWidget(self.reimportCheckBox)
        self.importPushButton = QtWidgets.QPushButton(self.malTab)
        self.importPushButton.setObjectName("importPushButton")
        self.verticalLayout_3.addWidget(self.importPushButton)
        self.tabWidget.addTab(self.malTab, "")
        self.anilistTab = QtWidgets.QWidget()
        self.anilistTab.setObjectName("anilistTab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.anilistTab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.anilistTab)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.tabWidget.addTab(self.anilistTab, "")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(ImportDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ImportDialog)

    def retranslateUi(self, ImportDialog):
        ImportDialog.setWindowTitle(QtWidgets.QApplication.translate("ImportDialog", "Dialog", None, -1))
        self.instructionsLabel.setText(QtWidgets.QApplication.translate("ImportDialog", "<html><head/><body><p><a href=\"https://myanimelist.net/panel.php?go=export\"><span style=\" text-decoration: underline; color:#0000ff;\">Export your MyAnimeList\'s list</span></a>, then extract the XML from the .gzip file.</p></body></html>", None, -1))
        self.fromXmlLabel.setText(QtWidgets.QApplication.translate("ImportDialog", "Exported XML", None, -1))
        self.browsePushButton.setText(QtWidgets.QApplication.translate("ImportDialog", "Browse", None, -1))
        self.reimportCheckBox.setText(QtWidgets.QApplication.translate("ImportDialog", "Re-import animes that are already on the list", None, -1))
        self.importPushButton.setText(QtWidgets.QApplication.translate("ImportDialog", "Import", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.malTab), QtWidgets.QApplication.translate("ImportDialog", "MyAnimeList", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("ImportDialog", "Soon™ !", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.anilistTab), QtWidgets.QApplication.translate("ImportDialog", "Anilist", None, -1))

