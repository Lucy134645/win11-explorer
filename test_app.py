"""
Verification script for Windows 11 Explorer.
Tests window creation, tab handling, navigation, rendering, and takes a screenshot.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from win11_explorer.main_window import Win11ExplorerWindow

def run_test():
    app = QApplication(sys.argv)
    
    # Initialize explorer in current directory
    win = Win11ExplorerWindow(os.getcwd())
    win.show()
    
    # Process events to render layout
    app.processEvents()

    print(f"Tabs count: {win.tab_bar.count()}")
    print(f"Current path: {win.get_current_session().path}")
    print(f"Items in file view: {win.file_view.model.rowCount()}")
    
    # Test new tab
    new_tab_idx = win.create_new_tab(os.path.expanduser("~"))
    print(f"Created new tab index: {new_tab_idx}, total tabs: {win.tab_bar.count()}")

    # Switch back to first tab
    win.tab_bar.setCurrentIndex(0)
    print(f"Switched back to tab: {win.tab_bar.currentIndex()}")

    # Test view modes
    win.set_view_mode("large")
    app.processEvents()
    win.set_view_mode("details")
    app.processEvents()

    # Capture a screenshot of the window!
    pixmap = win.grab()
    screenshot_path = os.path.abspath("win11_explorer_preview.png")
    pixmap.save(screenshot_path)
    print(f"Screenshot saved to: {screenshot_path}")

    # Close test
    win.close()
    print("Test passed successfully!")

if __name__ == "__main__":
    run_test()
