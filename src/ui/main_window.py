from PySide2 import QtWidgets, QtGui

from ui.ui_main_window import Ui_MainWindow
from ui.import_dialog import ImportDialog


class MainWindow(Ui_MainWindow):
    def __init__(self):
        self.dialog_widget = QtWidgets.QDialog()
        self.import_dialog = ImportDialog()
        self.import_dialog.setupUi(self.dialog_widget)

    def setupUi(self, main_win, anisongs):
        super(MainWindow, self).setupUi(main_win)
        self.actionExit.triggered.connect(main_win.close)
        self.actionImport.triggered.connect(self.onImportClick)

        self.tableWidget.setRowCount(len(anisongs))
        for i, anisong in enumerate(anisongs):
            anime_item = QtWidgets.QTableWidgetItem(anisong.anime.anime_name)
            self.tableWidget.setItem(i, 0, anime_item)
            type_item = QtWidgets.QTableWidgetItem(anisong.type)
            self.tableWidget.setItem(i, 1, type_item)
            number_item = QtWidgets.QTableWidgetItem(anisong.number)
            self.tableWidget.setItem(i, 2, number_item)
            title_item = QtWidgets.QTableWidgetItem(anisong.title)
            self.tableWidget.setItem(i, 3, title_item)
            artist_item = QtWidgets.QTableWidgetItem(anisong.artist)
            self.tableWidget.setItem(i, 4, artist_item)
            used_in_item = \
                QtWidgets.QTableWidgetItem(anisong.used_in_eps)
            self.tableWidget.setItem(i, 5, used_in_item)
        self.tableWidget.resizeColumnsToContents()

    def onImportClick(self):
        self.dialog_widget.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mw = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setupUi(mw)

    row = 0
    column = 0
    ui.tableWidget.setRowCount(10)
    newItem = QtWidgets.QTableWidgetItem("aaaaaaaaaaaaaaaaaaaaaaaaaaa")
    newItem.setBackground(QtGui.QBrush(QtGui.QColor(100, 100, 100)))
    ui.tableWidget.setItem(row, column, newItem)

    mw.show()
    sys.exit(app.exec_())
