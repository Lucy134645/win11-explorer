"""
Windows 11 Breadcrumb Address Bar widget.
Features clickable path segments, chevron sibling dropdowns, and an editable line input.
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton, QToolButton,
    QLineEdit, QFrame, QMenu, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QIcon, QAction
from win11_explorer.icons import get_icon


class BreadcrumbAddressBar(QFrame):
    """Windows 11 style interactive breadcrumbs with path editor."""

    pathChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AddressContainer")
        self.setFixedHeight(34)
        self.current_path = ""

        # Outer layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(4, 2, 4, 2)
        self.main_layout.setSpacing(2)

        # Left folder / computer icon
        self.icon_label = QLabel(self)
        self.icon_label.setFixedSize(20, 20)
        self.icon_label.setPixmap(get_icon("folder", size=18).pixmap(18, 18))
        self.main_layout.addWidget(self.icon_label)

        # Breadcrumbs widget container
        self.breadcrumbs_widget = QWidget(self)
        self.breadcrumbs_layout = QHBoxLayout(self.breadcrumbs_widget)
        self.breadcrumbs_layout.setContentsMargins(0, 0, 0, 0)
        self.breadcrumbs_layout.setSpacing(1)
        self.main_layout.addWidget(self.breadcrumbs_widget)

        # Clickable empty space to trigger text edit
        self.empty_clicker = QPushButton(self.breadcrumbs_widget)
        self.empty_clicker.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.empty_clicker.setFlat(True)
        self.empty_clicker.setStyleSheet("border: none; background: transparent;")
        self.empty_clicker.clicked.connect(self.enable_edit_mode)

        # Editable line edit (hidden by default)
        self.edit_line = QLineEdit(self)
        self.edit_line.setObjectName("AddressEdit")
        self.edit_line.returnPressed.connect(self._on_edit_committed)
        self.edit_line.hide()
        self.main_layout.addWidget(self.edit_line)

        # Refresh button inside right of address bar
        self.refresh_btn = QToolButton(self)
        self.refresh_btn.setIcon(get_icon("refresh", size=14))
        self.refresh_btn.setToolTip("Refresh (F5)")
        self.refresh_btn.setFixedSize(24, 24)
        self.refresh_btn.setStyleSheet("""
            QToolButton {
                background: transparent;
                border: none;
                border-radius: 4px;
            }
            QToolButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
        """)
        self.refresh_btn.clicked.connect(lambda: self.pathChanged.emit(self.current_path))
        self.main_layout.addWidget(self.refresh_btn)

    def set_path(self, path: str):
        """Update breadcrumbs display for the given path."""
        path = os.path.abspath(path)
        self.current_path = path
        self.disable_edit_mode()
        self._rebuild_breadcrumbs(path)

    def _rebuild_breadcrumbs(self, path: str):
        # Clear existing breadcrumb widgets except empty_clicker
        while self.breadcrumbs_layout.count() > 0:
            item = self.breadcrumbs_layout.takeAt(0)
            if item.widget() and item.widget() != self.empty_clicker:
                item.widget().deleteLater()

        # Split path into segments
        parts = []
        curr = path
        while True:
            parent, tail = os.path.split(curr)
            if tail:
                parts.insert(0, (tail, curr))
                curr = parent
            else:
                if curr:
                    parts.insert(0, (curr, curr))
                break

        # User friendly replacement for home folder
        home = os.path.expanduser("~")
        built_parts = []
        if path.startswith(home):
            rel = os.path.relpath(path, home)
            built_parts.append(("Home", home))
            if rel != ".":
                acc = home
                for seg in rel.split(os.sep):
                    acc = os.path.join(acc, seg)
                    built_parts.append((seg, acc))
        else:
            built_parts = parts

        for i, (name, target_path) in enumerate(built_parts):
            # Segment button
            btn = QPushButton(name, self.breadcrumbs_widget)
            btn.setFlat(True)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: inherit;
                    border: 1px solid transparent;
                    border-radius: 4px;
                    padding: 2px 7px;
                    font-size: 12px;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                }
            """)
            btn.clicked.connect(lambda checked, p=target_path: self.pathChanged.emit(p))
            self.breadcrumbs_layout.addWidget(btn)

            # Chevron drop-down
            chevron_btn = QToolButton(self.breadcrumbs_widget)
            chevron_btn.setIcon(get_icon("chevron-right", size=10))
            chevron_btn.setFixedSize(16, 20)
            chevron_btn.setStyleSheet("""
                QToolButton {
                    background: transparent;
                    border: none;
                    border-radius: 3px;
                }
                QToolButton:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                }
            """)
            chevron_btn.clicked.connect(lambda checked, p=target_path, b=chevron_btn: self._show_subfolder_menu(p, b))
            self.breadcrumbs_layout.addWidget(chevron_btn)

        # Re-add flexible empty clicker
        self.breadcrumbs_layout.addWidget(self.empty_clicker)

    def _show_subfolder_menu(self, parent_dir: str, anchor_btn: QToolButton):
        """Show dropdown menu with subdirectories of this segment."""
        menu = QMenu(self)
        try:
            entries = sorted(os.scandir(parent_dir), key=lambda e: e.name.lower())
            dirs = [e for e in entries if e.is_dir(follow_symlinks=False) and not e.name.startswith(".")]
            if not dirs:
                action = menu.addAction("No subfolders")
                action.setEnabled(False)
            else:
                for d in dirs[:25]:  # limit to top 25
                    act = menu.addAction(get_icon("folder", size=16), d.name)
                    act.triggered.connect(lambda checked, p=d.path: self.pathChanged.emit(p))
        except Exception as e:
            menu.addAction(f"Error: {e}").setEnabled(False)

        menu.exec(anchor_btn.mapToGlobal(anchor_btn.rect().bottomLeft()))

    def enable_edit_mode(self):
        """Switch from breadcrumbs to editable path input."""
        self.breadcrumbs_widget.hide()
        self.edit_line.setText(self.current_path)
        self.edit_line.show()
        self.edit_line.selectAll()
        self.edit_line.setFocus()

    def disable_edit_mode(self):
        """Switch back to breadcrumbs display."""
        self.edit_line.hide()
        self.breadcrumbs_widget.show()

    def _on_edit_committed(self):
        new_path = self.edit_line.text().strip()
        new_path = os.path.expanduser(new_path)
        if os.path.exists(new_path):
            self.pathChanged.emit(os.path.abspath(new_path))
        self.disable_edit_mode()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape and self.edit_line.isVisible():
            self.disable_edit_mode()
            return
        super().keyPressEvent(event)
