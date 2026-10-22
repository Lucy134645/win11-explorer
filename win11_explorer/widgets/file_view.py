"""
Windows 11 Main File View Container.
Supports Details View, Large/Medium/Small Icons Grid View, List View, and Tiles View.
"""

from typing import List, Optional
from PyQt6.QtWidgets import (
    QWidget, QStackedWidget, QTableView, QListView, QVBoxLayout,
    QHeaderView, QAbstractItemView, QMenu, QInputDialog, QMessageBox
)
from PyQt6.QtCore import (
    pyqtSignal, Qt, QModelIndex, QSize, QPoint
)
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut
from win11_explorer.models import FileTableModel, FileItem
from win11_explorer.file_ops import (
    open_with_default, open_terminal, delete_to_trash,
    ExplorerClipboard, ClipboardMode
)
from win11_explorer.widgets.context_menu import Win11ContextMenu
from win11_explorer.widgets.properties_dialog import Win11PropertiesDialog


class Win11FileView(QWidget):
    """File View Manager supporting Details, Grid Icons, List, and Tiles."""

    folderOpened = pyqtSignal(str)
    selectionChanged = pyqtSignal(list)       # list of FileItem
    itemCountChanged = pyqtSignal(int, int, int) # total_items, selected_count, selected_bytes
    refreshRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MainContentArea")

        self.model = FileTableModel(self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.stack = QStackedWidget(self)
        layout.addWidget(self.stack)

        # 1. Details Table View
        self.table_view = QTableView(self)
        self.table_view.setObjectName("DetailsView")
        self.table_view.setModel(self.model)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.table_view.setShowGrid(False)
        self.table_view.setAlternatingRowColors(False)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.horizontalHeader().setHighlightSections(False)
        self.table_view.horizontalHeader().setStretchLastSection(False)
        self.table_view.setSortingEnabled(True)
        self.table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        # Configure column widths
        header = self.table_view.horizontalHeader()
        header.resizeSection(0, 320)  # Name
        header.resizeSection(1, 150)  # Date
        header.resizeSection(2, 140)  # Type
        header.resizeSection(3, 100)  # Size

        # 2. Icons View (Large / Medium / Small)
        self.icons_view = QListView(self)
        self.icons_view.setObjectName("IconsView")
        self.icons_view.setModel(self.model)
        self.icons_view.setViewMode(QListView.ViewMode.IconMode)
        self.icons_view.setResizeMode(QListView.ResizeMode.Adjust)
        self.icons_view.setMovement(QListView.Movement.Static)
        self.icons_view.setWordWrap(True)
        self.icons_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.icons_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._set_icon_size("large")

        # 3. List View
        self.list_view = QListView(self)
        self.list_view.setObjectName("IconsView")
        self.list_view.setModel(self.model)
        self.list_view.setViewMode(QListView.ViewMode.ListMode)
        self.list_view.setMovement(QListView.Movement.Static)
        self.list_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.list_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        # Add views to stack
        self.stack.addWidget(self.table_view)  # index 0: details
        self.stack.addWidget(self.icons_view)  # index 1: icons
        self.stack.addWidget(self.list_view)   # index 2: list

        # Connect signals
        for view in [self.table_view, self.icons_view, self.list_view]:
            view.doubleClicked.connect(self._on_item_double_clicked)
            view.customContextMenuRequested.connect(self._on_context_menu)
            view.selectionModel().selectionChanged.connect(self._on_selection_changed)

        # Shortcuts
        self._setup_shortcuts()

    def _setup_shortcuts(self):
        # Delete shortcut
        del_sc = QShortcut(QKeySequence.StandardKey.Delete, self)
        del_sc.activated.connect(self.delete_selected)

        # Rename shortcut
        f2_sc = QShortcut(QKeySequence("F2"), self)
        f2_sc.activated.connect(self.rename_selected)

        # Enter to open
        enter_sc = QShortcut(QKeySequence("Return"), self)
        enter_sc.activated.connect(self.open_selected)

    def set_directory(self, path: str):
        self.model.load_directory(path)
        self._update_counts()

    def set_show_hidden(self, show: bool):
        self.model.set_show_hidden(show)
        self._update_counts()

    def set_search_filter(self, filter_text: str):
        self.model.set_search_filter(filter_text)
        self._update_counts()

    def sort_by(self, col: int, order: Qt.SortOrder):
        self.model.sort(col, order)

    def set_view_mode(self, mode: str):
        if mode == "details":
            self.stack.setCurrentIndex(0)
        elif mode in ["large", "medium", "small", "tiles"]:
            self._set_icon_size(mode)
            self.stack.setCurrentIndex(1)
        elif mode == "list":
            self.stack.setCurrentIndex(2)

    def _set_icon_size(self, mode: str):
        if mode == "large":
            self.icons_view.setIconSize(QSize(64, 64))
            self.icons_view.setGridSize(QSize(96, 100))
        elif mode == "medium":
            self.icons_view.setIconSize(QSize(48, 48))
            self.icons_view.setGridSize(QSize(80, 84))
        elif mode == "small":
            self.icons_view.setIconSize(QSize(32, 32))
            self.icons_view.setGridSize(QSize(64, 68))
        elif mode == "tiles":
            self.icons_view.setIconSize(QSize(40, 40))
            self.icons_view.setGridSize(QSize(180, 60))

    def _get_active_view(self) -> QAbstractItemView:
        return self.stack.currentWidget()

    def get_selected_items(self) -> List[FileItem]:
        view = self._get_active_view()
        selected_indexes = view.selectionModel().selectedRows(0)
        items = []
        for idx in selected_indexes:
            item = self.model.get_item(idx.row())
            if item:
                items.append(item)
        return items

    def _on_selection_changed(self):
        items = self.get_selected_items()
        self.selectionChanged.emit(items)
        self._update_counts()

    def _update_counts(self):
        total = self.model.rowCount()
        selected = self.get_selected_items()
        selected_count = len(selected)
        selected_bytes = sum(it.size for it in selected if not it.is_dir)
        self.itemCountChanged.emit(total, selected_count, selected_bytes)

    def _on_item_double_clicked(self, index: QModelIndex):
        item = self.model.get_item(index.row())
        if not item:
            return
        if item.is_dir:
            self.folderOpened.emit(item.path)
        else:
            open_with_default(item.path)

    def open_selected(self):
        items = self.get_selected_items()
        for it in items:
            if it.is_dir:
                self.folderOpened.emit(it.path)
                break
            else:
                open_with_default(it.path)

    def select_all(self):
        view = self._get_active_view()
        view.selectAll()

    def _on_context_menu(self, pos: QPoint):
        view = self._get_active_view()
        index = view.indexAt(pos)
        has_sel = index.isValid() or bool(self.get_selected_items())

        menu = Win11ContextMenu(has_selection=has_sel, parent=self)
        
        # Connect context menu actions
        menu.openRequested.connect(self.open_selected)
        menu.cutRequested.connect(self.cut_selected)
        menu.copyRequested.connect(self.copy_selected)
        menu.renameRequested.connect(self.rename_selected)
        menu.deleteRequested.connect(self.delete_selected)
        menu.copyPathRequested.connect(self.copy_selected_paths)
        menu.terminalRequested.connect(self.open_terminal_here)
        menu.propertiesRequested.connect(self.show_properties)
        menu.refreshRequested.connect(self.refreshRequested.emit)

        menu.exec(view.mapToGlobal(pos))

    def cut_selected(self):
        items = self.get_selected_items()
        if items:
            ExplorerClipboard.set_cut([it.path for it in items])

    def copy_selected(self):
        items = self.get_selected_items()
        if items:
            ExplorerClipboard.set_copy([it.path for it in items])

    def rename_selected(self):
        items = self.get_selected_items()
        if not items:
            return
        target = items[0]
        new_name, ok = QInputDialog.getText(
            self, "Rename", "Enter new name:", text=target.name
        )
        if ok and new_name and new_name != target.name:
            import os
            new_path = os.path.join(os.path.dirname(target.path), new_name)
            try:
                os.rename(target.path, new_path)
                self.refreshRequested.emit()
            except Exception as e:
                QMessageBox.critical(self, "Rename Error", str(e))

    def delete_selected(self):
        items = self.get_selected_items()
        if not items:
            return
        count = len(items)
        msg = f"Are you sure you want to move {count} item{'s' if count > 1 else ''} to the Recycle Bin?"
        res = QMessageBox.question(self, "Delete", msg, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if res == QMessageBox.StandardButton.Yes:
            paths = [it.path for it in items]
            delete_to_trash(paths)
            self.refreshRequested.emit()

    def copy_selected_paths(self):
        from PyQt6.QtWidgets import QApplication
        items = self.get_selected_items()
        if items:
            text = "\n".join(it.path for it in items)
            QApplication.clipboard().setText(text)

    def open_terminal_here(self):
        items = self.get_selected_items()
        if items and items[0].is_dir:
            open_terminal(items[0].path)
        else:
            open_terminal(self.model.current_directory)

    def show_properties(self):
        items = self.get_selected_items()
        path = items[0].path if items else self.model.current_directory
        dlg = Win11PropertiesDialog(path, self)
        dlg.exec()
