#!/bin/sh

git fetch origin
git pull

GJTIFF_DIR=./gjtiff
GJTIFF_REPO_URL=https://github.com/MartinPulec/gjtiff.git

mkdir -p $GJTIFF_DIR

if [ -d "$GJTIFF_DIR/.git" ]; then
    echo "Repository exists, updating..."
    cd "$GJTIFF_DIR"
    git fetch origin
    git reset --hard origin/main
    echo "Repository updated."
else
    echo "Repository does not exist, cloning..."
    git clone "$GJTIFF_REPO_URL" "$GJTIFF_DIR"
    echo "Repository cloned."
fi

docker compose build --no-cache
docker compose up -d
