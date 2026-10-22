"""
Windows 11 Tab Bar widget.
Features Fluent tabs with folder icons, close buttons, and a '+' new tab button.
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QTabBar, QToolButton, QStyle, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal, QSize, Qt
from win11_explorer.icons import get_icon


class Win11TabBar(QWidget):
    """Container holding the QTabBar and the '+' new tab button."""

    currentChanged = pyqtSignal(int)
    tabCloseRequested = pyqtSignal(int)
    newTabRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TabBarContainer")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 4, 6, 0)
        layout.setSpacing(4)

        # Tab bar
        self.tab_bar = QTabBar(self)
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.setMovable(True)
        self.tab_bar.setExpanding(False)
        self.tab_bar.setIconSize(QSize(16, 16))
        self.tab_bar.currentChanged.connect(self.currentChanged.emit)
        self.tab_bar.tabCloseRequested.connect(self._on_close_requested)

        layout.addWidget(self.tab_bar)

        # Plus button for new tab
        self.new_tab_btn = QToolButton(self)
        self.new_tab_btn.setIcon(get_icon("plus", size=16))
        self.new_tab_btn.setToolTip("Add new tab (Ctrl+T)")
        self.new_tab_btn.setFixedSize(28, 28)
        self.new_tab_btn.setStyleSheet("""
            QToolButton {
                background: transparent;
                border: 1px solid transparent;
                border-radius: 5px;
                padding: 4px;
                margin-bottom: 2px;
            }
            QToolButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            QToolButton:pressed {
                background: rgba(255, 255, 255, 0.05);
            }
        """)
        self.new_tab_btn.clicked.connect(self.newTabRequested.emit)
        layout.addWidget(self.new_tab_btn, alignment=Qt.AlignmentFlag.AlignVCenter)

        layout.addStretch()

    def addTab(self, icon, title: str) -> int:
        idx = self.tab_bar.addTab(icon, title)
        return idx

    def setTabText(self, index: int, title: str):
        self.tab_bar.setTabText(index, title)

    def setTabIcon(self, index: int, icon):
        self.tab_bar.setTabIcon(index, icon)

    def setTabToolTip(self, index: int, tooltip: str):
        self.tab_bar.setTabToolTip(index, tooltip)

    def currentIndex(self) -> int:
        return self.tab_bar.currentIndex()

    def setCurrentIndex(self, index: int):
        self.tab_bar.setCurrentIndex(index)

    def count(self) -> int:
        return self.tab_bar.count()

    def removeTab(self, index: int):
        self.tab_bar.removeTab(index)

    def _on_close_requested(self, index: int):
        # Always allow if more than 1 tab, or emit to parent window
        self.tabCloseRequested.emit(index)
