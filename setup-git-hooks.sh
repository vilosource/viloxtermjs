#!/bin/bash
# Setup script to install Git hooks for this repository

echo "Setting up Git hooks for viloxtermjs..."

# Configure Git to use the .githooks directory
git config core.hooksPath .githooks

if [ $? -eq 0 ]; then
    echo "✅ Git hooks successfully configured!"
    echo ""
    echo "The following hooks are now active:"
    echo "  • pre-commit: Automatically formats Python files with black"
    echo "  • commit-msg: "
    echo "      - Enforces conventional commit format (feat:, fix:, etc.)"
    echo "      - Prevents AI attributions in commit messages"
    echo ""
    echo "Conventional commit types:"
    echo "  feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert"
    echo ""
    echo "To disable hooks temporarily, run:"
    echo "  git config --unset core.hooksPath"
    echo ""
    echo "To re-enable hooks, run:"
    echo "  git config core.hooksPath .githooks"
else
    echo "❌ Failed to configure Git hooks"
    exit 1
fi