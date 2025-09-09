# Git Hooks

This directory contains Git hooks for the viloxtermjs project to maintain code quality and commit standards.

## Available Hooks

### commit-msg
Validates commit messages to ensure they don't contain AI attributions or auto-generated markers.

**What it blocks:**
- AI tool attributions (Claude, ChatGPT, Copilot, etc.)
- Co-authored-by AI/bot messages
- Auto-generated markers
- AI-related emojis (🤖)

**Why:**
Commit messages should describe what changed and why, not how the code was created. This maintains a clean, professional commit history.

## Setup

Run the setup script from the repository root:

```bash
./setup-git-hooks.sh
```

This will configure Git to use the hooks in this directory.

## Manual Setup

If you prefer to set up manually:

```bash
git config core.hooksPath .githooks
```

## Disabling Hooks

To temporarily disable hooks:

```bash
git config --unset core.hooksPath
```

To re-enable:

```bash
git config core.hooksPath .githooks
```

## Bypassing Hooks (Emergency Only)

If you absolutely need to bypass the hooks:

```bash
git commit --no-verify -m "your message"
```

⚠️ **Warning:** Only use this in emergencies. The hooks exist to maintain code quality.

## Testing Hooks

To test if the commit-msg hook is working:

```bash
# This should fail
echo "test: add feature (Generated with Claude)" | .githooks/commit-msg /dev/stdin

# This should pass
echo "test: add feature" | .githooks/commit-msg /dev/stdin
```

## Adding New Hooks

1. Create a new executable script in `.githooks/`
2. Name it according to Git hook conventions (pre-commit, post-merge, etc.)
3. Make it executable: `chmod +x .githooks/hook-name`
4. Update this README with documentation

## Troubleshooting

**Hook not running:**
- Check if the hook is executable: `ls -la .githooks/`
- Verify Git is configured: `git config core.hooksPath`
- Ensure you're in the right repository

**Hook blocking valid commits:**
- Review the patterns in the hook script
- Consider if the message really needs AI attribution
- Use `--no-verify` as a last resort

## Contributing

When modifying hooks:
1. Test thoroughly before committing
2. Document any new patterns or rules
3. Keep error messages helpful and actionable
4. Maintain backwards compatibility