#!/usr/bin/env python3
"""
Qt/PySide6 Terminal Widget
Encapsulates the pyxterm.js web components in QWebEngineView
"""
from PySide6.QtCore import QUrl, Signal, QThread, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from .server import TerminalServer
import time
import logging

class TerminalWidget(QWidget):
    """A Qt widget that embeds a web-based terminal using QWebEngineView"""
    
    # Signal emitted when terminal is closed
    terminal_closed = Signal()
    
    def __init__(self, command='bash', cmd_args='', parent=None):
        super().__init__(parent)
        self.command = command
        self.cmd_args = cmd_args
        self.terminal_server = None
        self.web_view = None
        self._setup_ui()
        self._start_terminal_server()
        
    def _setup_ui(self):
        """Setup the UI with QWebEngineView"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create web view for terminal
        self.web_view = QWebEngineView(self)
        layout.addWidget(self.web_view)
        
    def _start_terminal_server(self):
        """Start the terminal server and load the terminal in web view"""
        try:
            # Create and start terminal server with random port
            self.terminal_server = TerminalServer(
                port=0,  # Use random available port
                host='127.0.0.1',
                command=self.command,
                cmd_args=self.cmd_args
            )
            
            # Start server in background
            actual_port = self.terminal_server.start()
            
            # Give server a moment to fully start
            QThread.msleep(500)
            
            # Load terminal URL in web view
            terminal_url = f"http://127.0.0.1:{actual_port}"
            logging.info(f"Loading terminal from {terminal_url}")
            self.web_view.load(QUrl(terminal_url))
            
        except Exception as e:
            logging.error(f"Failed to start terminal server: {e}")
            # Show error in the widget
            self._show_error(f"Terminal server failed to start:\n{str(e)}")
    
    def _show_error(self, message):
        """Display error message in the widget"""
        from PySide6.QtWidgets import QLabel
        error_label = QLabel(message)
        error_label.setWordWrap(True)
        error_label.setStyleSheet("QLabel { color: red; padding: 10px; }")
        self.layout().addWidget(error_label)
        
    def close_terminal(self):
        """Close the terminal and cleanup"""
        if self.terminal_server:
            self.terminal_server.stop()
            self.terminal_server = None
        self.terminal_closed.emit()
        
    def closeEvent(self, event):
        """Handle widget close event"""
        self.close_terminal()
        super().closeEvent(event)
        
    def get_command(self):
        """Get the command being run in this terminal"""
        return self.command
        
    def set_focus(self):
        """Set focus to the terminal"""
        if self.web_view:
            self.web_view.setFocus()