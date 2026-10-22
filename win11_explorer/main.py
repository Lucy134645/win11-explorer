"""
Entry point for Windows 11 File Explorer on Arch Linux.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt

from win11_explorer.main_window import Win11ExplorerWindow
from win11_explorer.icons import get_icon


def main():
    # Set high DPI awareness
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)
    app.setApplicationName("File Explorer")
    app.setApplicationDisplayName("File Explorer")
    app.setOrganizationName("Windows")

    # Set Windows 11 modern font
    font = QFont()
    font.setFamilies(["Segoe UI Variable Text", "Segoe UI", "Cantarell", "Noto Sans", "Sans Serif"])
    font.setPixelSize(13)
    app.setFont(font)

    # Set Default App Icon
    app.setWindowIcon(get_icon("folder", size=48))

    # Determine initial directory from arguments
    initial_path = None
    if len(sys.argv) > 1:
        arg_path = sys.argv[1]
        if os.path.exists(arg_path):
            initial_path = os.path.abspath(arg_path)

    window = Win11ExplorerWindow(initial_path)
    window.show()

    # Track windows
    app._windows = [window]

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
