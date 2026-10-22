"""
Windows 11 Navigation Sidebar (Left Pane) with custom styling and capacity bars.
Features left blue accent pill on selection and drive storage progress bars.
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeView, QAbstractItemView, QStyledItemDelegate, QStyle
)
from PyQt6.QtGui import (
    QStandardItemModel, QStandardItem, QIcon, QPainter, QColor, QFont, QPen, QBrush
)
from PyQt6.QtCore import pyqtSignal, Qt, QModelIndex, QRect, QRectF, QSize
from win11_explorer.icons import get_icon
from win11_explorer.file_ops import get_drive_info, format_size


class SidebarItemDelegate(QStyledItemDelegate):
    """Custom delegate painting the Windows 11 left accent pill and drive gauges."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.accent_color = QColor("#60CDFF")
        self.hover_color = QColor(255, 255, 255, 15)
        self.select_color = QColor(255, 255, 255, 22)

    def sizeHint(self, option, index: QModelIndex) -> QSize:
        is_drive = index.data(Qt.ItemDataRole.UserRole + 1)
        if is_drive:
            return QSize(200, 46)  # taller for drive with capacity bar
        return QSize(200, 34)

    def paint(self, painter: QPainter, option, index: QModelIndex):
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = option.rect
        is_selected = bool(option.state & QStyle.StateFlag.State_Selected)
        is_hover = bool(option.state & QStyle.StateFlag.State_MouseOver)
        is_drive = index.data(Qt.ItemDataRole.UserRole + 1)

        # Draw rounded background
        bg_rect = rect.adjusted(4, 2, -4, -2)
        if is_selected:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(self.select_color)
            painter.drawRoundedRect(bg_rect, 5, 5)

            # Draw Windows 11 Left Accent Pill (3px wide cyan pill)
            pill_h = 16
            pill_y = rect.y() + (rect.height() - pill_h) // 2
            pill_rect = QRectF(rect.x() + 1, pill_y, 3, pill_h)
            painter.setBrush(self.accent_color)
            painter.drawRoundedRect(pill_rect, 1.5, 1.5)

        elif is_hover:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(self.hover_color)
            painter.drawRoundedRect(bg_rect, 5, 5)

        # Draw Icon
        icon = index.data(Qt.ItemDataRole.DecorationRole)
        icon_size = 20
        icon_x = rect.x() + 12
        icon_y = rect.y() + (rect.height() - icon_size) // 2
        if is_drive:
            icon_y = rect.y() + 8  # align top for drives
        if icon:
            icon.paint(painter, icon_x, icon_y, icon_size, icon_size)

        # Draw Label Text
        text = index.data(Qt.ItemDataRole.DisplayRole) or ""
        font = painter.font()
        font.setPixelSize(13)
        painter.setFont(font)
        painter.setPen(QColor("#FFFFFF" if is_selected else "#E5E5E5"))

        text_x = icon_x + icon_size + 10
        if is_drive:
            # Main drive title
            painter.drawText(text_x, rect.y() + 18, text)

            # Capacity progress bar & text
            free_bytes = index.data(Qt.ItemDataRole.UserRole + 2) or 0
            total_bytes = index.data(Qt.ItemDataRole.UserRole + 3) or 1
            percent = index.data(Qt.ItemDataRole.UserRole + 4) or 0

            # Progress Bar Track
            bar_w = min(120, rect.width() - text_x - 16)
            bar_h = 3
            bar_y = rect.y() + 26
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor("#404040"))
            painter.drawRoundedRect(QRectF(text_x, bar_y, bar_w, bar_h), 1.5, 1.5)

            # Filled Progress Bar
            fill_w = int(bar_w * (percent / 100.0))
            painter.setBrush(self.accent_color)
            painter.drawRoundedRect(QRectF(text_x, bar_y, fill_w, bar_h), 1.5, 1.5)

            # Free Space Text
            small_font = painter.font()
            small_font.setPixelSize(10)
            painter.setFont(small_font)
            painter.setPen(QColor("#9E9E9E"))
            sub_text = f"{format_size(free_bytes)} free of {format_size(total_bytes)}"
            painter.drawText(text_x, rect.y() + 40, sub_text)

        else:
            text_rect = QRect(text_x, rect.y(), rect.width() - text_x - 6, rect.height())
            painter.drawText(text_rect, int(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft), text)

        painter.restore()


