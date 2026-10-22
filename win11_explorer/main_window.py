"""
Windows 11 File Explorer Main Window for Arch Linux.
Assembles the Fluent UI tabs, navigation bar, command bar, sidebar, and content views.
"""

import os
from typing import List
from dataclasses import dataclass, field
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMessageBox, QApplication, QFrame
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut

from win11_explorer.styles import DARK_THEME, LIGHT_THEME
from win11_explorer.icons import get_icon
from win11_explorer.file_ops import (
    paste_files, create_new_folder, create_new_file, open_terminal,
    ExplorerClipboard, get_file_icon_name
)
from win11_explorer.widgets.tab_bar import Win11TabBar
from win11_explorer.widgets.nav_bar import Win11NavBar
from win11_explorer.widgets.command_bar import Win11CommandBar
from win11_explorer.widgets.sidebar import Win11Sidebar
from win11_explorer.widgets.file_view import Win11FileView
from win11_explorer.widgets.status_bar import Win11StatusBar
from win11_explorer.widgets.properties_dialog import Win11PropertiesDialog


@dataclass
class TabSession:
    path: str
    history: List[str] = field(default_factory=list)
    history_idx: int = -1
    view_mode: str = "details"
    show_hidden: bool = False
    search_query: str = ""

    def __post_init__(self):
        if not self.history:
            self.history = [self.path]
            self.history_idx = 0


