from threading import Thread

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Slot, Qt

from ui.ui_main_window import Ui_MainWindow
from ui.import_dialog import ImportDialog

from anime import Anime
from animelist import AnimeList
from anisong import AnisongStatusNamespace
import database_manager as db
from anisong_table_model import AnisongTableModel, ProxyAnisongTableModel


class MainWindow(Ui_MainWindow):
    def __init__(self):
        self.dialog_widget = QtWidgets.QDialog()
        self.import_dialog = ImportDialog()
        self.import_dialog.finished.connect(self.onImportDone)
        self.import_dialog.setupUi(self.dialog_widget)

        self.model = AnisongTableModel()
        self.model.dataChanged.connect(self.resizeColumns)
        self.newProxyModel = ProxyAnisongTableModel(AnisongStatusNamespace.new)
        self.newProxyModel.setSourceModel(self.model)
        self.ownedProxyModel = ProxyAnisongTableModel(
            AnisongStatusNamespace.owned)
        self.ownedProxyModel.setSourceModel(self.model)
        self.ignoredProxyModel = ProxyAnisongTableModel(
            AnisongStatusNamespace.ignored)
        self.ignoredProxyModel.setSourceModel(self.model)

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
        self.newTableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.newTableView.customContextMenuRequested.connect(self.showMenu)
        self.newTableView.setModel(self.newProxyModel)

        # Context menu
        self.ownedContextMenu = QtWidgets.QMenu()
        self.ownedContextMenu.addAction('Move to "New"',
                                        self.moveFromOwnedToNew)
        self.ownedContextMenu.addAction('Move to "Ignored"',
                                        self.moveFromOwnedToIgnored)
        self.ownedTableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ownedTableView.customContextMenuRequested.connect(self.showMenu)
        self.ownedTableView.setModel(self.ownedProxyModel)

        # Context menu
        self.ignoredContextMenu = QtWidgets.QMenu()
        self.ignoredContextMenu.addAction('Move to "New"',
                                          self.moveFromIgnoredToNew)
        self.ignoredContextMenu.addAction('Move to "Owned"',
                                          self.moveFromIgnoredToOwned)
        self.ignoredTableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ignoredTableView.customContextMenuRequested.connect(
            self.showMenu)
        self.ignoredTableView.setModel(self.ignoredProxyModel)

    @Slot(str)
    def onImportDone(self, mal_xml):
        """Called when user has chosen the file he wants to import"""
        excluded_animes = None
        if not self.import_dialog.isReimportChecked():
            excluded_animes = self.model.getAllAnimes()
        self.user_animelist = AnimeList(mal_xml, include_ptw=False,
                                        exclude_animes_from_file=False,
                                        excluded_animes=excluded_animes)
        self.import_dialog.display_progress_bar(
            min_value=0,
            max_value=self.user_animelist.get_nb_animes())

        th = Thread(target=self.fetch_anisongs)
        th.start()

    def fetch_anisongs(self):
        user_animes = list()
        for data in self.user_animelist.anime_data:
            self.import_dialog.anisong_loading_widget.infoReceived.emit(
                str(data['anime_title']))
            user_animes.append(Anime.from_dict(data))
            self.import_dialog.anisong_loading_widget.progressed.emit()

            # User clicked on Cancel while loading anisongs
            if not self.import_dialog.anisong_loading_widget.isVisible():
                break

        anisongs = list()
        for user_anime in user_animes:
            anisongs += user_anime.songs
        self.model.insertRows(anisongs)

        self.import_dialog.anisong_loading_widget.close()
        self.import_dialog.close()

    def showMenu(self, pos):
        tables_menus = [(self.newTableView, self.newContextMenu),
                        (self.ownedTableView, self.ownedContextMenu),
                        (self.ignoredTableView, self.ignoredContextMenu)]
        for table, context_menu in tables_menus:
            selected_indexes = table.selectedIndexes()
            if len(selected_indexes):
                context_menu.exec_(QtGui.QCursor.pos())

    def changeStatusOfSelectedItemsOfTable(self, source_table, new_status):
        selected_indexes = source_table.selectedIndexes()

        source_model = selected_indexes[0].model().sourceModel()
        nb_columns = source_model.columnCount()
        for i in range(0, len(selected_indexes) // nb_columns):
            # Get the indexes of the whole row
            indexes = selected_indexes[i * nb_columns:(i + 1) * nb_columns]
            song = source_model.modelIndexToData(indexes)
            song.status = new_status

        self.invalidateAllModelFilters()

    def saveToDatabase(self):
        """Save anisongs to database"""
        db.generate_and_update_db_objects_for_anisongs(self.model.anisongs)
        db.commit()

    def resizeColumns(self, topleft=None, bottomright=None):
        """Resize the columns of every tableView
        topleft and bottomright args are needed for Qt callback but are unused
        """
        for table in (self.newTableView,
                      self.ownedTableView,
                      self.ignoredTableView):
            table.resizeColumnsToContents()

    def invalidateAllModelFilters(self):
        """Invalidate and relaunch validation for all models"""
        for model in (self.newProxyModel,
                      self.ownedProxyModel,
                      self.ignoredProxyModel):
            model.invalidateFilter()
        self.resizeColumns()

    def moveFromNewToOwned(self):
        self.changeStatusOfSelectedItemsOfTable(self.newTableView,
                                                AnisongStatusNamespace.owned)

    def moveFromNewToIgnored(self):
        self.changeStatusOfSelectedItemsOfTable(self.newTableView,
                                                AnisongStatusNamespace.ignored)

    def moveFromOwnedToNew(self):
        self.changeStatusOfSelectedItemsOfTable(self.ownedTableView,
                                                AnisongStatusNamespace.new)

    def moveFromOwnedToIgnored(self):
        self.changeStatusOfSelectedItemsOfTable(self.ownedTableView,
                                                AnisongStatusNamespace.ignored)

    def moveFromIgnoredToNew(self):
        self.changeStatusOfSelectedItemsOfTable(self.ignoredTableView,
                                                AnisongStatusNamespace.new)

    def moveFromIgnoredToOwned(self):
        self.changeStatusOfSelectedItemsOfTable(self.ignoredTableView,
                                                AnisongStatusNamespace.owned)
