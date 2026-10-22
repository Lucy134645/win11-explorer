"""
Windows 11 "This PC" dedicated view.
Renders the authentic Folders group and Devices & drives group with capacity bars.
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal, Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QFont, QMouseEvent
from win11_explorer.icons import get_icon
from win11_explorer.file_ops import get_drive_info, format_size


class FolderCard(QFrame):
    """Tile card for Special Folders in This PC."""

    clicked = pyqtSignal(str)

    def __init__(self, name: str, path: str, icon_name: str, parent=None):
        super().__init__(parent)
        self.path = path
        self.setFixedSize(220, 56)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 6px;
            }
            QFrame:hover {
                background-color: rgba(255, 255, 255, 0.09);
                border: 1px solid rgba(255, 255, 255, 0.12);
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        icon_lbl = QLabel(self)
        icon_lbl.setPixmap(get_icon(icon_name, size=36).pixmap(36, 36))
        layout.addWidget(icon_lbl)

        title_lbl = QLabel(name, self)
        title_lbl.setStyleSheet("color: #FFFFFF; font-weight: 500; font-size: 13px; border: none; background: transparent;")
        layout.addWidget(title_lbl)
        layout.addStretch()

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.path)


class DriveCard(QFrame):
    """Tile card for Drives in This PC with progress bar."""

    clicked = pyqtSignal(str)

    def __init__(self, drive_data: dict, parent=None):
        super().__init__(parent)
        self.path = drive_data["path"]
        self.setFixedSize(270, 72)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 6px;
            }
            QFrame:hover {
                background-color: rgba(255, 255, 255, 0.09);
                border: 1px solid rgba(255, 255, 255, 0.12);
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        icon_lbl = QLabel(self)
        icon_lbl.setPixmap(get_icon("drive", size=40).pixmap(40, 40))
        icon_lbl.setStyleSheet("border: none; background: transparent;")
        layout.addWidget(icon_lbl)

        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(4)

        title_lbl = QLabel(drive_data["name"], self)
        title_lbl.setStyleSheet("color: #FFFFFF; font-weight: 500; font-size: 13px; border: none; background: transparent;")
        info_layout.addWidget(title_lbl)

        # Storage capacity bar
        bar_bg = QFrame(self)
        bar_bg.setFixedHeight(6)
        bar_bg.setFixedWidth(180)
        percent = drive_data["percent"]
        bar_color = "#0078D4" if percent < 90 else "#D13438"
        bar_bg.setStyleSheet(f"""
            QFrame {{
                background-color: #383838;
                border-radius: 3px;
                border: none;
            }}
        """)

        bar_fill = QFrame(bar_bg)
        bar_fill.setFixedHeight(6)
        bar_fill.setFixedWidth(int(180 * (percent / 100.0)))
        bar_fill.setStyleSheet(f"""
            QFrame {{
                background-color: {bar_color};
                border-radius: 3px;
                border: none;
            }}
        """)
        info_layout.addWidget(bar_bg)

        # Subtext
        free_str = format_size(drive_data["free"])
        total_str = format_size(drive_data["total"])
        sub_lbl = QLabel(f"{free_str} free of {total_str}", self)
        sub_lbl.setStyleSheet("color: #9D9D9D; font-size: 11px; border: none; background: transparent;")
        info_layout.addWidget(sub_lbl)

        layout.addLayout(info_layout)
        layout.addStretch()

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.path)


class Win11ThisPCView(QWidget):
    """Windows 11 This PC view."""

    folderOpened = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MainContentArea")

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        container.setStyleSheet("background-color: #191919;")
        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(24, 20, 24, 20)
        self.layout.setSpacing(24)

        # 1. Folders Section
        self._build_folders_section()

        # 2. Devices and drives Section
        self._build_drives_section()

        self.layout.addStretch()
        scroll.setWidget(container)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def _build_folders_section(self):
        header_layout = QHBoxLayout()
        chevron = QLabel("˅", self)
        chevron.setStyleSheet("color: #9D9D9D; font-size: 11px;")
        lbl = QLabel("Folders (6)", self)
        lbl.setStyleSheet("color: #E0E0E0; font-weight: 600; font-size: 13px;")
        header_layout.addWidget(chevron)
        header_layout.addWidget(lbl)
        header_layout.addStretch()
        self.layout.addLayout(header_layout)

        grid = QGridLayout()
        grid.setSpacing(12)

        home = os.path.expanduser("~")
        folders = [
            ("Desktop", os.path.join(home, "Desktop"), "folder-desktop"),
            ("Downloads", os.path.join(home, "Downloads"), "folder-downloads"),
            ("Documents", os.path.join(home, "Documents"), "folder-documents"),
            ("Pictures", os.path.join(home, "Pictures"), "folder-pictures"),
            ("Music", os.path.join(home, "Music"), "folder-music"),
            ("Videos", os.path.join(home, "Videos"), "folder-videos"),
        ]

        for i, (name, path, icon_name) in enumerate(folders):
            card = FolderCard(name, path, icon_name, self)
            card.clicked.connect(self.folderOpened.emit)
            row = i // 3
            col = i % 3
            grid.addWidget(card, row, col)

        self.layout.addLayout(grid)

    def _build_drives_section(self):
        drives = get_drive_info()
        header_layout = QHBoxLayout()
        chevron = QLabel("˅", self)
        chevron.setStyleSheet("color: #9D9D9D; font-size: 11px;")
        lbl = QLabel(f"Devices and drives ({len(drives)})", self)
        lbl.setStyleSheet("color: #E0E0E0; font-weight: 600; font-size: 13px;")
        header_layout.addWidget(chevron)
        header_layout.addWidget(lbl)
        header_layout.addStretch()
        self.layout.addLayout(header_layout)

        grid = QGridLayout()
        grid.setSpacing(12)

        for i, d in enumerate(drives):
            card = DriveCard(d, self)
            card.clicked.connect(self.folderOpened.emit)
            row = i // 2
            col = i % 2
            grid.addWidget(card, row, col)

        self.layout.addLayout(grid)
