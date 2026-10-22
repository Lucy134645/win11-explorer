"""
Windows 11 Navigation Bar widget.
Contains Back, Forward, Up, Refresh, Breadcrumb Address Bar, and Search Box.
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QToolButton, QLineEdit, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal, QSize, Qt
from win11_explorer.icons import get_icon
from win11_explorer.widgets.breadcrumb import BreadcrumbAddressBar


class Win11NavBar(QWidget):
    """Windows 11 Navigation bar containing nav buttons, address bar, and search."""

    backRequested = pyqtSignal()
    forwardRequested = pyqtSignal()
    upRequested = pyqtSignal()
    refreshRequested = pyqtSignal()
    pathChanged = pyqtSignal(str)
    searchChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("NavBar")
        self.setFixedHeight(46)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)

        # Back button
        self.back_btn = QToolButton(self)
        self.back_btn.setIcon(get_icon("nav-back", size=18))
        self.back_btn.setToolTip("Back (Alt+Left Arrow)")
        self.back_btn.setFixedSize(32, 32)
        self.back_btn.clicked.connect(self.backRequested.emit)
        self.back_btn.setEnabled(False)
        layout.addWidget(self.back_btn)

        # Forward button
        self.forward_btn = QToolButton(self)
        self.forward_btn.setIcon(get_icon("nav-forward", size=18))
        self.forward_btn.setToolTip("Forward (Alt+Right Arrow)")
        self.forward_btn.setFixedSize(32, 32)
        self.forward_btn.clicked.connect(self.forwardRequested.emit)
        self.forward_btn.setEnabled(False)
        layout.addWidget(self.forward_btn)

        # Up button
        self.up_btn = QToolButton(self)
        self.up_btn.setIcon(get_icon("nav-up", size=18))
        self.up_btn.setToolTip("Up (Alt+Up Arrow)")
        self.up_btn.setFixedSize(32, 32)
        self.up_btn.clicked.connect(self.upRequested.emit)
        layout.addWidget(self.up_btn)

        # Breadcrumbs address bar
        self.address_bar = BreadcrumbAddressBar(self)
        self.address_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.address_bar.pathChanged.connect(self.pathChanged.emit)
        layout.addWidget(self.address_bar)

        # Search Box
        self.search_box = QLineEdit(self)
        self.search_box.setObjectName("SearchBox")
        self.search_box.setPlaceholderText("Search")
        self.search_box.setFixedWidth(240)
        self.search_box.setFixedHeight(34)
        self.search_box.setClearButtonEnabled(True)
        self.search_box.textChanged.connect(self.searchChanged.emit)

        # Magnifying glass search icon action
        search_icon = get_icon("search", size=16)
        self.search_box.addAction(search_icon, QLineEdit.ActionPosition.LeadingPosition)

        layout.addWidget(self.search_box)

    def set_path(self, path: str):
        self.address_bar.set_path(path)
        folder_name = os.path.basename(path) or path
        self.search_box.setPlaceholderText(f"Search {folder_name}")

    def update_nav_buttons(self, can_back: bool, can_forward: bool, can_up: bool):
        self.back_btn.setEnabled(can_back)
        self.forward_btn.setEnabled(can_forward)
        self.up_btn.setEnabled(can_up)