class Win11Sidebar(QWidget):
    """Windows 11 Left Navigation Tree Pane."""

    pathSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(240)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tree = QTreeView(self)
        self.tree.setObjectName("SidebarTree")
        self.tree.setHeaderHidden(True)
        self.tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tree.setIndentation(14)
        self.tree.setAnimated(True)
        self.tree.setItemDelegate(SidebarItemDelegate(self.tree))

        self.model = QStandardItemModel(self)
        self.tree.setModel(self.model)

        layout.addWidget(self.tree)

        self._populate_sidebar()
        self.tree.clicked.connect(self._on_item_clicked)
        self.tree.expandAll()

    def _populate_sidebar(self):
        self.model.clear()
        home = os.path.expanduser("~")

        # 1. Home Section
        home_root = QStandardItem(get_icon("folder-home", size=20), "Home")
        home_root.setData(home, Qt.ItemDataRole.UserRole)
        home_root.setData(False, Qt.ItemDataRole.UserRole + 1)
        self.model.appendRow(home_root)

        quick_items = [
            ("Desktop", os.path.join(home, "Desktop"), "folder-desktop"),
            ("Downloads", os.path.join(home, "Downloads"), "folder-downloads"),
            ("Documents", os.path.join(home, "Documents"), "folder-documents"),
            ("Pictures", os.path.join(home, "Pictures"), "folder-pictures"),
            ("Music", os.path.join(home, "Music"), "folder-music"),
            ("Videos", os.path.join(home, "Videos"), "folder-videos"),
        ]

        for label, path, icon_name in quick_items:
            if not os.path.exists(path):
                try:
                    os.makedirs(path, exist_ok=True)
                except Exception:
                    pass
            item = QStandardItem(get_icon(icon_name, size=20), label)
            item.setData(path, Qt.ItemDataRole.UserRole)
            item.setData(False, Qt.ItemDataRole.UserRole + 1)
            home_root.appendRow(item)

        # 2. This PC Section
        pc_root = QStandardItem(get_icon("this-pc", size=20), "This PC")
        pc_root.setData("THIS_PC", Qt.ItemDataRole.UserRole)
        pc_root.setData(False, Qt.ItemDataRole.UserRole + 1)
        self.model.appendRow(pc_root)

        # Drives
        drives = get_drive_info()
        for d in drives:
            drive_item = QStandardItem(get_icon("drive", size=20), d["name"])
            drive_item.setData(d["path"], Qt.ItemDataRole.UserRole)
            drive_item.setData(True, Qt.ItemDataRole.UserRole + 1)      # is_drive
            drive_item.setData(d["free"], Qt.ItemDataRole.UserRole + 2)  # free
            drive_item.setData(d["total"], Qt.ItemDataRole.UserRole + 3) # total
            drive_item.setData(d["percent"], Qt.ItemDataRole.UserRole + 4) # percent
            pc_root.appendRow(drive_item)

        # 3. Network Section
        net_root = QStandardItem(get_icon("network", size=20), "Network")
        net_root.setData("/mnt", Qt.ItemDataRole.UserRole)
        net_root.setData(False, Qt.ItemDataRole.UserRole + 1)
        self.model.appendRow(net_root)

        # 4. Trash / Recycle Bin
        trash_path = os.path.expanduser("~/.local/share/Trash/files")
        trash_root = QStandardItem(get_icon("trash", size=20), "Recycle Bin")
        trash_root.setData(trash_path, Qt.ItemDataRole.UserRole)
        trash_root.setData(False, Qt.ItemDataRole.UserRole + 1)
        self.model.appendRow(trash_root)

    def _on_item_clicked(self, index: QModelIndex):
        item = self.model.itemFromIndex(index)
        if item:
            path = item.data(Qt.ItemDataRole.UserRole)
            if path:
                self.pathSelected.emit(path)

    def select_path(self, path: str):
        """Highlight corresponding sidebar item if matched."""
        norm_path = os.path.normpath(path)
        for row in range(self.model.rowCount()):
            root = self.model.item(row)
            if root.data(Qt.ItemDataRole.UserRole) == norm_path:
                self.tree.setCurrentIndex(root.index())
                return
            for child_row in range(root.rowCount()):
                child = root.child(child_row)
                if child.data(Qt.ItemDataRole.UserRole) == norm_path:
                    self.tree.setCurrentIndex(child.index())
                    return
