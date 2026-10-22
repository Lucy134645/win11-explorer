"""
Windows 11 Context Menu widget.
Replicates the Windows 11 floating rounded context menu with top horizontal quick action buttons.
"""

from PyQt6.QtWidgets import (
    QMenu, QWidget, QHBoxLayout, QToolButton, QWidgetAction
)
from PyQt6.QtCore import pyqtSignal, QSize, Qt
from win11_explorer.icons import get_icon


class Win11ContextMenu(QMenu):
    """Windows 11 Modern Context Menu with top action bar."""

    cutRequested = pyqtSignal()
    copyRequested = pyqtSignal()
    renameRequested = pyqtSignal()
    shareRequested = pyqtSignal()
    deleteRequested = pyqtSignal()
    openRequested = pyqtSignal()
    terminalRequested = pyqtSignal()
    copyPathRequested = pyqtSignal()
    propertiesRequested = pyqtSignal()
    newFolderRequested = pyqtSignal()
    newFileRequested = pyqtSignal()
    refreshRequested = pyqtSignal()

    def __init__(self, has_selection: bool = True, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        if has_selection:
            # 1. Top Quick Action Bar (Cut, Copy, Rename, Share, Delete)
            top_bar_action = QWidgetAction(self)
            top_bar_widget = QWidget(self)
            top_layout = QHBoxLayout(top_bar_widget)
            top_layout.setContentsMargins(6, 4, 6, 4)
            top_layout.setSpacing(6)

            cut_btn = self._make_quick_btn("cut", "Cut (Ctrl+X)", self.cutRequested)
            copy_btn = self._make_quick_btn("copy", "Copy (Ctrl+C)", self.copyRequested)
            rename_btn = self._make_quick_btn("rename", "Rename (F2)", self.renameRequested)
            share_btn = self._make_quick_btn("share", "Share", self.shareRequested)
            delete_btn = self._make_quick_btn("delete", "Delete (Del)", self.deleteRequested)

            top_layout.addWidget(cut_btn)
            top_layout.addWidget(copy_btn)
            top_layout.addWidget(rename_btn)
            top_layout.addWidget(share_btn)
            top_layout.addWidget(delete_btn)

            top_bar_action.setDefaultWidget(top_bar_widget)
            self.addAction(top_bar_action)
            self.addSeparator()

            # 2. Main item actions
            act_open = self.addAction("Open")
            act_open.triggered.connect(self.openRequested.emit)

            act_term = self.addAction(get_icon("terminal", size=18), "Open in Terminal")
            act_term.triggered.connect(self.terminalRequested.emit)

            act_path = self.addAction(get_icon("copy", size=18), "Copy as path")
            act_path.setShortcut("Ctrl+Shift+C")
            act_path.triggered.connect(self.copyPathRequested.emit)

            self.addSeparator()

            act_props = self.addAction(get_icon("properties", size=18), "Properties")
            act_props.setShortcut("Alt+Enter")
            act_props.triggered.connect(self.propertiesRequested.emit)

        else:
            # Empty area right-click menu
            act_refresh = self.addAction(get_icon("refresh", size=18), "Refresh")
            act_refresh.setShortcut("F5")
            act_refresh.triggered.connect(self.refreshRequested.emit)

            self.addSeparator()

            new_menu = self.addMenu(get_icon("new", size=18), "New")
            act_new_folder = new_menu.addAction(get_icon("folder", size=18), "Folder")
            act_new_folder.setShortcut("Ctrl+Shift+N")
            act_new_folder.triggered.connect(self.newFolderRequested.emit)

            act_new_file = new_menu.addAction(get_icon("file-text", size=18), "Text Document")
            act_new_file.triggered.connect(self.newFileRequested.emit)

            self.addSeparator()

            act_term = self.addAction(get_icon("terminal", size=18), "Open in Terminal")
            act_term.triggered.connect(self.terminalRequested.emit)

            self.addSeparator()

            act_props = self.addAction(get_icon("properties", size=18), "Properties")
            act_props.triggered.connect(self.propertiesRequested.emit)

    def _make_quick_btn(self, icon_name: str, tooltip: str, signal: pyqtSignal) -> QToolButton:
        btn = QToolButton(self)
        btn.setIcon(get_icon(icon_name, size=16))
        btn.setToolTip(tooltip)
        btn.setFixedSize(30, 30)
        btn.setStyleSheet("""
            QToolButton {
                background: transparent;
                border: 1px solid transparent;
                border-radius: 5px;
                padding: 4px;
            }
            QToolButton:hover {
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.08);
            }
        """)
        btn.clicked.connect(lambda: (signal.emit(), self.close()))
        return btn
