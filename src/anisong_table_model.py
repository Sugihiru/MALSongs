from PySide2 import QtCore
from PySide2.QtCore import Qt

import database_manager as db


class AnisongTableModel(QtCore.QAbstractTableModel):
    def __init__(self, anisongs=None):
        super().__init__()
        if anisongs:
            self.anisongs = anisongs
        else:
            self.anisongs = list()
        self.headers = ["Anime", "Type", "Number", "Song", "Artist", "Used in"]

    def load_from_database(self):
        db.create_table()  # Create the table if it doesn't exist
        self.anisongs = db.get_all_anisongs()

        # Needed to notify View that rowCount has changed
        self.beginInsertRows(QtCore.QModelIndex(),
                             0, len(self.anisongs))
        self.endInsertRows()
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def rowCount(self, parent=None):
        return len(self.anisongs)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            if column == 0:
                value = self.anisongs[row].anime.anime_name
            elif column == 1:
                value = self.anisongs[row].type
            elif column == 2:
                value = self.anisongs[row].number
            elif column == 3:
                value = self.anisongs[row].title
            elif column == 4:
                value = self.anisongs[row].artist
            elif column == 5:
                value = self.anisongs[row].used_in_eps
            return value

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]

    def insertRows(self, row, count, new_items, parent=QtCore.QModelIndex()):
        self.beginInsertRows(QtCore.QModelIndex(),
                             row,
                             row + count)
        self.anisongs += new_items
        self.endInsertRows()
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def modelIndexToData(self, index_list):
        """Returns the data corresponding to the indexes
        The indexes must match the following conditions :
            - len(index_list) == self.columnCount()
            - index_list are correctly ordered by column number
        """
        title = index_list[3].data()
        artist = index_list[4].data()

        corresponding_data = next((x for x in self.anisongs
                                   if x.title == title and x.artist == artist),
                                  None)
        return corresponding_data


class ProxyAnisongTableModel(QtCore.QSortFilterProxyModel):
    def __init__(self, accepted_status):
        super().__init__()
        self.accepted_status = accepted_status

    def filterAcceptsRow(self, sourceRow, sourceParent):
        if sourceRow >= self.sourceModel().rowCount():
            return False
        return (self.sourceModel().anisongs[sourceRow].status ==
                self.accepted_status)
