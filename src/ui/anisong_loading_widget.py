from PySide2.QtCore import QObject, Signal, Slot

from ui.ui_loading_widget import Ui_LoadingWidget


class AnisongLoadingWidget(QObject, Ui_LoadingWidget):
    progressed = Signal()
    infoReceived = Signal(str)
    DEFAULT_INFO_TEXT = "Fetching anime data, please wait..."

    def setupUi(self, base_widget):
        super(AnisongLoadingWidget, self).setupUi(base_widget)
        self.close = base_widget.close
        self.isVisible = base_widget.isVisible
        self.cancelPushButton.clicked.connect(base_widget.close)
        self.progressed.connect(self.increment_progress_bar)
        self.infoReceived.connect(self.update_info_text)
        self.infoLabel.setText(self.DEFAULT_INFO_TEXT)

    def init_progress_bar(self, min_value=0, max_value=0):
        self.progressBar.setMinimum(min_value)
        self.progressBar.setMaximum(max_value)
        self.progressBar.setValue(0)

    def increment_progress_bar(self):
        self.progressBar.setValue(self.progressBar.value() + 1)

    @Slot(str)
    def update_info_text(self, new_text):
        print(new_text)
        self.infoLabel.setText("{0}<br>{1}".format(self.DEFAULT_INFO_TEXT,
                                                   new_text))
