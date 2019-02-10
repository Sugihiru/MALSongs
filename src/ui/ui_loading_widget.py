# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\ui\ui_loading_widget.ui',
# licensing of '.\src\ui\ui_loading_widget.ui' applies.
#
# Created: Sun Feb 10 18:18:29 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_LoadingWidget(object):
    def setupUi(self, LoadingWidget):
        LoadingWidget.setObjectName("LoadingWidget")
        LoadingWidget.resize(400, 125)
        self.verticalLayout = QtWidgets.QVBoxLayout(LoadingWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.infoLabel = QtWidgets.QLabel(LoadingWidget)
        self.infoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.infoLabel.setObjectName("infoLabel")
        self.verticalLayout.addWidget(self.infoLabel)
        self.progressBar = QtWidgets.QProgressBar(LoadingWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.cancelPushButton = QtWidgets.QPushButton(LoadingWidget)
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.verticalLayout.addWidget(self.cancelPushButton)

        self.retranslateUi(LoadingWidget)
        QtCore.QMetaObject.connectSlotsByName(LoadingWidget)

    def retranslateUi(self, LoadingWidget):
        LoadingWidget.setWindowTitle(QtWidgets.QApplication.translate("LoadingWidget", "Loading", None, -1))
        self.infoLabel.setText(QtWidgets.QApplication.translate("LoadingWidget", "In progress...", None, -1))
        self.cancelPushButton.setText(QtWidgets.QApplication.translate("LoadingWidget", "Cancel", None, -1))

