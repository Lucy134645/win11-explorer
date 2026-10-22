"""
Windows 11 Integrated Titlebar Widget.
Contains tabs, '+' button, draggable region, and authentic Windows 11 caption controls (─, □, ✕).
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QToolButton, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal, Qt, QPoint
from PyQt6.QtGui import QMouseEvent
from win11_explorer.icons import get_icon
from win11_explorer.widgets.tab_bar import Win11TabBar


class Win11CaptionButton(QToolButton):
    """Windows 11 caption control button (Minimize, Maximize, Close)."""

    def __init__(self, icon_name: str, is_close: bool = False, parent=None):
        super().__init__(parent)
        self.is_close = is_close
        self.icon_name = icon_name
        self.setIcon(get_icon(icon_name, size=12))
        self.setFixedSize(46, 38)
        self._apply_style()

    def set_caption_icon(self, icon_name: str):
        self.icon_name = icon_name
        self.setIcon(get_icon(icon_name, size=12))

    def _apply_style(self):
        if self.is_close:
            self.setStyleSheet("""
                QToolButton {
                    background: transparent;
                    border: none;
                    margin: 0px;
                    padding: 0px;
                }
                QToolButton:hover {
                    background-color: #C42B1C;
                    color: #FFFFFF;
                }
                QToolButton:pressed {
                    background-color: #B22619;
                }
            """)
        else:
            self.setStyleSheet("""
                QToolButton {
                    background: transparent;
                    border: none;
                    margin: 0px;
                    padding: 0px;
                }
                QToolButton:hover {
                    background-color: rgba(255, 255, 255, 0.09);
                }
                QToolButton:pressed {
                    background-color: rgba(255, 255, 255, 0.05);
                }
            """)


class Win11TitleBar(QWidget):
    """Unified Windows 11 Titlebar hosting Tabs and Caption Controls."""

    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.parent_window = parent_window
        self.setObjectName("TitleBarContainer")
        self.setFixedHeight(42)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 0, 0, 0)
        layout.setSpacing(0)

        # Tab bar
        self.tab_bar = Win11TabBar(self)
        layout.addWidget(self.tab_bar)

        # Draggable stretch region
        layout.addStretch(1)

        # Caption Controls (Min, Max, Close)
        caption_container = QWidget(self)
        caption_layout = QHBoxLayout(caption_container)
        caption_layout.setContentsMargins(0, 0, 0, 0)
        caption_layout.setSpacing(0)

        self.btn_min = Win11CaptionButton("cap-min", is_close=False, parent=caption_container)
        self.btn_min.clicked.connect(self.parent_window.showMinimized)

        self.btn_max = Win11CaptionButton("cap-max", is_close=False, parent=caption_container)
        self.btn_max.clicked.connect(self._toggle_maximize)

        self.btn_close = Win11CaptionButton("cap-close", is_close=True, parent=caption_container)
        self.btn_close.clicked.connect(self.parent_window.close)

        caption_layout.addWidget(self.btn_min)
        caption_layout.addWidget(self.btn_max)
        caption_layout.addWidget(self.btn_close)

        layout.addWidget(caption_container)

    def _toggle_maximize(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.btn_max.set_caption_icon("cap-max")
        else:
            self.parent_window.showMaximized()
            self.btn_max.set_caption_icon("cap-restore")

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            # Native Wayland / X11 window dragging
            wh = self.parent_window.windowHandle()
            if wh and hasattr(wh, "startSystemMove"):
                wh.startSystemMove()
            event.accept()
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._toggle_maximize()
            event.accept()
        super().mouseDoubleClickEvent(event)
