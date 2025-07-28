#!/bin/sh
set -e
ZIP_NAME="Hecate_ios.zip"

# Remove old archive if exists
[ -f "$ZIP_NAME" ] && rm "$ZIP_NAME"

zip -r "$ZIP_NAME" "index.html" "README.md" "OK workspaces/hecate.py" "OK workspaces/main. py"

echo "Created $ZIP_NAME with project files for iOS deployment."
