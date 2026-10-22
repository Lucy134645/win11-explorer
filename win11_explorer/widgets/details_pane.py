"""
Windows 11 Details Pane (Right Sidebar).
Displays large preview, metadata, dimensions, and attributes for selected items.
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
from win11_explorer.icons import get_icon
from win11_explorer.file_ops import (
    format_size, format_datetime, get_file_type_description, get_file_icon_name
)


class Win11DetailsPane(QWidget):
    """Windows 11 Right-hand Details & Properties Pane."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(260)
        self.setStyleSheet("""
            QWidget {
                background-color: #202020;
                border-left: 1px solid rgba(255, 255, 255, 0.07);
                color: #FFFFFF;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(12)

        # Header title
        title_lbl = QLabel("Details", self)
        title_lbl.setStyleSheet("font-weight: 600; font-size: 14px; color: #E0E0E0;")
        layout.addWidget(title_lbl)

        # Large icon centered
        self.icon_lbl = QLabel(self)
        self.icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_lbl.setPixmap(get_icon("folder", size=72).pixmap(72, 72))
        layout.addWidget(self.icon_lbl)

        # File name
        self.name_lbl = QLabel("Select an item", self)
        self.name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_lbl.setStyleSheet("font-weight: 600; font-size: 14px; color: #FFFFFF;")
        self.name_lbl.setWordWrap(True)
        layout.addWidget(self.name_lbl)

        # Divider
        div = QFrame(self)
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet("background-color: rgba(255, 255, 255, 0.08);")
        layout.addWidget(div)

        # Details list
        self.type_val = self._create_row(layout, "Type:")
        self.size_val = self._create_row(layout, "Size:")
        self.date_val = self._create_row(layout, "Date modified:")
        self.path_val = self._create_row(layout, "Folder path:")

        layout.addStretch()

    def _create_row(self, parent_layout, label_text: str) -> QLabel:
        vbox = QVBoxLayout()
        vbox.setSpacing(2)
        lbl = QLabel(label_text, self)
        lbl.setStyleSheet("color: #8A8886; font-size: 11px;")
        val = QLabel("-", self)
        val.setStyleSheet("color: #E0E0E0; font-size: 12px;")
        val.setWordWrap(True)
        vbox.addWidget(lbl)
        vbox.addWidget(val)
        parent_layout.addLayout(vbox)
        return val

    def update_item(self, path: str = None):
        if not path or not os.path.exists(path):
            self.name_lbl.setText("Select an item to see details")
            self.icon_lbl.setPixmap(get_icon("folder", size=72).pixmap(72, 72))
            self.type_val.setText("-")
            self.size_val.setText("-")
            self.date_val.setText("-")
            self.path_val.setText("-")
            return

        is_dir = os.path.isdir(path)
        icon_name = get_file_icon_name(path, is_dir)
        self.icon_lbl.setPixmap(get_icon(icon_name, size=72).pixmap(72, 72))
        self.name_lbl.setText(os.path.basename(path) or path)

        try:
            st = os.stat(path)
            size_str = format_size(st.st_size) if not is_dir else "-"
            date_str = format_datetime(st.st_mtime)
        except Exception:
            size_str = "-"
            date_str = "-"

        self.type_val.setText(get_file_type_description(path, is_dir))
        self.size_val.setText(size_str)
        self.date_val.setText(date_str)
        self.path_val.setText(os.path.dirname(path))
