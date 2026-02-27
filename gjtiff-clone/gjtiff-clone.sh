#!/bin/sh

REPO_DIR=/gjtiff
REPO_URL=https://github.com/MartinPulec/gjtiff.git

if [ -d "$REPO_DIR/.git" ]; then
    echo "Repository exists, updating..."
    cd "$REPO_DIR"
    git fetch origin
    git reset --hard origin/main
    echo "Repository updated."
else
    echo "Repository does not exist, cloning..."
    git clone "$REPO_URL" "$REPO_DIR"
    echo "Repository cloned."
fi