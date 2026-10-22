"""
Windows 11 Command Bar (Ribbon) widget.
Includes New button with dropdown, Cut/Copy/Paste/Rename/Share/Delete action buttons,
Sort dropdown, View options dropdown, and More (...) menu.
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QToolButton, QMenu, QFrame, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal, QSize, Qt
from PyQt6.QtGui import QAction, QActionGroup
from win11_explorer.icons import get_icon


class Win11CommandBar(QWidget):
    """Windows 11 Fluent Command Bar with actions and dropdown menus."""

    newFolderRequested = pyqtSignal()
    newFileRequested = pyqtSignal()
    openTerminalRequested = pyqtSignal()
    cutRequested = pyqtSignal()
    copyRequested = pyqtSignal()
    pasteRequested = pyqtSignal()
    renameRequested = pyqtSignal()
    shareRequested = pyqtSignal()
    deleteRequested = pyqtSignal()
    sortRequested = pyqtSignal(int, Qt.SortOrder)  # column_idx, order
    viewModeRequested = pyqtSignal(str)           # "details", "large", "medium", "small", "list", "tiles"
    toggleHiddenRequested = pyqtSignal(bool)
    selectAllRequested = pyqtSignal()
    copyPathRequested = pyqtSignal()
    propertiesRequested = pyqtSignal()
    toggleThemeRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CommandBar")
        self.setFixedHeight(46)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 10, 4)
        layout.setSpacing(4)

        # 1. New Button with Dropdown
        self.new_btn = QToolButton(self)
        self.new_btn.setObjectName("NewButton")
        self.new_btn.setIcon(get_icon("new", size=18))
        self.new_btn.setText(" New")
        self.new_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.new_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self._setup_new_menu()
        layout.addWidget(self.new_btn)

        layout.addWidget(self._create_separator())

        # 2. File Action Icon Buttons
        self.cut_btn = self._create_icon_btn("cut", "Cut (Ctrl+X)", self.cutRequested)
        self.copy_btn = self._create_icon_btn("copy", "Copy (Ctrl+C)", self.copyRequested)
        self.paste_btn = self._create_icon_btn("paste", "Paste (Ctrl+V)", self.pasteRequested)
        self.rename_btn = self._create_icon_btn("rename", "Rename (F2)", self.renameRequested)
        self.share_btn = self._create_icon_btn("share", "Share", self.shareRequested)
        self.delete_btn = self._create_icon_btn("delete", "Delete (Del)", self.deleteRequested)

        layout.addWidget(self.cut_btn)
        layout.addWidget(self.copy_btn)
        layout.addWidget(self.paste_btn)
        layout.addWidget(self.rename_btn)
        layout.addWidget(self.share_btn)
        layout.addWidget(self.delete_btn)

        layout.addWidget(self._create_separator())

        # 3. Sort Dropdown
        self.sort_btn = QToolButton(self)
        self.sort_btn.setIcon(get_icon("sort", size=16))
        self.sort_btn.setText(" Sort")
        self.sort_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.sort_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self._setup_sort_menu()
        layout.addWidget(self.sort_btn)

        # 4. View Dropdown
        self.view_btn = QToolButton(self)
        self.view_btn.setIcon(get_icon("view", size=16))
        self.view_btn.setText(" View")
        self.view_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.view_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self._setup_view_menu()
        layout.addWidget(self.view_btn)

        layout.addWidget(self._create_separator())

        # 5. More (...) Menu
        self.more_btn = QToolButton(self)
        self.more_btn.setIcon(get_icon("more", size=16))
        self.more_btn.setToolTip("See more")
        self.more_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self._setup_more_menu()
        layout.addWidget(self.more_btn)

        layout.addStretch()

    def _create_separator(self) -> QFrame:
        sep = QFrame(self)
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setFixedHeight(22)
        sep.setStyleSheet("background-color: rgba(255, 255, 255, 0.1); margin: 0 4px;")
        return sep

    def _create_icon_btn(self, icon_name: str, tooltip: str, signal: pyqtSignal) -> QToolButton:
        btn = QToolButton(self)
        btn.setIcon(get_icon(icon_name, size=16))
        btn.setToolTip(tooltip)
        btn.setFixedSize(32, 32)
        btn.clicked.connect(signal.emit)
        return btn

    def _setup_new_menu(self):
        menu = QMenu(self.new_btn)
        act_folder = menu.addAction(get_icon("folder", size=18), "Folder")
        act_folder.setShortcut("Ctrl+Shift+N")
        act_folder.triggered.connect(self.newFolderRequested.emit)

        act_file = menu.addAction(get_icon("file-text", size=18), "Text Document")
        act_file.triggered.connect(self.newFileRequested.emit)

        menu.addSeparator()
        act_term = menu.addAction(get_icon("terminal", size=18), "Terminal")
        act_term.triggered.connect(self.openTerminalRequested.emit)

        self.new_btn.setMenu(menu)

    def _setup_sort_menu(self):
        menu = QMenu(self.sort_btn)
        
        grp_col = QActionGroup(menu)
        grp_col.setExclusive(True)

        act_name = menu.addAction("Name")
        act_name.setCheckable(True)
        act_name.setChecked(True)
        grp_col.addAction(act_name)

        act_date = menu.addAction("Date modified")
        act_date.setCheckable(True)
        grp_col.addAction(act_date)

        act_type = menu.addAction("Type")
        act_type.setCheckable(True)
        grp_col.addAction(act_type)

        act_size = menu.addAction("Size")
        act_size.setCheckable(True)
        grp_col.addAction(act_size)

        menu.addSeparator()

        grp_order = QActionGroup(menu)
        grp_order.setExclusive(True)

        act_asc = menu.addAction("Ascending")
        act_asc.setCheckable(True)
        act_asc.setChecked(True)
        grp_order.addAction(act_asc)

        act_desc = menu.addAction("Descending")
        act_desc.setCheckable(True)
        grp_order.addAction(act_desc)

        def emit_sort():
            col = 0
            if act_date.isChecked():
                col = 1
            elif act_type.isChecked():
                col = 2
            elif act_size.isChecked():
                col = 3
            order = Qt.SortOrder.AscendingOrder if act_asc.isChecked() else Qt.SortOrder.DescendingOrder
            self.sortRequested.emit(col, order)

        act_name.triggered.connect(emit_sort)
        act_date.triggered.connect(emit_sort)
        act_type.triggered.connect(emit_sort)
        act_size.triggered.connect(emit_sort)
        act_asc.triggered.connect(emit_sort)
        act_desc.triggered.connect(emit_sort)

        self.sort_btn.setMenu(menu)

    def _setup_view_menu(self):
        menu = QMenu(self.view_btn)

        grp_view = QActionGroup(menu)
        grp_view.setExclusive(True)

        act_large = menu.addAction(get_icon("view-large", size=16), "Large icons")
        act_large.setCheckable(True)
        grp_view.addAction(act_large)

        act_medium = menu.addAction(get_icon("view-large", size=16), "Medium icons")
        act_medium.setCheckable(True)
        grp_view.addAction(act_medium)

        act_small = menu.addAction(get_icon("view-large", size=16), "Small icons")
        act_small.setCheckable(True)
        grp_view.addAction(act_small)

        act_list = menu.addAction(get_icon("view-list", size=16), "List")
        act_list.setCheckable(True)
        grp_view.addAction(act_list)

        act_details = menu.addAction(get_icon("view-details", size=16), "Details")
        act_details.setCheckable(True)
        act_details.setChecked(True)
        grp_view.addAction(act_details)

        act_tiles = menu.addAction(get_icon("view-tiles", size=16), "Tiles")
        act_tiles.setCheckable(True)
        grp_view.addAction(act_tiles)

        act_large.triggered.connect(lambda: self.viewModeRequested.emit("large"))
        act_medium.triggered.connect(lambda: self.viewModeRequested.emit("medium"))
        act_small.triggered.connect(lambda: self.viewModeRequested.emit("small"))
        act_list.triggered.connect(lambda: self.viewModeRequested.emit("list"))
        act_details.triggered.connect(lambda: self.viewModeRequested.emit("details"))
        act_tiles.triggered.connect(lambda: self.viewModeRequested.emit("tiles"))

        menu.addSeparator()

        # Hidden items toggle
        self.act_hidden = menu.addAction("Hidden items")
        self.act_hidden.setCheckable(True)
        self.act_hidden.setChecked(False)
        self.act_hidden.toggled.connect(self.toggleHiddenRequested.emit)

        self.view_btn.setMenu(menu)

    def _setup_more_menu(self):
        menu = QMenu(self.more_btn)

        act_term = menu.addAction(get_icon("terminal", size=18), "Open in Terminal")
        act_term.triggered.connect(self.openTerminalRequested.emit)

        act_copy_path = menu.addAction(get_icon("copy", size=18), "Copy as path")
        act_copy_path.triggered.connect(self.copyPathRequested.emit)

        menu.addSeparator()

        act_all = menu.addAction("Select all")
        act_all.setShortcut("Ctrl+A")
        act_all.triggered.connect(self.selectAllRequested.emit)

        menu.addSeparator()

        act_theme = menu.addAction(get_icon("theme", size=18), "Toggle Dark / Light Theme")
        act_theme.triggered.connect(self.toggleThemeRequested.emit)

        act_props = menu.addAction(get_icon("properties", size=18), "Properties")
        act_props.triggered.connect(self.propertiesRequested.emit)

        self.more_btn.setMenu(menu)

    def update_action_states(self, has_selection: bool, can_paste: bool):
        self.cut_btn.setEnabled(has_selection)
        self.copy_btn.setEnabled(has_selection)
        self.rename_btn.setEnabled(has_selection)
        self.share_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        self.paste_btn.setEnabled(can_paste)
