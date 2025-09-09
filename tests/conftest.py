"""
Pytest configuration and fixtures for viloxtermjs tests
"""
import os
import sys
import pytest
from unittest.mock import Mock, patch
from PySide6.QtWidgets import QApplication

# Set environment for headless testing (GitHub Actions)
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['QT_LOGGING_RULES'] = '*.debug=false'
os.environ['QT_OPENGL'] = 'software'
os.environ['QTWEBENGINE_DISABLE_SANDBOX'] = '1'
os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--use-angle=swiftshader --disable-gpu-driver-bug-workarounds'

# Ensure the package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture(scope='session')
def qapp():
    """Create a QApplication instance for the entire test session"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    # Don't quit the app as it might be needed for other tests
    
@pytest.fixture
def mock_flask_app():
    """Mock Flask application for testing"""
    with patch('viloxtermjs.server.Flask') as mock_flask:
        app = Mock()
        mock_flask.return_value = app
        yield app
        
@pytest.fixture
def mock_socketio():
    """Mock SocketIO for testing"""
    with patch('viloxtermjs.server.SocketIO') as mock_sio:
        socketio = Mock()
        mock_sio.return_value = socketio
        yield socketio
        
@pytest.fixture
def mock_pty():
    """Mock PTY operations for testing"""
    with patch('viloxtermjs.server.pty') as mock_pty_module:
        mock_pty_module.fork.return_value = (12345, 10)  # pid, fd
        yield mock_pty_module
        
@pytest.fixture
def terminal_server_params():
    """Default parameters for TerminalServer"""
    return {
        'port': 0,
        'host': '127.0.0.1',
        'command': 'bash',
        'cmd_args': ''
    }

@pytest.fixture
def mock_webengine():
    """Mock QWebEngineView for testing widgets"""
    with patch('viloxtermjs.widget.QWebEngineView') as mock_view:
        view = Mock()
        mock_view.return_value = view
        yield view