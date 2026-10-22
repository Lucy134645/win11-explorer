"""
Windows 11 Navigation Sidebar (Left Pane).
Displays Quick Access / Home shortcuts, This PC drives, and Recycle Bin.
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeView, QAbstractItemView, QHeaderView
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt6.QtCore import pyqtSignal, Qt, QModelIndex
from win11_explorer.icons import get_icon
from win11_explorer.file_ops import get_drive_info


class Win11Sidebar(QWidget):
    """Windows 11 Left Navigation Tree Pane."""

    pathSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(230)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tree = QTreeView(self)
        self.tree.setObjectName("SidebarTree")
        self.tree.setHeaderHidden(True)
        self.tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tree.setIndentation(14)
        self.tree.setAnimated(True)

        self.model = QStandardItemModel(self)
        self.tree.setModel(self.model)

        layout.addWidget(self.tree)

        self._populate_sidebar()
        self.tree.clicked.connect(self._on_item_clicked)

        # Expand top sections by default
        self.tree.expandAll()

    def _populate_sidebar(self):
        self.model.clear()
        home = os.path.expanduser("~")

        # 1. Home / Quick Access Header
        home_root = QStandardItem(get_icon("folder-home", size=20), "Home")
        home_root.setData(home, Qt.ItemDataRole.UserRole)
        home_root.setSelectable(True)
        self.model.appendRow(home_root)

        # Quick access pinned items
        quick_items = [
            ("Desktop", os.path.join(home, "Desktop"), "folder-desktop"),
            ("Downloads", os.path.join(home, "Downloads"), "folder-downloads"),
            ("Documents", os.path.join(home, "Documents"), "folder-documents"),
            ("Pictures", os.path.join(home, "Pictures"), "folder-pictures"),
            ("Music", os.path.join(home, "Music"), "folder-music"),
            ("Videos", os.path.join(home, "Videos"), "folder-videos"),
        ]

        for label, path, icon_name in quick_items:
            # Create directory if it doesn't exist
            if not os.path.exists(path):
                try:
                    os.makedirs(path, exist_ok=True)
                except Exception:
                    pass
            item = QStandardItem(get_icon(icon_name, size=20), label)
            item.setData(path, Qt.ItemDataRole.UserRole)
            home_root.appendRow(item)

        # 2. This PC Section
        pc_root = QStandardItem(get_icon("this-pc", size=20), "This PC")
        pc_root.setData("/", Qt.ItemDataRole.UserRole)
        self.model.appendRow(pc_root)

        # Drives
        drives = get_drive_info()
        for d in drives:
            drive_item = QStandardItem(get_icon("drive", size=20), d["name"])
            drive_item.setData(d["path"], Qt.ItemDataRole.UserRole)
            pc_root.appendRow(drive_item)

        # 3. Network Section
        net_root = QStandardItem(get_icon("network", size=20), "Network")
        net_root.setData("/mnt", Qt.ItemDataRole.UserRole)
        self.model.appendRow(net_root)

        # 4. Trash / Recycle Bin
        trash_path = os.path.expanduser("~/.local/share/Trash/files")
        trash_root = QStandardItem(get_icon("trash", size=20), "Recycle Bin")
        trash_root.setData(trash_path, Qt.ItemDataRole.UserRole)
        self.model.appendRow(trash_root)

    def _on_item_clicked(self, index: QModelIndex):
        item = self.model.itemFromIndex(index)
        if item:
            path = item.data(Qt.ItemDataRole.UserRole)
            if path and os.path.exists(path):
                self.pathSelected.emit(path)

    def select_path(self, path: str):
        """Highlight corresponding sidebar item if matched."""
        norm_path = os.path.normpath(path)
        # Search model
        for row in range(self.model.rowCount()):
            root = self.model.item(row)
            if root.data(Qt.ItemDataRole.UserRole) == norm_path:
                self.tree.setCurrentIndex(root.index())
                return
            for child_row in range(root.rowCount()):
                child = root.child(child_row)
                if child.data(Qt.ItemDataRole.UserRole) == norm_path:
                    self.tree.setCurrentIndex(child.index())
                    return
