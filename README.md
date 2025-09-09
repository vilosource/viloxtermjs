# Viloxtermjs

[![Tests](https://github.com/vilosource/viloxtermjs/actions/workflows/test.yml/badge.svg)](https://github.com/vilosource/viloxtermjs/actions/workflows/test.yml)
[![Python Version](https://img.shields.io/pypi/pyversions/viloxtermjs)](https://pypi.org/project/viloxtermjs/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Easy-to-use Qt/PySide6 terminal emulator widgets for Python applications**

Viloxtermjs provides production-ready terminal emulator widgets that you can easily embed in your Qt/PySide6 applications. Powered by xterm.js and a Flask backend, it offers a full-featured terminal experience with minimal setup.

## ✨ Features

- 🖥️ **Full Terminal Emulation** - Complete terminal experience powered by xterm.js
- 🎛️ **Simple Integration** - Just a few lines of code to add a terminal to your app
- 🔌 **Qt/PySide6 Native** - Seamlessly integrates with your Qt application
- 🎨 **Customizable** - Control terminal appearance and behavior
- 📋 **Copy/Paste Support** - Built-in clipboard integration
- 🚀 **WebSocket Communication** - Real-time bidirectional communication
- 🖼️ **WSL/VM Compatible** - Works in Windows Subsystem for Linux and VMs
- 📦 **Zero Configuration** - Works out of the box with sensible defaults
- ✅ **CI/CD Ready** - Automated testing with GitHub Actions

## 🚀 Quick Start

### Installation

```bash
pip install viloxtermjs
```

### Simple Example

Create a terminal window in just a few lines:

```python
from viloxtermjs import TerminalWidget
from PySide6.QtWidgets import QApplication, QMainWindow
import sys

app = QApplication(sys.argv)
window = QMainWindow()
terminal = TerminalWidget()
window.setCentralWidget(terminal)
window.show()
app.exec()
```

That's it! You now have a fully functional terminal in your Qt application.

## 📚 Examples

### Single Terminal Window

```python
from viloxtermjs import TerminalWidget
from PySide6.QtWidgets import QApplication, QMainWindow
import sys

def main():
    app = QApplication(sys.argv)
    
    window = QMainWindow()
    window.setWindowTitle("My Terminal App")
    window.setGeometry(100, 100, 800, 600)
    
    # Create terminal widget with custom command
    terminal = TerminalWidget(command='bash')
    window.setCentralWidget(terminal)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

### Multiple Terminals in Tabs

See `examples/tabbed_terminal.py` for a complete implementation of a tabbed terminal application with:
- Dynamic tab creation/deletion
- Keyboard shortcuts
- Menu bar
- Dark theme

### Custom Terminal Commands

```python
# Run Python interpreter
terminal = TerminalWidget(command='python')

# Run with arguments
terminal = TerminalWidget(command='ssh', cmd_args='user@host')

# Run custom shell
terminal = TerminalWidget(command='zsh')
```

## 🎮 Keyboard Shortcuts

The terminal supports standard keyboard shortcuts:

- **Copy**: `Ctrl+Shift+C` or `Ctrl+Shift+X`
- **Paste**: `Ctrl+Shift+V`
- **New Tab** (in tabbed example): `Ctrl+T`
- **Close Tab** (in tabbed example): `Ctrl+W`

## 🛠️ Advanced Usage

### Handling Terminal Events

```python
from viloxtermjs import TerminalWidget

terminal = TerminalWidget()

# Connect to terminal closed signal
terminal.terminal_closed.connect(lambda: print("Terminal closed"))

# Programmatically close terminal
terminal.close_terminal()
```

### Custom Styling

The widget uses QWebEngineView, so you can inject custom CSS:

```python
terminal = TerminalWidget()
# Custom styling can be applied through the Flask template
```

### Running in WSL/Virtual Machines

The package automatically detects and configures settings for WSL and VM environments. If you encounter graphics issues, the package will automatically use software rendering.

For manual control:

```python
import os
# Disable auto-configuration
os.environ['VILOTERM_NO_AUTO_SETUP'] = '1'

# Configure manually
os.environ['QT_OPENGL'] = 'software'
os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--use-angle=swiftshader'
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Your Qt Application             │
├─────────────────────────────────────────┤
│         TerminalWidget (PySide6)        │
├─────────────────────────────────────────┤
│         QWebEngineView                  │
│              ↕                          │
│     Flask Server (localhost)            │
├─────────────────────────────────────────┤
│     PTY Process ←→ WebSocket            │
│              ↕                          │
│           xterm.js                      │
└─────────────────────────────────────────┘
```

## 📋 Requirements

- Python 3.8+
- PySide6
- Flask & Flask-SocketIO
- Modern web browser engine (provided by Qt WebEngine)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/viloxtermjs.git
cd viloxtermjs

# Install Git hooks
./setup-git-hooks.sh

# Install in development mode
pip install -e ".[dev]"
```

See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for detailed development setup and guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [xterm.js](https://xtermjs.org/) - Terminal emulator for the web
- [pyxtermjs](https://github.com/cs01/pyxtermjs) - Inspiration for the Flask/xterm.js integration
- [PySide6](https://doc.qt.io/qtforpython/) - Qt for Python

## 🐛 Troubleshooting

### Graphics Issues in WSL/VM

If you encounter OpenGL errors in WSL or virtual machines, the package should automatically handle this. If issues persist:

1. Use the provided launch script:
```bash
./run_terminal.sh
```

2. Or set environment variables manually:
```bash
export QT_OPENGL=software
export QTWEBENGINE_CHROMIUM_FLAGS="--use-angle=swiftshader"
python your_app.py
```

### Terminal Not Loading

Ensure all dependencies are installed:
```bash
pip install viloxtermjs[dev]  # Includes development dependencies
```

### Copy/Paste Not Working

The terminal uses `Ctrl+Shift+C/V` for copy/paste to avoid conflicts with terminal control sequences.

## 📧 Support

For bugs and feature requests, please use the [GitHub Issues](https://github.com/yourusername/viloxtermjs/issues) page.

For questions and discussions, use [GitHub Discussions](https://github.com/yourusername/viloxtermjs/discussions).

---

Made with ❤️ for the Python community