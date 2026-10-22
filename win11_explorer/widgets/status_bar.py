"""
Windows 11 Status Bar widget.
Displays item count, selected items and bytes, and view switcher shortcuts.
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QToolButton, QFrame
)
from PyQt6.QtCore import pyqtSignal, Qt
from win11_explorer.icons import get_icon
from win11_explorer.file_ops import format_size


class Win11StatusBar(QWidget):
    """Windows 11 Bottom Status Bar."""

    viewModeChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                color: #A0A0A0;
                font-size: 12px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(10)

        # Left status text
        self.items_lbl = QLabel("0 items", self)
        layout.addWidget(self.items_lbl)

        self.selected_lbl = QLabel("", self)
        layout.addWidget(self.selected_lbl)

        layout.addStretch()

        # Right quick view buttons
        self.btn_details = QToolButton(self)
        self.btn_details.setIcon(get_icon("view-details", size=14))
        self.btn_details.setToolTip("Details view")
        self.btn_details.setFixedSize(22, 22)
        self.btn_details.setStyleSheet("border: none; border-radius: 3px;")
        self.btn_details.clicked.connect(lambda: self.viewModeChanged.emit("details"))
        layout.addWidget(self.btn_details)

        self.btn_large = QToolButton(self)
        self.btn_large.setIcon(get_icon("view-large", size=14))
        self.btn_large.setToolTip("Large icons")
        self.btn_large.setFixedSize(22, 22)
        self.btn_large.setStyleSheet("border: none; border-radius: 3px;")
        self.btn_large.clicked.connect(lambda: self.viewModeChanged.emit("large"))
        layout.addWidget(self.btn_large)

    def update_status(self, total: int, selected: int, selected_bytes: int):
        self.items_lbl.setText(f"{total} item{'s' if total != 1 else ''}")
        if selected > 0:
            if selected_bytes > 0:
                self.selected_lbl.setText(f"|   {selected} item{'s' if selected != 1 else ''} selected   {format_size(selected_bytes)}")
            else:
                self.selected_lbl.setText(f"|   {selected} item{'s' if selected != 1 else ''} selected")
        else:
            self.selected_lbl.setText("")
