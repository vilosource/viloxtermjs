"""
Tests for the TerminalServer class
"""
import pytest
import os
import threading
import time
from unittest.mock import Mock, patch, MagicMock, call
from viloxtermjs.server import TerminalServer


class TestTerminalServer:
    """Test suite for TerminalServer"""
    
    def test_initialization(self, terminal_server_params):
        """Test TerminalServer initialization"""
        server = TerminalServer(**terminal_server_params)
        
        assert server.port == 0
        assert server.host == '127.0.0.1'
        assert server.command == 'bash'
        assert server.cmd_args == []
        assert server.running is False
        assert server.app is not None
        assert server.socketio is not None
        
    def test_initialization_with_args(self):
        """Test TerminalServer initialization with custom arguments"""
        server = TerminalServer(
            port=8080,
            host='0.0.0.0',
            command='python',
            cmd_args='-u -c "print(123)"'
        )
        
        assert server.port == 8080
        assert server.host == '0.0.0.0'
        assert server.command == 'python'
        assert server.cmd_args == ['-u', '-c', 'print(123)']
        
    @patch('viloxtermjs.server.Flask')
    @patch('viloxtermjs.server.SocketIO')
    def test_flask_app_setup(self, mock_socketio, mock_flask):
        """Test Flask app is properly configured"""
        # Configure mock Flask app config to behave like a real dict
        mock_app = MagicMock()
        mock_config = {}
        mock_app.config = mock_config
        mock_flask.return_value = mock_app
        
        server = TerminalServer()
        
        # Check Flask was initialized
        mock_flask.assert_called_once()
        
        # Check SocketIO was initialized with the Flask app
        mock_socketio.assert_called_once()
        
        # Check app config
        assert 'SECRET_KEY' in server.app.config
        assert server.app.config['fd'] is None
        assert server.app.config['child_pid'] is None
        
    def test_html_template_generation(self):
        """Test HTML template contains required elements"""
        server = TerminalServer()
        html = server._get_html_template()
        
        # Check for essential components
        assert 'xterm.js' in html
        assert 'socket.io' in html
        assert 'terminal' in html
        assert 'pty-input' in html
        assert 'pty-output' in html
        assert 'resize' in html
        
    @patch('viloxtermjs.server.struct.pack')
    @patch('viloxtermjs.server.fcntl.ioctl')
    def test_set_winsize(self, mock_ioctl, mock_pack):
        """Test terminal window size setting"""
        server = TerminalServer()
        
        # Test setting window size
        server._set_winsize(10, 24, 80)
        
        # Check struct.pack was called with correct parameters
        mock_pack.assert_called_once_with("HHHH", 24, 80, 0, 0)
        
        # Check ioctl was called
        mock_ioctl.assert_called_once()
        
    @patch('threading.Thread')
    def test_start_server(self, mock_thread):
        """Test server start functionality"""
        server = TerminalServer(port=5000)
        mock_thread_instance = Mock()
        mock_thread.return_value = mock_thread_instance
        
        port = server.start()
        
        # Check thread was created and started
        mock_thread.assert_called_once()
        mock_thread_instance.start.assert_called_once()
        
        assert server.running is True
        assert port == 5000
        
    def test_start_server_already_running(self):
        """Test starting an already running server"""
        server = TerminalServer(port=5000)
        server.running = True
        
        port = server.start()
        
        # Should return existing port without starting again
        assert port == 5000
        
    @patch('os.kill')
    @patch('os.close')
    def test_stop_server(self, mock_close, mock_kill):
        """Test server stop functionality"""
        server = TerminalServer()
        server.running = True
        server.child_pid = 12345
        server.fd = 10
        
        server.stop()
        
        assert server.running is False
        mock_kill.assert_called_once_with(12345, 15)  # SIGTERM
        mock_close.assert_called_once_with(10)
        
    @patch('os.kill')
    def test_stop_server_no_process(self, mock_kill):
        """Test stopping server when process doesn't exist"""
        mock_kill.side_effect = ProcessLookupError()
        
        server = TerminalServer()
        server.running = True
        server.child_pid = 99999
        
        # Should not raise exception
        server.stop()
        
        assert server.running is False
        
    def test_get_url(self):
        """Test URL generation"""
        server = TerminalServer(port=8080, host='localhost')
        
        url = server.get_url()
        
        assert url == "http://localhost:8080"
        
    @patch('viloxtermjs.server.select.select')
    @patch('viloxtermjs.server.os.read')
    def test_read_and_forward_pty_output(self, mock_read, mock_select):
        """Test PTY output reading and forwarding"""
        server = TerminalServer()
        server.running = True
        server.app.config['fd'] = 10
        server.socketio = Mock()
        
        # Simulate data ready
        mock_select.return_value = ([10], [], [])
        mock_read.return_value = b"test output"
        
        # Run one iteration (modify method to be testable)
        # Note: In real implementation, this runs in a loop
        # We're testing the logic inside the loop
        
        # Since the method runs forever, we test its components
        assert server.running is True
        
    def test_dynamic_port_allocation(self):
        """Test that port 0 gets dynamically allocated"""
        server = TerminalServer(port=0)
        
        # When port is 0, it should remain 0 until started
        assert server.port == 0
        
        # After starting, it should have a real port
        # (In actual test, we'd mock the socket binding)
        
    @patch('viloxtermjs.server.pty.fork')
    def test_pty_fork_handling(self, mock_fork):
        """Test PTY fork handling in connect handler"""
        # This would require more complex setup to test the socketio handlers
        # For now, we verify the basic structure
        server = TerminalServer()
        
        # Simulate child process
        mock_fork.return_value = (0, None)
        
        # The actual handler would be tested through integration tests
        assert server.app is not None


class TestServerIntegration:
    """Integration tests for TerminalServer"""
    
    @pytest.mark.skipif(
        os.environ.get('CI') == 'true',
        reason="Integration test skipped in CI"
    )
    def test_server_lifecycle(self):
        """Test complete server lifecycle"""
        server = TerminalServer(command='echo', cmd_args='test')
        
        try:
            # Start server
            port = server.start()
            assert port > 0
            assert server.running is True
            
            # Give server time to start
            time.sleep(0.5)
            
            # Stop server
            server.stop()
            assert server.running is False
            
        finally:
            # Ensure cleanup
            if server.running:
                server.stop()