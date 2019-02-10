from threading import Thread

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Slot

from ui.ui_main_window import Ui_MainWindow
from ui.import_dialog import ImportDialog

from anime import Anime
from animelist import AnimeList


class MainWindow(Ui_MainWindow):
    def __init__(self):
        self.dialog_widget = QtWidgets.QDialog()
        self.import_dialog = ImportDialog()
        self.import_dialog.finished.connect(self.onImportDone)
        self.import_dialog.setupUi(self.dialog_widget)

    def setupUi(self, main_win):
        super(MainWindow, self).setupUi(main_win)
        self.actionExit.triggered.connect(main_win.close)
        self.actionImport.triggered.connect(self.dialog_widget.show)

    def display_anisongs_in_table(self, anisongs):
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

    @Slot(str)
    def onImportDone(self, mal_xml):
        self.user_animelist = AnimeList(mal_xml, include_ptw=False,
                                        exclude_animes_from_file=False)
        self.import_dialog.display_progress_bar(
            min_value=0,
            max_value=self.user_animelist.get_nb_animes())

        th = Thread(target=self.fetch_and_display_anisongs)
        th.start()

    def fetch_and_display_anisongs(self):
        self.user_animes = list()
        for data in self.user_animelist.anime_data:
            self.import_dialog.anisong_loading_widget.infoReceived.emit(
                str(data['anime_title']))
            self.user_animes.append(Anime.from_dict(data))
            self.import_dialog.anisong_loading_widget.progressed.emit()

            # User clicked on Cancel while loading anisongs
            if not self.import_dialog.anisong_loading_widget.isVisible():
                break

        anisongs = list()
        for user_anime in self.user_animes:
            anisongs += user_anime.songs

        self.display_anisongs_in_table(anisongs)
        self.import_dialog.anisong_loading_widget.close()
        self.import_dialog.close()


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
