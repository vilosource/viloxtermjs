"""
Viloxtermjs - Qt Terminal Emulator Widgets

A Python package providing easy-to-use Qt/PySide6 terminal emulator widgets
powered by xterm.js and Flask backend.

Basic Usage:
    from viloxtermjs import TerminalWidget
    from PySide6.QtWidgets import QApplication, QMainWindow
    
    app = QApplication([])
    window = QMainWindow()
    terminal = TerminalWidget()
    window.setCentralWidget(terminal)
    window.show()
    app.exec()
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .widget import TerminalWidget
from .server import TerminalServer

__all__ = ['TerminalWidget', 'TerminalServer']

# Environment setup for WSL/VM compatibility
import os
import sys

def setup_environment():
    """Setup environment variables for better compatibility in WSL/VM"""
    # Only set if not already set by user
    if 'QT_OPENGL' not in os.environ:
        os.environ['QT_OPENGL'] = 'software'
    if 'QT_QUICK_BACKEND' not in os.environ:
        os.environ['QT_QUICK_BACKEND'] = 'software'
    if 'QTWEBENGINE_DISABLE_SANDBOX' not in os.environ:
        os.environ['QTWEBENGINE_DISABLE_SANDBOX'] = '1'
    if 'QTWEBENGINE_CHROMIUM_FLAGS' not in os.environ:
        os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--use-angle=swiftshader --disable-gpu-driver-bug-workarounds'

# Auto-setup environment on import for better out-of-box experience
# Users can disable by setting VILOXTERMJS_NO_AUTO_SETUP=1
if os.environ.get('VILOXTERMJS_NO_AUTO_SETUP') != '1':
    setup_environment()