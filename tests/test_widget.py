"""
Tests for the TerminalWidget class that work with PySide6
"""
import pytest
from unittest.mock import Mock, patch, MagicMock, PropertyMock
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtTest import QTest
import time


class TestTerminalWidget:
    """Test suite for TerminalWidget that properly handles Qt objects"""
    
    @patch('viloxtermjs.widget.TerminalServer')
    def test_initialization(self, mock_server, qapp):
        """Test TerminalWidget initialization"""
        from viloxtermjs.widget import TerminalWidget
        
        # Mock the server
        mock_server_instance = Mock()
        mock_server_instance.start.return_value = 12345
        mock_server.return_value = mock_server_instance
        
        # Create widget (QWebEngineView will be real, not mocked)
        widget = TerminalWidget()
        
        # Check widget properties
        assert isinstance(widget, QWidget)
        assert widget.command == 'bash'
        assert widget.cmd_args == ''
        
        # Check that server was created
        mock_server.assert_called_once()
        
    @patch('viloxtermjs.widget.TerminalServer')
    def test_initialization_with_custom_command(self, mock_server, qapp):
        """Test TerminalWidget with custom command"""
        from viloxtermjs.widget import TerminalWidget
        
        # Mock the server
        mock_server_instance = Mock()
        mock_server_instance.start.return_value = 12345
        mock_server.return_value = mock_server_instance
        
        widget = TerminalWidget(command='python', cmd_args='-i')
        
        assert widget.command == 'python'
        assert widget.cmd_args == '-i'
        
        # Check server was created with correct parameters
        mock_server.assert_called_once_with(
            port=0,
            host='127.0.0.1',
            command='python',
            cmd_args='-i'
        )
        
    @patch('viloxtermjs.widget.TerminalServer')
    def test_close_terminal(self, mock_server, qapp):
        """Test closing the terminal"""
        from viloxtermjs.widget import TerminalWidget
        
        mock_server_instance = Mock()
        mock_server_instance.start.return_value = 12345
        mock_server.return_value = mock_server_instance
        
        widget = TerminalWidget()
        
        # Connect to signal to check it's emitted
        signal_emitted = []
        widget.terminal_closed.connect(lambda: signal_emitted.append(True))
        
        # Close terminal
        widget.close_terminal()
        
        # Check server was stopped
        mock_server_instance.stop.assert_called_once()
        
        # Check terminal_server is None
        assert widget.terminal_server is None
        
        # Check signal was emitted
        assert len(signal_emitted) == 1
        
    @patch('viloxtermjs.widget.TerminalServer')
    def test_get_command(self, mock_server, qapp):
        """Test getting the command"""
        from viloxtermjs.widget import TerminalWidget
        
        mock_server_instance = Mock()
        mock_server_instance.start.return_value = 12345
        mock_server.return_value = mock_server_instance
        
        widget = TerminalWidget(command='zsh')
        
        assert widget.get_command() == 'zsh'
        
    @patch('viloxtermjs.widget.TerminalServer')
    def test_server_error_handling(self, mock_server, qapp):
        """Test error handling when server fails"""
        from viloxtermjs.widget import TerminalWidget
        
        # Make server.start() raise an exception
        mock_server_instance = Mock()
        mock_server_instance.start.side_effect = Exception("Server failed")
        mock_server.return_value = mock_server_instance
        
        # Should not raise exception during initialization
        widget = TerminalWidget()
        
        # Layout should have error message
        layout = widget.layout()
        assert layout is not None
        assert layout.count() > 1  # QWebEngineView + error label