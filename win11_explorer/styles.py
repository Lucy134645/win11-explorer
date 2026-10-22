"""
Windows 11 Fluent Design stylesheets for Win11 Explorer.
Supports Dark Mica styling with Segoe UI typography and smooth borders.
"""

DARK_THEME = """
/* Base Window & Frameless Border */
QMainWindow {
    background-color: #1f1f1f;
}

QWidget#CentralWidget {
    background-color: #1f1f1f;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px;
    color: #FFFFFF;
    font-family: 'Segoe UI Variable Text', 'Segoe UI', 'Cantarell', 'Noto Sans', sans-serif;
    font-size: 13px;
}

/* Titlebar & Tabs Header */
QWidget#TitleBarContainer {
    background-color: #1f1f1f;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    border-bottom: 1px solid #2c2c2c;
}

/* Tab Bar */
QTabBar {
    background: transparent;
    qproperty-drawBase: 0;
    border: none;
}

QTabBar::tab {
    background-color: transparent;
    color: #9D9D9D;
    padding: 8px 14px 8px 12px;
    margin-right: 2px;
    margin-top: 6px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    border: 1px solid transparent;
    min-width: 140px;
    max-width: 230px;
    font-size: 12px;
    font-weight: 500;
}

QTabBar::tab:hover:!selected {
    background-color: rgba(255, 255, 255, 0.05);
    color: #FFFFFF;
}

QTabBar::tab:selected {
    background-color: #2c2c2c;
    color: #FFFFFF;
    border-top: 1px solid rgba(255, 255, 255, 0.09);
    border-left: 1px solid rgba(255, 255, 255, 0.07);
    border-right: 1px solid rgba(255, 255, 255, 0.07);
    border-bottom: 1px solid #2c2c2c;
}

/* Close Tab Button */
QTabBar::close-button {
    image: none;
    subcontrol-position: right center;
    padding: 2px;
    border-radius: 4px;
}

QTabBar::close-button:hover {
    background-color: rgba(255, 255, 255, 0.12);
}

/* Navigation & Command Bars */
QWidget#NavBar, QWidget#CommandBar {
    background-color: #2c2c2c;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

/* Icon Buttons (Command Bar & Nav Bar) */
QToolButton {
    background-color: transparent;
    color: #E2E2E2;
    border: 1px solid transparent;
    border-radius: 5px;
    padding: 5px 8px;
    margin: 1px 2px;
    font-size: 12px;
}

QToolButton:hover {
    background-color: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.04);
    color: #FFFFFF;
}

QToolButton:pressed {
    background-color: rgba(255, 255, 255, 0.03);
}

QToolButton:disabled {
    color: #606060;
}

QToolButton::menu-indicator {
    image: none;
    width: 0px;
}

/* Special "New" button */
QToolButton#NewButton {
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 6px 12px;
    font-weight: 500;
}

QToolButton#NewButton:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

/* Breadcrumb & Address Bar Container */
QFrame#AddressContainer {
    background-color: #1f1f1f;
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 6px;
    padding: 2px 6px;
}

QFrame#AddressContainer:focus-within {
    border: 1px solid #60CDFF;
}

/* Search Bar */
QLineEdit#SearchBox {
    background-color: #1f1f1f;
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 6px;
    padding: 5px 10px 5px 28px;
    font-size: 12px;
}

QLineEdit#SearchBox:focus {
    border: 1px solid #60CDFF;
    background-color: #1c1c1c;
}

QLineEdit#SearchBox::placeholder {
    color: #8E8E8E;
}

/* Address Editable Text Box */
QLineEdit#AddressEdit {
    background-color: #1f1f1f;
    color: #FFFFFF;
    border: none;
    padding: 4px 6px;
    font-size: 13px;
    selection-background-color: #0078D4;
}

/* Sidebar Navigation Pane */
QTreeView#SidebarTree {
    background-color: #202020;
    border: none;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
    color: #E2E2E2;
    padding-top: 6px;
    padding-left: 2px;
    outline: none;
}

QTreeView#SidebarTree::branch {
    background: transparent;
}

/* Main Content Views */
QWidget#MainContentArea {
    background-color: #191919;
}

QTableView#DetailsView, QListView#IconsView {
    background-color: #191919;
    border: none;
    color: #FFFFFF;
    outline: none;
    gridline-color: transparent;
    selection-background-color: transparent;
}

/* Details Table Header */
QHeaderView::section {
    background-color: #191919;
    color: #9D9D9D;
    padding: 7px 12px;
    border: none;
    border-right: 1px solid rgba(255, 255, 255, 0.04);
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    font-weight: 500;
    font-size: 12px;
}

QHeaderView::section:hover {
    background-color: rgba(255, 255, 255, 0.04);
    color: #FFFFFF;
}

/* Item Selection & Hover in Details/Icon Views */
QTableView#DetailsView::item {
    height: 36px;
    padding: 2px 8px;
    border-radius: 4px;
}

QTableView#DetailsView::item:hover, QListView::item:hover {
    background-color: rgba(255, 255, 255, 0.04);
}

QTableView#DetailsView::item:selected, QListView::item:selected {
    background-color: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #FFFFFF;
}

/* Status Bar */
QStatusBar, QWidget#StatusBarContainer {
    background-color: #202020;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
    color: #8E8E8E;
    font-size: 12px;
}

/* Modern Win11 Context Menu */
QMenu {
    background-color: #2c2c2c;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px;
    padding: 6px 4px;
    color: #FFFFFF;
    font-size: 13px;
}

QMenu::item {
    padding: 6px 28px 6px 28px;
    border-radius: 5px;
    margin: 1px 4px;
}

QMenu::item:selected {
    background-color: rgba(255, 255, 255, 0.09);
}

QMenu::separator {
    height: 1px;
    background: rgba(255, 255, 255, 0.08);
    margin: 4px 8px;
}

/* Modern Thin Windows 11 Scrollbars */
QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 6px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 0.2);
    min-height: 25px;
    border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(255, 255, 255, 0.35);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: transparent;
    height: 6px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background: rgba(255, 255, 255, 0.2);
    min-width: 25px;
    border-radius: 3px;
}

QScrollBar::handle:horizontal:hover {
    background: rgba(255, 255, 255, 0.35);
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Splitter */
QSplitter::handle {
    background-color: transparent;
}
"""

