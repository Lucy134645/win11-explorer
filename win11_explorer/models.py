"""
File system item models and sorting for Win11 Explorer.
Supports Details View, Grid View, filtering, and hidden file toggles.
"""

import os
from dataclasses import dataclass
from typing import List, Optional
from PyQt6.QtCore import (
    QAbstractTableModel, QModelIndex, Qt, QVariant, QDateTime
)
from PyQt6.QtGui import QIcon
from win11_explorer.file_ops import (
    format_size, format_datetime, get_file_type_description, get_file_icon_name
)
from win11_explorer.icons import get_icon


@dataclass
class FileItem:
    name: str
    path: str
    is_dir: bool
    size: int
    modified_time: float
    type_str: str
    icon_name: str
    is_hidden: bool


class FileTableModel(QAbstractTableModel):
    """Table model representing files and folders in a directory."""

    COL_NAME = 0
    COL_DATE = 1
    COL_TYPE = 2
    COL_SIZE = 3

    HEADERS = ["Name", "Date modified", "Type", "Size"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_directory: str = ""
        self.all_items: List[FileItem] = []
        self.filtered_items: List[FileItem] = []
        self.show_hidden: bool = False
        self.search_filter: str = ""
        self.sort_column: int = self.COL_NAME
        self.sort_order: Qt.SortOrder = Qt.SortOrder.AscendingOrder

    def load_directory(self, path: str):
        """Scan directory and populate items."""
        self.beginResetModel()
        self.current_directory = os.path.abspath(path)
        self.all_items.clear()

        try:
            with os.scandir(self.current_directory) as entries:
                for entry in entries:
                    is_hidden = entry.name.startswith(".")
                    try:
                        stat = entry.stat()
                        is_dir = entry.is_dir(follow_symlinks=False)
                        size = 0 if is_dir else stat.st_size
                        mtime = stat.st_mtime
                    except Exception:
                        is_dir = False
                        size = 0
                        mtime = 0.0

                    type_desc = get_file_type_description(entry.path, is_dir)
                    icon_name = get_file_icon_name(entry.path, is_dir)

                    self.all_items.append(FileItem(
                        name=entry.name,
                        path=entry.path,
                        is_dir=is_dir,
                        size=size,
                        modified_time=mtime,
                        type_str=type_desc,
                        icon_name=icon_name,
                        is_hidden=is_hidden
                    ))
        except Exception as e:
            print(f"Error reading directory {path}: {e}")

        self._apply_filter_and_sort()
        self.endResetModel()

    def set_show_hidden(self, show: bool):
        if self.show_hidden != show:
            self.beginResetModel()
            self.show_hidden = show
            self._apply_filter_and_sort()
            self.endResetModel()

    def set_search_filter(self, filter_text: str):
        self.beginResetModel()
        self.search_filter = filter_text.strip().lower()
        self._apply_filter_and_sort()
        self.endResetModel()

    def _apply_filter_and_sort(self):
        """Filter by hidden state and search query, then sort."""
        items = []
        for it in self.all_items:
            if it.is_hidden and not self.show_hidden:
                continue
            if self.search_filter and self.search_filter not in it.name.lower():
                continue
            items.append(it)

        # Sort: directories first (Windows Explorer convention)
        reverse = (self.sort_order == Qt.SortOrder.DescendingOrder)

        def sort_key(item: FileItem):
            # Sort directories first
            dir_priority = 0 if item.is_dir else 1
            if self.sort_column == self.COL_NAME:
                val = item.name.lower()
            elif self.sort_column == self.COL_DATE:
                val = item.modified_time
            elif self.sort_column == self.COL_TYPE:
                val = item.type_str.lower()
            elif self.sort_column == self.COL_SIZE:
                val = item.size
            else:
                val = item.name.lower()
            return (dir_priority, val)

        # Windows explorer keeps folders on top even when descending sort
        if reverse:
            # Sort with folders top, but reverse inside each group
            folders = [it for it in items if it.is_dir]
            files = [it for it in items if not it.is_dir]
            folders.sort(key=lambda it: self._get_col_val(it), reverse=True)
            files.sort(key=lambda it: self._get_col_val(it), reverse=True)
            self.filtered_items = folders + files
        else:
            folders = [it for it in items if it.is_dir]
            files = [it for it in items if not it.is_dir]
            folders.sort(key=lambda it: self._get_col_val(it), reverse=False)
            files.sort(key=lambda it: self._get_col_val(it), reverse=False)
            self.filtered_items = folders + files

    def _get_col_val(self, item: FileItem):
        if self.sort_column == self.COL_NAME:
            return item.name.lower()
        elif self.sort_column == self.COL_DATE:
            return item.modified_time
        elif self.sort_column == self.COL_TYPE:
            return item.type_str.lower()
        elif self.sort_column == self.COL_SIZE:
            return item.size
        return item.name.lower()

    def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder):
        self.beginResetModel()
        self.sort_column = column
        self.sort_order = order
        self._apply_filter_and_sort()
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.filtered_items)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.HEADERS)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if 0 <= section < len(self.HEADERS):
                return self.HEADERS[section]
        return QVariant()

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self.filtered_items):
            return QVariant()

        item = self.filtered_items[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if col == self.COL_NAME:
                return item.name
            elif col == self.COL_DATE:
                return format_datetime(item.modified_time) if item.modified_time else ""
            elif col == self.COL_TYPE:
                return item.type_str
            elif col == self.COL_SIZE:
                return "" if item.is_dir else format_size(item.size)

        elif role == Qt.ItemDataRole.DecorationRole:
            if col == self.COL_NAME:
                return get_icon(item.icon_name, size=22)

        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if col == self.COL_SIZE:
                return int(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            return int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        elif role == Qt.ItemDataRole.UserRole:
            # Custom role returns the FileItem
            return item

        return QVariant()

    def get_item(self, row: int) -> Optional[FileItem]:
        if 0 <= row < len(self.filtered_items):
            return self.filtered_items[row]
        return None
