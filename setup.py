"""
Setup configuration for viloxtermjs package
"""
from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="viloxtermjs",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Qt/PySide6 terminal emulator widgets with xterm.js backend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vilosource/viloxtermjs",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Widget Sets",
        "Topic :: Terminals :: Terminal Emulators/X Terminals",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PySide6>=6.0.0",
        "flask>=2.0.0",
        "flask-socketio>=5.0.0",
        "python-socketio>=5.0.0",
        "python-engineio>=4.0.0",
        "simple-websocket>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-qt>=4.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "build>=0.10.0",
            "twine>=4.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-qt>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "viloterm-demo=examples.simple_demo:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/vilosource/viloxtermjs/issues",
        "Source": "https://github.com/vilosource/viloxtermjs",
        "Documentation": "https://github.com/vilosource/viloxtermjs/wiki",
    },
)