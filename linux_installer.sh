/bash
=== Installing PyDictionary ===

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "ERROR: PYTHON3 ISN'T INSTALLED, PLEASE INSTALL IT THEN TRY AGAIN"
    exit 1
fi

# check for Tkinter
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "ERROR: TKINTER ISN'T INSTALLED, PLEASE INSTALL IT THEN TRY AGAIN"
    exit 1
fi

# Install PyInstaller
echo "Installing PyInstaller..."
pip3 install --user pyinstaller

# Build the app
echo "Building the app..."
pyinstaller --onefile --windowed app.py

# Create App Shortcut
echo "Creating application menu shortcut..."
mkdir -p ~/.local/share/applications

CURRENT_DIR=$(pwd)
EXEC_PATH="$CURRENT_DIR/dist/app"
DESKTOP_FILE="$HOME/.local/share/applications/PyDictionary.desktop"

cat << EOF >> "$DESKTOP_FILE"
[Desktop Entry]
Name=PyDictionary
Comment=Conlang Python Lexicon Application
Exec=$EXEC_PATH
Terminal=false
Type=Application
Categories=Utility;Education;
EOF

chmod +x "$DESKTOP_FILE"
update-desktop-database ~/.local/share/applications 2>/dev/null

echo "=== Installation Complete! ==="