#!/usr/bin/env bash
# Install Windows 11 Explorer to system / user menu
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/128x128/apps"

mkdir -p "$BIN_DIR" "$APP_DIR" "$ICON_DIR"

# Link launcher script into ~/.local/bin
ln -sf "$SCRIPT_DIR/run.sh" "$BIN_DIR/win11-explorer"

# Copy icon
cp -f "$SCRIPT_DIR/win11_explorer/resources/icons/explorer.png" "$ICON_DIR/win11-explorer.png"

# Install .desktop file
cat <<EOF > "$APP_DIR/win11-explorer.desktop"
[Desktop Entry]
Name=Windows 11 Explorer
GenericName=File Manager
Comment=Windows 11 File Explorer replica for Linux
Exec=$BIN_DIR/win11-explorer %U
Icon=win11-explorer
Terminal=false
Type=Application
Categories=System;FileTools;FileManager;Utility;
MimeType=inode/directory;
Keywords=folder;manager;explore;disk;filesystem;windows;
StartupNotify=true
StartupWMClass=File Explorer
EOF

update-desktop-database "$APP_DIR" 2>/dev/null || true

echo "Windows 11 Explorer successfully installed!"
echo "You can now launch it via:"
echo "  1) Command line: win11-explorer"
echo "  2) Application menu: Search for 'Windows 11 Explorer'"
echo "  3) From this folder: ./run.sh"
