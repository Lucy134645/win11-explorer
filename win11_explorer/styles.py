"""
Windows 11 Fluent Design stylesheets for Win11 Explorer.
Supports Dark and Light Mica styling with Segoe UI typography and smooth borders.
"""

DARK_THEME = """
/* Base Window */
QMainWindow, QDialog, QWidget#CentralWidget {
    background-color: #202020;
    color: #FFFFFF;
    font-family: 'Segoe UI Variable Text', 'Segoe UI', 'Cantarell', 'Noto Sans', sans-serif;
    font-size: 13px;
}

/* Header & Tab Bar Area */
QWidget#HeaderContainer {
    background-color: #1a1a1a;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

/* Tab Bar */
QTabBar {
    background: transparent;
    qproperty-drawBase: 0;
    border: none;
}

QTabBar::tab {
    background-color: #232323;
    color: #CCCCCC;
    padding: 7px 16px 7px 12px;
    margin-right: 3px;
    margin-top: 6px;
    border-top-left-radius: 7px;
    border-top-right-radius: 7px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-bottom: none;
    min-width: 140px;
    max-width: 220px;
}

QTabBar::tab:hover {
    background-color: #2c2c2c;
    color: #FFFFFF;
}

QTabBar::tab:selected {
    background-color: #2c2c2c;
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-bottom: 1px solid #2c2c2c;
}

/* Navigation & Command Bars */
QWidget#NavBar, QWidget#CommandBar {
    background-color: #2c2c2c;
    border-bottom: 1px solid rgba(255, 255, 255, 0.07);
}

/* Icon Buttons (Command Bar & Nav Bar) */
QToolButton {
    background-color: transparent;
    color: #E0E0E0;
    border: 1px solid transparent;
    border-radius: 5px;
    padding: 5px 8px;
    margin: 1px 2px;
    font-size: 12px;
}

QToolButton:hover {
    background-color: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.05);
    color: #FFFFFF;
}

QToolButton:pressed {
    background-color: rgba(255, 255, 255, 0.04);
}

QToolButton:disabled {
    color: #666666;
}

QToolButton::menu-indicator {
    image: none;
    subcontrol-position: right center;
    subcontrol-origin: padding;
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
    background-color: #202020;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 6px;
    padding: 2px 6px;
}

QFrame#AddressContainer:focus-within {
    border: 1px solid #60CDFF;
}

/* Search Bar */
QLineEdit#SearchBox {
    background-color: #202020;
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 6px;
    padding: 5px 10px 5px 28px;
    font-size: 12px;
}

QLineEdit#SearchBox:focus {
    border: 1px solid #60CDFF;
    background-color: #1e1e1e;
}

QLineEdit#SearchBox::placeholder {
    color: #8A8886;
}

/* Address Editable Text Box */
QLineEdit#AddressEdit {
    background-color: #202020;
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
    border-right: 1px solid rgba(255, 255, 255, 0.07);
    color: #E0E0E0;
    padding-top: 6px;
    padding-left: 4px;
    outline: none;
}

QTreeView#SidebarTree::item {
    height: 32px;
    border-radius: 5px;
    padding-left: 6px;
    margin: 1px 6px 1px 4px;
}

QTreeView#SidebarTree::item:hover {
    background-color: rgba(255, 255, 255, 0.06);
    color: #FFFFFF;
}

QTreeView#SidebarTree::item:selected {
    background-color: rgba(255, 255, 255, 0.09);
    color: #FFFFFF;
}

QTreeView#SidebarTree::branch {
    background: transparent;
}

/* Main Content Views */
QWidget#MainContentArea {
    background-color: #191919;
}

QTableView#DetailsView, QListView#IconsView, QListView#TilesView {
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
    color: #A0A0A0;
    padding: 6px 12px;
    border: none;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    border-bottom: 1px solid rgba(255, 255, 255, 0.07);
    font-weight: 500;
    font-size: 12px;
}

QHeaderView::section:hover {
    background-color: rgba(255, 255, 255, 0.04);
    color: #FFFFFF;
}

/* Item Selection & Hover in Details/Icon Views */
QTableView#DetailsView::item {
    height: 34px;
    padding: 2px 8px;
    border-radius: 4px;
}

QTableView#DetailsView::item:hover, QListView::item:hover {
    background-color: rgba(255, 255, 255, 0.06);
}

QTableView#DetailsView::item:selected, QListView::item:selected {
    background-color: rgba(255, 255, 255, 0.1);
    color: #FFFFFF;
}

/* Status Bar */
QStatusBar {
    background-color: #202020;
    border-top: 1px solid rgba(255, 255, 255, 0.07);
    color: #9E9E9E;
    font-size: 12px;
    padding: 3px 12px;
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
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 0.2);
    min-height: 25px;
    border-radius: 4px;
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
    height: 8px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background: rgba(255, 255, 255, 0.2);
    min-width: 25px;
    border-radius: 4px;
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
QMainWindow, QDialog, QWidget#CentralWidget {
    background-color: #F3F3F3;
    color: #1B1B1B;
    font-family: 'Segoe UI Variable Text', 'Segoe UI', 'Cantarell', 'Noto Sans', sans-serif;
    font-size: 13px;
}

/* Header & Tab Bar Area */
QWidget#HeaderContainer {
    background-color: #EBEBEB;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

/* Tab Bar */
QTabBar {
    background: transparent;
    qproperty-drawBase: 0;
    border: none;
}

QTabBar::tab {
    background-color: #E5E5E5;
    color: #555555;
    padding: 7px 16px 7px 12px;
    margin-right: 3px;
    margin-top: 6px;
    border-top-left-radius: 7px;
    border-top-right-radius: 7px;
    border: 1px solid rgba(0, 0, 0, 0.05);
    border-bottom: none;
    min-width: 140px;
    max-width: 220px;
}

QTabBar::tab:hover {
    background-color: #ECECEC;
    color: #111111;
}

QTabBar::tab:selected {
    background-color: #FFFFFF;
    color: #111111;
    border: 1px solid rgba(0, 0, 0, 0.08);
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
    padding-left: 4px;
    outline: none;
}

QTreeView#SidebarTree::item {
    height: 32px;
    border-radius: 5px;
    padding-left: 6px;
    margin: 1px 6px 1px 4px;
}

QTreeView#SidebarTree::item:hover {
    background-color: rgba(0, 0, 0, 0.04);
    color: #000000;
}

QTreeView#SidebarTree::item:selected {
    background-color: rgba(0, 0, 0, 0.07);
    color: #000000;
}

/* Main Content Views */
QWidget#MainContentArea {
    background-color: #FFFFFF;
}

QTableView#DetailsView, QListView#IconsView, QListView#TilesView {
    background-color: #FFFFFF;
    border: none;
    color: #1B1B1B;
    outline: none;
}

QHeaderView::section {
    background-color: #FFFFFF;
    color: #666666;
    padding: 6px 12px;
    border: none;
    border-right: 1px solid rgba(0, 0, 0, 0.05);
    border-bottom: 1px solid rgba(0, 0, 0, 0.07);
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
QStatusBar {
    background-color: #F3F3F3;
    border-top: 1px solid rgba(0, 0, 0, 0.06);
    color: #666666;
    font-size: 12px;
    padding: 3px 12px;
}

/* Context Menu */
QMenu {
    background-color: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.12);
    border-radius: 8px;
    padding: 6px 4px;
    color: #1B1B1B;
    font-size: 13px;
}

QMenu::item {
    padding: 6px 28px 6px 28px;
    border-radius: 5px;
    margin: 1px 4px;
}

QMenu::item:selected {
    background-color: rgba(0, 0, 0, 0.06);
}

QMenu::separator {
    height: 1px;
    background: rgba(0, 0, 0, 0.08);
    margin: 4px 8px;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 8px;
}

QScrollBar::handle:vertical {
    background: rgba(0, 0, 0, 0.2);
    min-height: 25px;
    border-radius: 4px;
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
    height: 8px;
}

QScrollBar::handle:horizontal {
    background: rgba(0, 0, 0, 0.2);
    min-width: 25px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background: rgba(0, 0, 0, 0.35);
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}
"""
