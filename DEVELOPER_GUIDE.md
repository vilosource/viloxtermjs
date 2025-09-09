# Developer Guide

This guide provides detailed information for developers who want to contribute to viloxtermjs or extend its functionality.

## 📦 Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, or virtualenv)
- Qt development libraries (for PySide6)

### Setting Up the Development Environment

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/viloxtermjs.git
cd viloxtermjs
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install in development mode**
```bash
pip install -e ".[dev]"
```

This installs the package in editable mode with all development dependencies.

## 🏗️ Project Structure

```
viloxtermjs/
├── viloxtermjs/          # Main package directory
│   ├── __init__.py           # Package initialization and exports
│   ├── server.py             # Flask terminal server implementation
│   └── widget.py             # Qt/PySide6 widget implementation
├── examples/                  # Example applications
│   ├── simple_demo.py        # Basic single terminal example
│   └── tabbed_terminal.py    # Advanced tabbed terminal example
├── tests/                     # Test suite
│   ├── test_server.py        # Server tests
│   └── test_widget.py        # Widget tests
├── docs/                      # Documentation
├── setup.py                   # Legacy setup configuration
├── pyproject.toml            # Modern Python packaging configuration
├── README.md                  # User-facing documentation
├── DEVELOPER_GUIDE.md        # This file
└── LICENSE                    # MIT License
```

## 🔧 Core Components

### TerminalServer (`server.py`)

The Flask-based backend that manages PTY sessions:

```python
class TerminalServer:
    def __init__(self, port=0, host='127.0.0.1', command='bash', cmd_args=''):
        # Initializes Flask app with SocketIO
        # Sets up WebSocket handlers for terminal I/O
    
    def start(self):
        # Starts the Flask server in a background thread
        # Returns the port number
    
    def stop(self):
        # Cleanly shuts down the server and PTY process
```

**Key responsibilities:**
- PTY (pseudo-terminal) process management
- WebSocket communication handling
- Terminal resize operations
- HTML template serving with xterm.js

### TerminalWidget (`widget.py`)

The Qt/PySide6 widget that embeds the terminal:

```python
class TerminalWidget(QWidget):
    terminal_closed = Signal()  # Emitted when terminal closes
    
    def __init__(self, command='bash', cmd_args='', parent=None):
        # Creates QWebEngineView
        # Starts terminal server
        # Loads terminal URL
```

**Key responsibilities:**
- QWebEngineView management
- Terminal server lifecycle
- Error handling and display
- Signal emission for Qt integration

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=viloxtermjs

# Run specific test file
pytest tests/test_widget.py
```

### Writing Tests

Create test files in the `tests/` directory:

```python
# tests/test_new_feature.py
import pytest
from viloxtermjs import TerminalWidget

def test_terminal_creation():
    widget = TerminalWidget()
    assert widget is not None
    # Add assertions
```

## 🎨 Code Style

We use standard Python code formatting tools:

```bash
# Format code with black
black viloxtermjs/

# Check code style
flake8 viloxtermjs/

# Type checking
mypy viloxtermjs/
```

### Style Guidelines

- Follow PEP 8
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use descriptive variable names
- Add docstrings to all public functions/classes

## 🔄 Development Workflow

### 1. Making Changes

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes
edit viloxtermjs/widget.py

# Test your changes
python examples/simple_demo.py
```

### 2. Testing in Different Environments

**WSL/VM Testing:**
```bash
# Set environment variables for WSL
export QT_OPENGL=software
export QTWEBENGINE_CHROMIUM_FLAGS="--use-angle=swiftshader"
python examples/simple_demo.py
```

**Native Linux/Windows:**
```bash
python examples/simple_demo.py
```

### 3. Committing Changes

```bash
# Add files
git add .

# Commit with descriptive message
git commit -m "feat: add support for custom terminal colors"

# Push to your fork
git push origin feature/your-feature-name
```

## 🔌 Extending the Package

### Adding New Terminal Features

To add new terminal features, modify the server's HTML template:

```python
# In server.py, _get_html_template() method
def _get_html_template(self):
    return '''
    <script>
        // Add new xterm.js addons or configurations
        term.loadAddon(new SearchAddon.SearchAddon());
    </script>
    '''
```

### Custom Widget Signals

Add new Qt signals for events:

```python
class TerminalWidget(QWidget):
    # Add new signal
    terminal_ready = Signal()
    
    def _on_load_finished(self):
        self.terminal_ready.emit()
```

### Supporting New Shell Commands

```python
# Allow custom environment variables
class TerminalServer:
    def __init__(self, ..., env=None):
        self.env = env or os.environ.copy()
```

## 🐛 Debugging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now run your application
```

### Common Issues and Solutions

**Issue: Terminal not connecting**
- Check if Flask server is running: Look for "Loading terminal from http://..." in logs
- Verify port is not blocked by firewall
- Check WebSocket connection in browser developer tools

**Issue: Graphics errors in WSL**
- Ensure environment variables are set correctly
- Try software rendering mode
- Check Qt and PySide6 versions

**Issue: PTY process not starting**
- Verify the command exists (e.g., 'bash', 'zsh')
- Check permissions
- Look for PTY-related errors in logs

## 📝 Documentation

### Updating Documentation

- **README.md**: User-facing documentation, installation, basic usage
- **DEVELOPER_GUIDE.md**: This file, for contributors
- **Docstrings**: In-code documentation for API reference

### Building API Documentation

```bash
# Generate API docs with Sphinx (if configured)
cd docs/
make html
```

## 🚀 Release Process

### 1. Update Version

Update version in:
- `viloxtermjs/__init__.py`
- `setup.py`
- `pyproject.toml`

### 2. Build Distribution

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build source and wheel distributions
python -m build
```

### 3. Test Installation

```bash
# Create a test environment
python -m venv test_env
source test_env/bin/activate

# Install from built package
pip install dist/viloxtermjs-*.whl

# Test it works
python -c "from viloxtermjs import TerminalWidget; print('Success!')"
```

### 4. Upload to PyPI

```bash
# Test PyPI first
twine upload --repository testpypi dist/*

# Production PyPI
twine upload dist/*
```

## 💡 Tips and Tricks

### Performance Optimization

- Reuse terminal servers when possible
- Implement connection pooling for multiple terminals
- Use lazy loading for terminal initialization

### Memory Management

- Properly close terminal servers when widgets are destroyed
- Clean up PTY processes on application exit
- Monitor Flask thread lifecycle

### Cross-Platform Compatibility

- Test on Windows, Linux, and macOS
- Handle platform-specific PTY behavior
- Account for different shell availability

## 🤝 Contributing Guidelines

1. **Fork the repository**
2. **Create a feature branch**
3. **Write tests for new features**
4. **Ensure all tests pass**
5. **Update documentation**
6. **Submit a pull request**

### Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Changelog updated (if applicable)
- [ ] No breaking changes (or documented if necessary)

## 📞 Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/viloxtermjs/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/viloxtermjs/discussions)
- **Email**: your.email@example.com

## 📚 Resources

- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [xterm.js Documentation](https://xtermjs.org/docs/)
- [PTY Python Documentation](https://docs.python.org/3/library/pty.html)

---

Happy coding! 🚀