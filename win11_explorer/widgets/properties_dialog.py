"""
Windows 11 Properties Dialog.
Faithfully recreates the Windows File / Folder Properties dialog.
"""

import os
import stat
from datetime import datetime
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QLineEdit, QFrame, QCheckBox, QPushButton, QSizePolicy
)
from PyQt6.QtCore import Qt
from win11_explorer.icons import get_icon
from win11_explorer.file_ops import (
    format_size, format_datetime, get_file_type_description, get_file_icon_name
)


class Win11PropertiesDialog(QDialog):
    """Windows 11 File / Folder Properties window."""

    def __init__(self, path: str, parent=None):
        super().__init__(parent)
        self.path = os.path.abspath(path)
        self.is_dir = os.path.isdir(self.path)
        base_name = os.path.basename(self.path) or self.path

        self.setWindowTitle(f"{base_name} Properties")
        self.setFixedSize(380, 480)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(12)

        # Tab Widget
        tabs = QTabWidget(self)
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 6px;
                background-color: transparent;
                top: -1px;
            }
        """)

        # General Tab
        gen_tab = self._create_general_tab()
        tabs.addTab(gen_tab, "General")

        # Permissions Tab
        perm_tab = self._create_permissions_tab()
        tabs.addTab(perm_tab, "Security")

        layout.addWidget(tabs)

        # Bottom buttons: OK, Cancel, Apply
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        ok_btn = QPushButton("OK", self)
        ok_btn.setFixedWidth(75)
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton("Cancel", self)
        cancel_btn.setFixedWidth(75)
        cancel_btn.clicked.connect(self.reject)

        apply_btn = QPushButton("Apply", self)
        apply_btn.setFixedWidth(75)
        apply_btn.setEnabled(False)

        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(apply_btn)

        layout.addLayout(btn_layout)

    def _create_general_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        # 1. Header: Icon + Name LineEdit
        header = QHBoxLayout()
        icon_label = QLabel(widget)
        icon_name = get_file_icon_name(self.path, self.is_dir)
        icon_label.setPixmap(get_icon(icon_name, size=36).pixmap(36, 36))
        header.addWidget(icon_label)

        self.name_edit = QLineEdit(os.path.basename(self.path), widget)
        self.name_edit.setFixedHeight(28)
        header.addWidget(self.name_edit)

        layout.addLayout(header)
        layout.addWidget(self._make_divider())

        # 2. File stats
        try:
            st = os.stat(self.path)
            size_bytes = st.st_size
            created = st.st_ctime
            modified = st.st_mtime
            accessed = st.st_atime
        except Exception:
            size_bytes = 0
            created = 0
            modified = 0
            accessed = 0

        type_desc = get_file_type_description(self.path, self.is_dir)

        # Grid-like rows
        layout.addLayout(self._make_row("Type of file:", type_desc))
        layout.addLayout(self._make_row("Opens with:", "System Default"))

        layout.addWidget(self._make_divider())

        layout.addLayout(self._make_row("Location:", os.path.dirname(self.path)))
        layout.addLayout(self._make_row("Size:", f"{format_size(size_bytes)} ({size_bytes:,} bytes)"))

        layout.addWidget(self._make_divider())

        layout.addLayout(self._make_row("Created:", format_datetime(created) if created else "Unknown"))
        layout.addLayout(self._make_row("Modified:", format_datetime(modified) if modified else "Unknown"))
        layout.addLayout(self._make_row("Accessed:", format_datetime(accessed) if accessed else "Unknown"))

        layout.addWidget(self._make_divider())

        # Attributes
        attr_layout = QHBoxLayout()
        attr_label = QLabel("Attributes:", widget)
        attr_label.setFixedWidth(80)
        attr_layout.addWidget(attr_label)

        chk_readonly = QCheckBox("Read-only", widget)
        chk_hidden = QCheckBox("Hidden", widget)

        if not os.access(self.path, os.W_OK):
            chk_readonly.setChecked(True)
        if os.path.basename(self.path).startswith("."):
            chk_hidden.setChecked(True)

        attr_layout.addWidget(chk_readonly)
        attr_layout.addWidget(chk_hidden)
        attr_layout.addStretch()

        layout.addLayout(attr_layout)
        layout.addStretch()

        return widget

    def _create_permissions_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title = QLabel("Permissions and Ownership (Linux)", widget)
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title)

        try:
            st = os.stat(self.path)
            mode = oct(stat.S_IMODE(st.st_mode))
            import pwd, grp
            owner = pwd.getpwuid(st.st_uid).pw_name
            group = grp.getgrgid(st.st_gid).gr_name
        except Exception:
            mode = "0755"
            owner = "user"
            group = "user"

        layout.addLayout(self._make_row("Permissions:", f"{mode} (Unix)"))
        layout.addLayout(self._make_row("Owner:", owner))
        layout.addLayout(self._make_row("Group:", group))

        layout.addStretch()
        return widget

    def _make_row(self, label_text: str, val_text: str) -> QHBoxLayout:
        row = QHBoxLayout()
        lbl = QLabel(label_text)
        lbl.setFixedWidth(90)
        lbl.setStyleSheet("color: #888888;")
        val = QLabel(val_text)
        val.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        row.addWidget(lbl)
        row.addWidget(val)
        row.addStretch()
        return row

    def _make_divider(self) -> QFrame:
        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet("background-color: rgba(255, 255, 255, 0.08);")
        return div
