from PySide2 import QtWidgets
from PySide2.QtCore import Signal, QObject

from ui.ui_import_dialog import Ui_ImportDialog
from ui.anisong_loading_widget import AnisongLoadingWidget


# Inherits from QObject to use Signal()
class ImportDialog(QObject, Ui_ImportDialog):
    finished = Signal(str)

    def __init__(self):
        super().__init__()
        self.base_loading_widget = QtWidgets.QWidget()
        self.anisong_loading_widget = AnisongLoadingWidget()
        self.anisong_loading_widget.setupUi(self.base_loading_widget)

    def setupUi(self, dialog_widget):
        super(ImportDialog, self).setupUi(dialog_widget)
        self.browsePushButton.clicked.connect(self.onBrowseClick)
        self.importPushButton.clicked.connect(self.onImportClick)
        self.close = dialog_widget.close

    def display_progress_bar(self, min_value=0, max_value=0):
        self.anisong_loading_widget.init_progress_bar(min_value=min_value,
                                                      max_value=max_value)
        self.base_loading_widget.show()

    def onBrowseClick(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "Open File", "", "XML files (*.xml)")
        if filename:
            self.fromXmlLineEdit.setText(filename)

    def onImportClick(self):
        filename = self.fromXmlLineEdit.text()
        if not filename:
            self.close()
        self.finished.emit(filename)
