#!/usr/bin/env python3
"""
Terminal Server Library
Extracted from pyxtermjs to provide terminal functionality for Qt GUI
"""
import os
import pty
import select
import struct
import fcntl
import termios
import shlex
import logging
import threading
import time
from flask import Flask, render_template_string
from flask_socketio import SocketIO
import sys

logging.getLogger("werkzeug").setLevel(logging.ERROR)

class TerminalServer:
    def __init__(self, port=0, host='127.0.0.1', command='bash', cmd_args=''):
        self.port = port
        self.host = host
        self.command = command
        self.cmd_args = shlex.split(cmd_args) if cmd_args else []
        self.app = None
        self.socketio = None
        self.server_thread = None
        self.fd = None
        self.child_pid = None
        self.running = False
        self._setup_flask_app()
        
    def _setup_flask_app(self):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "terminal_secret!"
        self.app.config["fd"] = None
        self.app.config["child_pid"] = None
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        @self.app.route("/")
        def index():
            return self._get_html_template()
            
        @self.socketio.on("pty-input", namespace="/pty")
        def pty_input(data):
            if self.app.config["fd"]:
                logging.debug("received input from browser: %s" % data["input"])
                os.write(self.app.config["fd"], data["input"].encode())
                
        @self.socketio.on("resize", namespace="/pty")
        def resize(data):
            if self.app.config["fd"]:
                logging.debug(f"Resizing window to {data['rows']}x{data['cols']}")
                self._set_winsize(self.app.config["fd"], data["rows"], data["cols"])
                
        @self.socketio.on("connect", namespace="/pty")
        def connect():
            logging.info("new client connected")
            if self.app.config["child_pid"]:
                return
                
            (child_pid, fd) = pty.fork()
            if child_pid == 0:
                subprocess_cmd = [self.command] + self.cmd_args
                os.execvp(subprocess_cmd[0], subprocess_cmd)
            else:
                self.app.config["fd"] = fd
                self.app.config["child_pid"] = child_pid
                self.fd = fd
                self.child_pid = child_pid
                self._set_winsize(fd, 24, 80)
                self.socketio.start_background_task(target=self._read_and_forward_pty_output)
                logging.info(f"child pid is {child_pid}")
                
    def _set_winsize(self, fd, row, col, xpix=0, ypix=0):
        winsize = struct.pack("HHHH", row, col, xpix, ypix)
        fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)
        
    def _read_and_forward_pty_output(self):
        max_read_bytes = 1024 * 20
        while self.running:
            self.socketio.sleep(0.01)
            if self.app.config["fd"]:
                timeout_sec = 0
                (data_ready, _, _) = select.select([self.app.config["fd"]], [], [], timeout_sec)
                if data_ready:
                    try:
                        output = os.read(self.app.config["fd"], max_read_bytes).decode(errors="ignore")
                        self.socketio.emit("pty-output", {"output": output}, namespace="/pty")
                    except OSError:
                        break
                        
    def _get_html_template(self):
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>Terminal</title>
    <style>
        body { margin: 0; padding: 0; overflow: hidden; background: #1e1e1e; }
        #terminal { width: 100%; height: 100vh; }
        
        /* Custom thin scrollbars for xterm.js */
        .xterm-viewport::-webkit-scrollbar {
            width: 8px !important;
            height: 8px !important;
        }
        
        .xterm-viewport::-webkit-scrollbar-track {
            background: #1e1e1e !important;
        }
        
        .xterm-viewport::-webkit-scrollbar-thumb {
            background: #464647 !important;
            border-radius: 4px !important;
        }
        
        .xterm-viewport::-webkit-scrollbar-thumb:hover {
            background: #5a5a5c !important;
        }
        
        .xterm-viewport::-webkit-scrollbar-corner {
            background: #1e1e1e !important;
        }
        
        /* Firefox scrollbar styling */
        .xterm-viewport {
            scrollbar-width: thin !important;
            scrollbar-color: #464647 #1e1e1e !important;
        }
    </style>
    <link rel="stylesheet" href="https://unpkg.com/xterm@4.11.0/css/xterm.css" />
</head>
<body>
    <div id="terminal"></div>
    <script src="https://unpkg.com/xterm@4.11.0/lib/xterm.js"></script>
    <script src="https://unpkg.com/xterm-addon-fit@0.5.0/lib/xterm-addon-fit.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.min.js"></script>
    <script>
        // Patch canvas getContext to always use willReadFrequently for 2D contexts
        // This fixes the Chrome warning about getImageData performance
        (function() {
            const originalGetContext = HTMLCanvasElement.prototype.getContext;
            HTMLCanvasElement.prototype.getContext = function(contextType, ...args) {
                if (contextType === '2d') {
                    // Ensure willReadFrequently is set for 2D contexts
                    let contextAttributes = args[0] || {};
                    contextAttributes.willReadFrequently = true;
                    return originalGetContext.call(this, contextType, contextAttributes);
                }
                return originalGetContext.apply(this, arguments);
            };
        })();
        
        const term = new Terminal({
            cursorBlink: true,
            macOptionIsMeta: true,
            scrollback: 1000,
            theme: {
                background: '#1e1e1e',
                foreground: '#d4d4d4'
            }
        });
        
        const fit = new FitAddon.FitAddon();
        term.loadAddon(fit);
        term.open(document.getElementById("terminal"));
        
        // Custom fit function that calculates exact dimensions
        function customFit() {
            const terminalElement = document.getElementById("terminal");
            const core = term._core;
            
            if (!core || !core._renderService || !core._renderService.dimensions) {
                // Fallback to standard fit if core not available
                fit.fit();
                return;
            }
            
            const dims = core._renderService.dimensions;
            const cellHeight = dims.actualCellHeight || 17;
            const cellWidth = dims.actualCellWidth || 9;
            
            // Get container dimensions
            const containerHeight = terminalElement.offsetHeight;
            const containerWidth = terminalElement.offsetWidth;
            
            // Calculate how many complete cells fit
            const rows = Math.floor(containerHeight / cellHeight);
            const cols = Math.floor(containerWidth / cellWidth);
            
            // Resize terminal to exact cell dimensions
            if (rows > 0 && cols > 0) {
                term.resize(cols, rows);
                
                // Calculate and set exact pixel dimensions to avoid white space
                const exactHeight = rows * cellHeight;
                const exactWidth = cols * cellWidth;
                
                // Apply exact dimensions to terminal element
                const xtermScreen = terminalElement.querySelector('.xterm-screen');
                if (xtermScreen) {
                    xtermScreen.style.height = exactHeight + 'px';
                }
                
                // Emit resize with cell dimensions for Qt side
                const dims = { 
                    cols: cols, 
                    rows: rows,
                    cellHeight: cellHeight,
                    cellWidth: cellWidth,
                    preferredHeight: exactHeight
                };
                socket.emit("resize", dims);
                
                // Store dimensions for external access
                window.terminalDimensions = dims;
            }
        }
        
        term.onData((data) => {
            socket.emit("pty-input", { input: data });
        });
        
        const socket = io.connect("/pty");
        
        socket.on("pty-output", function (data) {
            term.write(data.output);
        });
        
        socket.on("connect", () => {
            setTimeout(() => {
                customFit();
            }, 100);
        });
        
        function fitToscreen() {
            customFit();
        }
        
        function debounce(func, wait_ms) {
            let timeout;
            return function (...args) {
                const context = this;
                clearTimeout(timeout);
                timeout = setTimeout(() => func.apply(context, args), wait_ms);
            };
        }
        
        window.onresize = debounce(fitToscreen, 50);
        
        // Initial fit after terminal is fully loaded
        setTimeout(() => {
            customFit();
        }, 200);
        
        term.attachCustomKeyEventHandler((e) => {
            if (e.type !== "keydown") return true;
            if (e.ctrlKey && e.shiftKey) {
                const key = e.key.toLowerCase();
                if (key === "v") {
                    navigator.clipboard.readText().then((toPaste) => {
                        term.writeText(toPaste);
                    });
                    return false;
                } else if (key === "c" || key === "x") {
                    const toCopy = term.getSelection();
                    navigator.clipboard.writeText(toCopy);
                    term.focus();
                    return false;
                }
            }
            return true;
        });
    </script>
</body>
</html>
'''
    
    def start(self):
        """Start the terminal server in a background thread"""
        if self.running:
            return self.port
            
        self.running = True
        
        # If port is 0, find an available port
        if self.port == 0:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', 0))
                self.port = s.getsockname()[1]
        
        def run_server():
            self.socketio.run(self.app, debug=False, port=self.port, host=self.host, allow_unsafe_werkzeug=True)
            
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        
        # Wait a moment for server to start
        time.sleep(0.5)
                
        return self.port
        
    def stop(self):
        """Stop the terminal server"""
        self.running = False
        if self.child_pid:
            try:
                os.kill(self.child_pid, 15)  # SIGTERM
            except ProcessLookupError:
                pass
        if self.fd:
            try:
                os.close(self.fd)
            except OSError:
                pass
                
    def get_url(self):
        """Get the URL for the terminal server"""
        return f"http://{self.host}:{self.port}"