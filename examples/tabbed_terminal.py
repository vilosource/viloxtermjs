#!/usr/bin/env python3
"""
Tabbed Terminal Demo

A more advanced example showing how to create a tabbed terminal application
with menu bar, keyboard shortcuts, and tab management.

Features:
- Multiple terminal tabs
- Add/close tabs with menu and keyboard shortcuts
- Tab close buttons
- At least one tab always remains open
- Dark theme styling

Usage:
    python tabbed_terminal.py
"""

import sys
import logging
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QTabBar,
    QMenuBar, QMenu, QPushButton, QHBoxLayout,
    QWidget, QLabel, QVBoxLayout, QMessageBox
)
from PySide6.QtGui import QAction, QKeySequence

# Import from our package
from viloxtermjs import TerminalWidget

logging.basicConfig(level=logging.INFO)


class TabWidget(QWidget):
    """Custom tab widget with close button"""
    def __init__(self, title, tab_widget, index):
        super().__init__()
        self.tab_widget = tab_widget
        self.index = index
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        
        # Tab title
        self.label = QLabel(title)
        layout.addWidget(self.label)
        
        # Close button
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(16, 16)
        self.close_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-weight: bold;
                font-size: 14px;
                color: #666;
            }
            QPushButton:hover {
                color: #ff0000;
                background: rgba(255, 0, 0, 0.1);
                border-radius: 2px;
            }
        """)
        self.close_button.clicked.connect(self.close_tab)
        layout.addWidget(self.close_button)
        
    def close_tab(self):
        """Request to close this tab"""
        self.tab_widget.request_close_tab(self.index)
        
    def update_index(self, index):
        """Update the tab index"""
        self.index = index


class TerminalTabWidget(QTabWidget):
    """Custom QTabWidget for terminal tabs"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(False)  # We'll handle close buttons ourselves
        self.setMovable(True)
        self.setDocumentMode(True)
        self.tab_counter = 0
        
    def add_terminal_tab(self, command='bash', cmd_args=''):
        """Add a new terminal tab"""
        self.tab_counter += 1
        
        try:
            terminal = TerminalWidget(command=command, cmd_args=cmd_args, parent=self)
            
            # Add tab
            index = self.addTab(terminal, f"Terminal {self.tab_counter}")
            
            # Create custom tab widget with close button
            tab_widget = TabWidget(f"Terminal {self.tab_counter}", self, index)
            self.tabBar().setTabButton(index, QTabBar.ButtonPosition.RightSide, tab_widget)
            
            # Switch to new tab
            self.setCurrentIndex(index)
            terminal.set_focus()
            
            return terminal
        except Exception as e:
            logging.error(f"Failed to create terminal tab: {e}")
            QMessageBox.warning(self, "Error", f"Failed to create terminal: {str(e)}")
            return None
        
    def request_close_tab(self, index):
        """Handle close tab request"""
        # Always keep at least one tab open
        if self.count() > 1:
            self.close_tab(index)
            
    def close_tab(self, index):
        """Close a specific tab"""
        if self.count() <= 1:
            return  # Keep at least one tab
            
        # Get the terminal widget and close it
        terminal = self.widget(index)
        if terminal and hasattr(terminal, 'close_terminal'):
            terminal.close_terminal()
            
        # Remove the tab
        self.removeTab(index)
        
        # Update indices for remaining tabs
        for i in range(self.count()):
            tab_button = self.tabBar().tabButton(i, QTabBar.ButtonPosition.RightSide)
            if isinstance(tab_button, TabWidget):
                tab_button.update_index(i)


class TerminalMainWindow(QMainWindow):
    """Main application window with menu and tabbed terminals"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Viloxtermjs - Tabbed Terminal Demo")
        self.setGeometry(100, 100, 1024, 768)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QMenuBar {
                background-color: #3c3c3c;
                color: white;
            }
            QMenuBar::item:selected {
                background-color: #505050;
            }
            QMenu {
                background-color: #3c3c3c;
                color: white;
            }
            QMenu::item:selected {
                background-color: #505050;
            }
            QTabWidget::pane {
                border: 1px solid #3c3c3c;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background-color: #3c3c3c;
                color: white;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #505050;
            }
            QTabBar::tab:hover {
                background-color: #454545;
            }
        """)
        
        self._setup_ui()
        self._setup_menu()
        
        # Add initial terminal tab
        self.add_new_tab()
        
    def _setup_ui(self):
        """Setup the main UI"""
        # Create central widget with tab widget
        self.tab_widget = TerminalTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        
    def _setup_menu(self):
        """Setup the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        # Add new tab action
        new_tab_action = QAction("Add New Tab", self)
        new_tab_action.setShortcut(QKeySequence("Ctrl+T"))
        new_tab_action.triggered.connect(self.add_new_tab)
        file_menu.addAction(new_tab_action)
        
        # Close tab action
        close_tab_action = QAction("Close Tab", self)
        close_tab_action.setShortcut(QKeySequence("Ctrl+W"))
        close_tab_action.triggered.connect(self.close_current_tab)
        file_menu.addAction(close_tab_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        # Copy action (informational)
        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence("Ctrl+Shift+C"))
        copy_action.setToolTip("Copy selected text (Ctrl+Shift+C or Ctrl+Shift+X in terminal)")
        edit_menu.addAction(copy_action)
        
        # Paste action (informational)
        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence("Ctrl+Shift+V"))
        paste_action.setToolTip("Paste from clipboard (Ctrl+Shift+V in terminal)")
        edit_menu.addAction(paste_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        # Next tab
        next_tab_action = QAction("Next Tab", self)
        next_tab_action.setShortcut(QKeySequence("Ctrl+Tab"))
        next_tab_action.triggered.connect(self.next_tab)
        view_menu.addAction(next_tab_action)
        
        # Previous tab
        prev_tab_action = QAction("Previous Tab", self)
        prev_tab_action.setShortcut(QKeySequence("Ctrl+Shift+Tab"))
        prev_tab_action.triggered.connect(self.previous_tab)
        view_menu.addAction(prev_tab_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        # About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About Tabbed Terminal",
            "Viloxtermjs Tabbed Terminal Demo\n\n"
            "A demonstration of the viloxtermjs package\n"
            "showing multiple terminal tabs with full management.\n\n"
            "Features:\n"
            "• Multiple terminal tabs\n"
            "• Keyboard shortcuts\n"
            "• Tab management\n"
            "• Dark theme\n\n"
            "Powered by xterm.js and PySide6")
        
    def add_new_tab(self):
        """Add a new terminal tab"""
        self.tab_widget.add_terminal_tab()
        
    def close_current_tab(self):
        """Close the current tab"""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            self.tab_widget.request_close_tab(current_index)
            
    def next_tab(self):
        """Switch to next tab"""
        current = self.tab_widget.currentIndex()
        count = self.tab_widget.count()
        if count > 0:
            self.tab_widget.setCurrentIndex((current + 1) % count)
            
    def previous_tab(self):
        """Switch to previous tab"""
        current = self.tab_widget.currentIndex()
        count = self.tab_widget.count()
        if count > 0:
            self.tab_widget.setCurrentIndex((current - 1) % count)
            
    def closeEvent(self, event):
        """Handle application close event"""
        # Close all terminals properly
        for i in range(self.tab_widget.count()):
            terminal = self.tab_widget.widget(i)
            if terminal and hasattr(terminal, 'close_terminal'):
                terminal.close_terminal()
        event.accept()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Viloxtermjs Tabbed Terminal")
    
    # Create and show main window
    window = TerminalMainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()