class Win11ExplorerWindow(QMainWindow):
    """Main window representing the 1:1 Windows 11 File Explorer."""

    def __init__(self, initial_path: str = None):
        super().__init__()

        self.setWindowTitle("File Explorer")
        self.resize(1100, 720)
        self.setMinimumSize(800, 500)
        self.setWindowIcon(get_icon("folder", size=32))

        # Theme state
        self.is_dark_theme = True
        self.setStyleSheet(DARK_THEME)

        # Tab sessions list
        self.tabs: List[TabSession] = []

        # Central widget
        central = QWidget(self)
        central.setObjectName("CentralWidget")
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Header container (Tabs + Navigation Bar + Command Bar)
        header_widget = QWidget(central)
        header_widget.setObjectName("HeaderContainer")
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        # 1.1 Tab bar
        self.tab_bar = Win11TabBar(header_widget)
        self.tab_bar.currentChanged.connect(self._on_tab_switched)
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        self.tab_bar.newTabRequested.connect(lambda: self.create_new_tab())
        header_layout.addWidget(self.tab_bar)

        # 1.2 Navigation bar
        self.nav_bar = Win11NavBar(header_widget)
        self.nav_bar.backRequested.connect(self.go_back)
        self.nav_bar.forwardRequested.connect(self.go_forward)
        self.nav_bar.upRequested.connect(self.go_up)
        self.nav_bar.pathChanged.connect(self.navigate_to)
        self.nav_bar.searchChanged.connect(self._on_search_changed)
        header_layout.addWidget(self.nav_bar)

        # 1.3 Command bar (Ribbon)
        self.cmd_bar = Win11CommandBar(header_widget)
        self.cmd_bar.newFolderRequested.connect(self.create_folder)
        self.cmd_bar.newFileRequested.connect(self.create_file)
        self.cmd_bar.openTerminalRequested.connect(self.open_terminal_here)
        self.cmd_bar.cutRequested.connect(self._on_cut)
        self.cmd_bar.copyRequested.connect(self._on_copy)
        self.cmd_bar.pasteRequested.connect(self.paste_clipboard)
        self.cmd_bar.renameRequested.connect(self._on_rename)
        self.cmd_bar.deleteRequested.connect(self._on_delete)
        self.cmd_bar.sortRequested.connect(self._on_sort)
        self.cmd_bar.viewModeRequested.connect(self.set_view_mode)
        self.cmd_bar.toggleHiddenRequested.connect(self.toggle_hidden_files)
        self.cmd_bar.selectAllRequested.connect(self._on_select_all)
        self.cmd_bar.copyPathRequested.connect(self._on_copy_path)
        self.cmd_bar.propertiesRequested.connect(self.show_properties)
        self.cmd_bar.toggleThemeRequested.connect(self.toggle_theme)
        header_layout.addWidget(self.cmd_bar)

        main_layout.addWidget(header_widget)

        # 2. Main split view (Sidebar + File View)
        self.splitter = QSplitter(Qt.Orientation.Horizontal, central)
        self.splitter.setHandleWidth(1)
        self.splitter.setStyleSheet("QSplitter::handle { background-color: rgba(255, 255, 255, 0.06); }")

        # 2.1 Sidebar
        self.sidebar = Win11Sidebar(self.splitter)
        self.sidebar.pathSelected.connect(self.navigate_to)
        self.splitter.addWidget(self.sidebar)

        # 2.2 File View
        self.file_view = Win11FileView(self.splitter)
        self.file_view.folderOpened.connect(self.navigate_to)
        self.file_view.selectionChanged.connect(self._on_selection_changed)
        self.file_view.itemCountChanged.connect(self._on_count_changed)
        self.file_view.refreshRequested.connect(self.refresh_current_tab)
        self.splitter.addWidget(self.file_view)

        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setSizes([230, 870])

        main_layout.addWidget(self.splitter, 1)

        # 3. Status Bar
        self.status_bar = Win11StatusBar(central)
        self.status_bar.viewModeChanged.connect(self.set_view_mode)
        main_layout.addWidget(self.status_bar)

        # Register global hotkeys
        self._setup_global_shortcuts()

        # Initialize first tab
        start_dir = initial_path or os.path.expanduser("~")
        self.create_new_tab(start_dir)

    def _setup_global_shortcuts(self):
        # Ctrl+T: New tab
        QShortcut(QKeySequence("Ctrl+T"), self, activated=lambda: self.create_new_tab())
        # Ctrl+W: Close tab
        QShortcut(QKeySequence("Ctrl+W"), self, activated=self.close_current_tab)
        # Ctrl+N: New window
        QShortcut(QKeySequence("Ctrl+N"), self, activated=self.create_new_window)
        # Ctrl+H: Toggle hidden files
        QShortcut(QKeySequence("Ctrl+H"), self, activated=self._shortcut_toggle_hidden)
        # F5: Refresh
        QShortcut(QKeySequence("F5"), self, activated=self.refresh_current_tab)
        # Alt+Up: Go up
        QShortcut(QKeySequence("Alt+Up"), self, activated=self.go_up)
        # Alt+Left: Back
        QShortcut(QKeySequence("Alt+Left"), self, activated=self.go_back)
        # Alt+Right: Forward
        QShortcut(QKeySequence("Alt+Right"), self, activated=self.go_forward)
        # Ctrl+L or Alt+D: Focus address bar
        QShortcut(QKeySequence("Ctrl+L"), self, activated=self.nav_bar.address_bar.enable_edit_mode)
        QShortcut(QKeySequence("Alt+D"), self, activated=self.nav_bar.address_bar.enable_edit_mode)
        # Ctrl+F: Focus search box
        QShortcut(QKeySequence("Ctrl+F"), self, activated=self.nav_bar.search_box.setFocus)

    # ------------------ Tab Management ------------------

    def create_new_tab(self, path: str = None) -> int:
        if path is None:
            curr = self.get_current_session()
            path = curr.path if curr else os.path.expanduser("~")

        path = os.path.abspath(path)
        session = TabSession(path=path)
        self.tabs.append(session)

        # Determine icon & title
        icon_name = get_file_icon_name(path, is_dir=True)
        title = os.path.basename(path) or path
        if path == os.path.expanduser("~"):
            title = "Home"

        idx = self.tab_bar.addTab(get_icon(icon_name, size=16), title)
        self.tab_bar.setCurrentIndex(idx)
        return idx

    def close_current_tab(self):
        idx = self.tab_bar.currentIndex()
        if idx >= 0:
            self.close_tab(idx)

    def close_tab(self, index: int):
        if len(self.tabs) <= 1:
            # If only 1 tab remaining, close window
            self.close()
            return

        self.tab_bar.removeTab(index)
        self.tabs.pop(index)

    def _on_tab_switched(self, index: int):
        if 0 <= index < len(self.tabs):
            session = self.tabs[index]
            self._load_session(session)

    def get_current_session(self) -> TabSession:
        idx = self.tab_bar.currentIndex()
        if 0 <= idx < len(self.tabs):
            return self.tabs[idx]
        return None

    def _load_session(self, session: TabSession):
        # Update view
        self.file_view.set_show_hidden(session.show_hidden)
        self.file_view.set_view_mode(session.view_mode)
        self.file_view.set_directory(session.path)

        # Update controls
        self.nav_bar.set_path(session.path)
        self.sidebar.select_path(session.path)
        self.cmd_bar.act_hidden.setChecked(session.show_hidden)

        # Update nav buttons state
        can_back = session.history_idx > 0
        can_forward = session.history_idx < len(session.history) - 1
        can_up = (session.path != "/")
        self.nav_bar.update_nav_buttons(can_back, can_forward, can_up)

        # Update title
        folder_name = os.path.basename(session.path) or session.path
        if session.path == os.path.expanduser("~"):
            folder_name = "Home"
        self.setWindowTitle(f"{folder_name} - File Explorer")

    # ------------------ Navigation ------------------

    def navigate_to(self, path: str, record_history: bool = True):
        path = os.path.abspath(path)
        if not os.path.exists(path):
            QMessageBox.warning(self, "Path Not Found", f"Cannot find '{path}'. Check the path and try again.")
            return

        session = self.get_current_session()
        if not session:
            return

        if record_history and session.path != path:
            # Truncate any forward history
            session.history = session.history[:session.history_idx + 1]
            session.history.append(path)
            session.history_idx = len(session.history) - 1

        session.path = path
        session.search_query = ""
        self.nav_bar.search_box.clear()

        # Update tab title & icon
        curr_idx = self.tab_bar.currentIndex()
        folder_name = os.path.basename(path) or path
        if path == os.path.expanduser("~"):
            folder_name = "Home"
        self.tab_bar.setTabText(curr_idx, folder_name)
        icon_name = get_file_icon_name(path, is_dir=True)
        self.tab_bar.setTabIcon(curr_idx, get_icon(icon_name, size=16))

        self._load_session(session)

    def go_back(self):
        session = self.get_current_session()
        if session and session.history_idx > 0:
            session.history_idx -= 1
            prev_path = session.history[session.history_idx]
            self.navigate_to(prev_path, record_history=False)

    def go_forward(self):
        session = self.get_current_session()
        if session and session.history_idx < len(session.history) - 1:
            session.history_idx += 1
            next_path = session.history[session.history_idx]
            self.navigate_to(next_path, record_history=False)

    def go_up(self):
        session = self.get_current_session()
        if session:
            parent = os.path.dirname(session.path)
            if parent and parent != session.path:
                self.navigate_to(parent)

    def refresh_current_tab(self):
        session = self.get_current_session()
        if session:
            self.file_view.set_directory(session.path)

    # ------------------ Actions ------------------

    def _on_search_changed(self, text: str):
        session = self.get_current_session()
        if session:
            session.search_query = text
            self.file_view.set_search_filter(text)

    def toggle_hidden_files(self, show: bool):
        session = self.get_current_session()
        if session:
            session.show_hidden = show
            self.file_view.set_show_hidden(show)

    def _shortcut_toggle_hidden(self):
        session = self.get_current_session()
        if session:
            new_val = not session.show_hidden
            self.cmd_bar.act_hidden.setChecked(new_val)
            self.toggle_hidden_files(new_val)

    def set_view_mode(self, mode: str):
        session = self.get_current_session()
        if session:
            session.view_mode = mode
            self.file_view.set_view_mode(mode)

    def _on_sort(self, col: int, order: Qt.SortOrder):
        self.file_view.sort_by(col, order)

    def _on_selection_changed(self, items):
        has_sel = bool(items)
        can_paste = ExplorerClipboard.has_files()
        self.cmd_bar.update_action_states(has_sel, can_paste)

    def _on_count_changed(self, total: int, selected: int, selected_bytes: int):
        self.status_bar.update_status(total, selected, selected_bytes)

    def _on_cut(self):
        self.file_view.cut_selected()
        self.cmd_bar.update_action_states(True, ExplorerClipboard.has_files())

    def _on_copy(self):
        self.file_view.copy_selected()
        self.cmd_bar.update_action_states(True, ExplorerClipboard.has_files())

    def paste_clipboard(self):
        session = self.get_current_session()
        if session and ExplorerClipboard.has_files():
            success, errors = paste_files(session.path)
            if errors:
                QMessageBox.warning(self, "Paste Error", "\n".join(errors))
            self.refresh_current_tab()
            self.cmd_bar.update_action_states(bool(self.file_view.get_selected_items()), ExplorerClipboard.has_files())

    def _on_rename(self):
        self.file_view.rename_selected()

    def _on_delete(self):
        self.file_view.delete_selected()

    def _on_select_all(self):
        self.file_view.select_all()

    def _on_copy_path(self):
        self.file_view.copy_selected_paths()

    def create_folder(self):
        session = self.get_current_session()
        if session:
            try:
                new_path = create_new_folder(session.path)
                self.refresh_current_tab()
            except Exception as e:
                QMessageBox.critical(self, "Create Folder Error", str(e))

    def create_file(self):
        session = self.get_current_session()
        if session:
            try:
                new_path = create_new_file(session.path)
                self.refresh_current_tab()
            except Exception as e:
                QMessageBox.critical(self, "Create File Error", str(e))

    def open_terminal_here(self):
        session = self.get_current_session()
        if session:
            open_terminal(session.path)

    def show_properties(self):
        self.file_view.show_properties()

    def create_new_window(self):
        session = self.get_current_session()
        path = session.path if session else os.path.expanduser("~")
        win = Win11ExplorerWindow(path)
        win.show()
        # Keep reference so window doesn't get garbage collected
        if not hasattr(QApplication.instance(), "_windows"):
            QApplication.instance()._windows = []
        QApplication.instance()._windows.append(win)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        if self.is_dark_theme:
            self.setStyleSheet(DARK_THEME)
        else:
            self.setStyleSheet(LIGHT_THEME)
