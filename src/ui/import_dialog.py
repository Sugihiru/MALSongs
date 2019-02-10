from PySide2 import QtWidgets

from ui.ui_import_dialog import Ui_ImportDialog


class ImportDialog(Ui_ImportDialog):
    def setupUi(self, dialog_widget):
        super(ImportDialog, self).setupUi(dialog_widget)
        self.browsePushButton.clicked.connect(self.onBrowseClick)
        self.importPushButton.clicked.connect(self.onImportClick)
        self.close = dialog_widget.close

    def onBrowseClick(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "Open File", "", "XML files (*.xml)")
        if filename:
            self.fromXmlLineEdit.setText(filename)

    def onImportClick(self):
        filename = self.fromXmlLineEdit.text()
        if not filename:
            self.close()
        print(filename)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog_widget = QtWidgets.QDialog()
    ui = ImportDialog()
    ui.setupUi(dialog_widget)
    dialog_widget.show()
    sys.exit(app.exec_())

