from threading import Thread

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Slot, Qt

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

        # Context menu
        self.newContextMenu = QtWidgets.QMenu()
        self.newContextMenu.addAction('Move to "Owned"',
                                      self.moveFromNewToOwned)
        self.newContextMenu.addAction('Move to "Ignored"',
                                      self.moveFromNewToIgnored)
        self.newTableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.newTableWidget.customContextMenuRequested.connect(self.showMenu)

        # Context menu
        self.ownedContextMenu = QtWidgets.QMenu()
        self.ownedContextMenu.addAction('Move to "New"',
                                        self.moveFromOwnedToNew)
        self.ownedContextMenu.addAction('Move to "Ignored"',
                                        self.moveFromOwnedToIgnored)
        self.ownedTableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ownedTableWidget.customContextMenuRequested.connect(self.showMenu)

        # Context menu
        self.ignoredContextMenu = QtWidgets.QMenu()
        self.ignoredContextMenu.addAction('Move to "New"',
                                          self.moveFromIgnoredToNew)
        self.ignoredContextMenu.addAction('Move to "Owned"',
                                          self.moveFromIgnoredToOwned)
        self.ignoredTableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ignoredTableWidget.customContextMenuRequested.connect(
            self.showMenu)

    def display_anisongs_in_table(self, anisongs):
        self.newTableWidget.setRowCount(len(anisongs))
        for i, anisong in enumerate(anisongs):
            anime_item = QtWidgets.QTableWidgetItem(anisong.anime.anime_name)
            self.newTableWidget.setItem(i, 0, anime_item)
            type_item = QtWidgets.QTableWidgetItem(anisong.type)
            self.newTableWidget.setItem(i, 1, type_item)
            number_item = QtWidgets.QTableWidgetItem(anisong.number)
            self.newTableWidget.setItem(i, 2, number_item)
            title_item = QtWidgets.QTableWidgetItem(anisong.title)
            self.newTableWidget.setItem(i, 3, title_item)
            artist_item = QtWidgets.QTableWidgetItem(anisong.artist)
            self.newTableWidget.setItem(i, 4, artist_item)
            used_in_item = \
                QtWidgets.QTableWidgetItem(anisong.used_in_eps)
            self.newTableWidget.setItem(i, 5, used_in_item)
        self.newTableWidget.resizeColumnsToContents()

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

    def showMenu(self, pos):
        tables_menus = [(self.newTableWidget, self.newContextMenu),
                        (self.ownedTableWidget, self.ownedContextMenu),
                        (self.ignoredTableWidget, self.ignoredContextMenu)]
        for table, context_menu in tables_menus:
            selection_model = table.selectionModel()
            if selection_model.hasSelection():
                context_menu.exec_(QtGui.QCursor.pos())

    def moveSelectedItemsFromTable(self, source_table, dest_table):
        selection_model = source_table.selectionModel()
        nb_rows_selected = len(selection_model.selectedRows())
        row_count = dest_table.rowCount() - 1
        dest_table.setRowCount(dest_table.rowCount() + nb_rows_selected)

        rows_to_delete = list()

        dest_table.setSortingEnabled(False)
        for item in source_table.selectedItems():
            item_column = item.column()
            item_row = item.row()
            # Remove ownership of the widget
            item = source_table.takeItem(item_row, item_column)

            if item_row not in rows_to_delete:
                rows_to_delete.append(item_row)
                row_count += 1

            dest_table.setItem(row_count, item_column, item)
        dest_table.sortByColumn(0, Qt.AscendingOrder)
        dest_table.setSortingEnabled(True)
        dest_table.resizeColumnsToContents()

        # Remove rows in decreasing order to avoid removing the wrong rows
        rows_to_delete.sort(reverse=True)
        for row_to_delete in rows_to_delete:
            source_table.removeRow(row_to_delete)

    def moveFromNewToOwned(self):
        self.moveSelectedItemsFromTable(self.newTableWidget,
                                        self.ownedTableWidget)

    def moveFromNewToIgnored(self):
        self.moveSelectedItemsFromTable(self.newTableWidget,
                                        self.ignoredTableWidget)

    def moveFromOwnedToNew(self):
        self.moveSelectedItemsFromTable(self.ownedTableWidget,
                                        self.newTableWidget)

    def moveFromOwnedToIgnored(self):
        self.moveSelectedItemsFromTable(self.ownedTableWidget,
                                        self.ignoredTableWidget)

    def moveFromIgnoredToNew(self):
        self.moveSelectedItemsFromTable(self.ignoredTableWidget,
                                        self.newTableWidget)

    def moveFromIgnoredToOwned(self):
        self.moveSelectedItemsFromTable(self.ignoredTableWidget,
                                        self.ownedTableWidget)
