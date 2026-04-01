#!/bin/bash
# install.sh — Install skill-creator to ~/.claude/skills/skill-creator/
set -e

SKILL_NAME="skill-creator"
SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)/skills/$SKILL_NAME"
TARGET_DIR="$HOME/.claude/skills/$SKILL_NAME"

# Check source exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory not found: $SOURCE_DIR" >&2
    exit 1
fi

# Check Python 3
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 not found. Install Python 3.8+ first." >&2
    exit 1
fi

# Check/install pyyaml (required for YAML API spec support)
if ! python3 -c "import yaml" &>/dev/null; then
    echo "Installing pyyaml (required for YAML spec parsing)..."
    if python3 -m pip install pyyaml -q 2>/dev/null || \
       python3 -m pip install pyyaml -q --break-system-packages 2>/dev/null; then
        echo "pyyaml installed."
    else
        echo "Warning: Could not install pyyaml automatically."
        echo "  YAML spec parsing will not work until you run: pip3 install pyyaml"
    fi
fi

# Check for existing install
if [ -d "$TARGET_DIR" ]; then
    echo "Skill '$SKILL_NAME' already installed at $TARGET_DIR"
    read -p "Overwrite? [y/N] " answer
    case "$answer" in
        [yY]|[yY][eE][sS]) rm -rf "$TARGET_DIR" ;;
        *) echo "Aborted."; exit 0 ;;
    esac
fi

# Install
mkdir -p "$TARGET_DIR"
cp -R "$SOURCE_DIR"/* "$TARGET_DIR"/
chmod +x "$TARGET_DIR"/scripts/*.py

echo ""
echo "Installed skill-creator to $TARGET_DIR"
echo ""
echo "Usage:"
echo "  In Claude Code, say: 'Create a skill for <API_URL>'"
echo "  Or directly:"
echo "    python3 $TARGET_DIR/scripts/fetch_docs.py <URL> | \\"
echo "    python3 $TARGET_DIR/scripts/generate_skill.py --name <service> --output ~/.claude/skills/<service>"
