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

    def loadFromDatabase(self):
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

    def insertRows(self, new_items):
        new_items = list(filter(lambda x: x not in self.anisongs, new_items))
        # No new songs to insert
        if not len(new_items):
            return False
        self.beginInsertRows(QtCore.QModelIndex(),
                             len(self.anisongs),
                             len(self.anisongs) + len(new_items))
        self.anisongs += new_items
        self.endInsertRows()
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        return True

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

    def getAllAnimes(self):
        """Returns all unique anime names in self.anisongs or None"""
        if not self.anisongs:
            return None
        return list(set([x.anime.anime_name for x in self.anisongs]))


class ProxyAnisongTableModel(QtCore.QSortFilterProxyModel):
    def __init__(self, accepted_status):
        super().__init__()
        self.accepted_status = accepted_status
        self.search_category = 0

    def filterAcceptsRow(self, sourceRow, sourceParent):
        if sourceRow >= self.sourceModel().rowCount():
            return False
        song = self.sourceModel().anisongs[sourceRow]
        if (song.status != self.accepted_status):
            return False

        return self.match_fields(self.filterRegExp(), song)

    def match_fields(self, filter_regex, song):
        """Check if the song matches the filter parameters"""
        if (filter_regex.isEmpty()):
            return True

        if self.search_category == 0:
            return (filter_regex.exactMatch(song.title) or
                    filter_regex.exactMatch(song.anime.anime_name) or
                    filter_regex.exactMatch(song.artist))

        category_to_field = {
            1: song.anime.anime_name,
            2: song.artist,
            3: song.title}

        return filter_regex.exactMatch(category_to_field[self.search_category])