LIGHT_THEME = """
/* Base Window */
QMainWindow {
    background-color: #F3F3F3;
}

QWidget#CentralWidget {
    background-color: #F3F3F3;
    border: 1px solid rgba(0, 0, 0, 0.12);
    border-radius: 8px;
    color: #1B1B1B;
    font-family: 'Segoe UI Variable Text', 'Segoe UI', 'Cantarell', 'Noto Sans', sans-serif;
    font-size: 13px;
}

/* Titlebar & Tabs Header */
QWidget#TitleBarContainer {
    background-color: #F3F3F3;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    border-bottom: 1px solid #FFFFFF;
}

/* Tab Bar */
QTabBar {
    background: transparent;
    qproperty-drawBase: 0;
    border: none;
}

QTabBar::tab {
    background-color: transparent;
    color: #666666;
    padding: 8px 14px 8px 12px;
    margin-right: 2px;
    margin-top: 6px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    border: 1px solid transparent;
    min-width: 140px;
    max-width: 230px;
    font-size: 12px;
    font-weight: 500;
}

QTabBar::tab:hover:!selected {
    background-color: rgba(0, 0, 0, 0.04);
    color: #111111;
}

QTabBar::tab:selected {
    background-color: #FFFFFF;
    color: #111111;
    border-top: 1px solid rgba(0, 0, 0, 0.08);
    border-left: 1px solid rgba(0, 0, 0, 0.06);
    border-right: 1px solid rgba(0, 0, 0, 0.06);
    border-bottom: 1px solid #FFFFFF;
}

/* Navigation & Command Bars */
QWidget#NavBar, QWidget#CommandBar {
    background-color: #FFFFFF;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

/* Icon Buttons */
QToolButton {
    background-color: transparent;
    color: #333333;
    border: 1px solid transparent;
    border-radius: 5px;
    padding: 5px 8px;
    margin: 1px 2px;
    font-size: 12px;
}

QToolButton:hover {
    background-color: rgba(0, 0, 0, 0.05);
    border: 1px solid rgba(0, 0, 0, 0.04);
    color: #000000;
}

QToolButton:pressed {
    background-color: rgba(0, 0, 0, 0.08);
}

QToolButton:disabled {
    color: #AAAAAA;
}

/* Breadcrumb & Address Bar Container */
QFrame#AddressContainer {
    background-color: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.15);
    border-radius: 6px;
    padding: 2px 6px;
}

QFrame#AddressContainer:focus-within {
    border: 1px solid #0078D4;
}

/* Search Bar */
QLineEdit#SearchBox {
    background-color: #FFFFFF;
    color: #1B1B1B;
    border: 1px solid rgba(0, 0, 0, 0.15);
    border-radius: 6px;
    padding: 5px 10px 5px 28px;
    font-size: 12px;
}

QLineEdit#SearchBox:focus {
    border: 1px solid #0078D4;
}

/* Sidebar Navigation Pane */
QTreeView#SidebarTree {
    background-color: #F9F9F9;
    border: none;
    border-right: 1px solid rgba(0, 0, 0, 0.06);
    color: #222222;
    padding-top: 6px;
    padding-left: 2px;
    outline: none;
}

/* Main Content Views */
QWidget#MainContentArea {
    background-color: #FFFFFF;
}

QTableView#DetailsView, QListView#IconsView {
    background-color: #FFFFFF;
    border: none;
    color: #1B1B1B;
    outline: none;
}

QHeaderView::section {
    background-color: #FFFFFF;
    color: #666666;
    padding: 7px 12px;
    border: none;
    border-right: 1px solid rgba(0, 0, 0, 0.04);
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    font-weight: 500;
    font-size: 12px;
}

QHeaderView::section:hover {
    background-color: rgba(0, 0, 0, 0.03);
    color: #000000;
}

QTableView#DetailsView::item:hover, QListView::item:hover {
    background-color: rgba(0, 0, 0, 0.04);
}

QTableView#DetailsView::item:selected, QListView::item:selected {
    background-color: rgba(0, 0, 0, 0.08);
    color: #000000;
}

/* Status Bar */
QStatusBar, QWidget#StatusBarContainer {
    background-color: #F3F3F3;
    border-top: 1px solid rgba(0, 0, 0, 0.06);
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
    color: #666666;
    font-size: 12px;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 6px;
}

QScrollBar::handle:vertical {
    background: rgba(0, 0, 0, 0.2);
    min-height: 25px;
    border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(0, 0, 0, 0.35);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: transparent;
    height: 6px;
}

QScrollBar::handle:horizontal {
    background: rgba(0, 0, 0, 0.2);
    min-width: 25px;
    border-radius: 3px;
}

QScrollBar::handle:horizontal:hover {
    background: rgba(0, 0, 0, 0.35);
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}
"""
