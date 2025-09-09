#!/usr/bin/env python3
"""
Simple Demo - Single Terminal Window

This is the simplest possible example of using viloterm-widgets.
It creates a single terminal in a Qt window.

Usage:
    python simple_demo.py
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt

# Import the terminal widget
from viloxtermjs import TerminalWidget


def main():
    # Create the Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Simple Terminal Demo")
    
    # Create main window
    window = QMainWindow()
    window.setWindowTitle("Viloxtermjs - Simple Terminal Demo")
    window.setGeometry(100, 100, 800, 600)
    
    # Create a terminal widget
    terminal = TerminalWidget(command='bash')
    
    # Set the terminal as the central widget
    window.setCentralWidget(terminal)
    
    # Show the window
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()