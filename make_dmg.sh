#!/bin/sh
# Ref.: https://www.pythonguis.com/tutorials/packaging-pyqt5-applications-pyinstaller-macos-dmg/

rm -rf build dist/*

#################################################
# Create app file using pyinstaller
#################################################

pyinstaller --name 'GitWriting' \
            --icon 'github.ico' \
            --windowed  \
            --add-data='./gitwriting.ini:.' \
            --add-data='./requirements.txt:.' \
            --add-data='./CHANGELOG.md:.' \
            --add-data='./README.md:.' \
            --recursive-copy-metadata 'readchar' \
            --recursive-copy-metadata 'pick' \
            main.py

#################################################
# Build the application bundle into a disk image
#################################################

# Create a folder (named dmg) to prepare our DMG in 
# (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -rf dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/GitWriting.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/GitWriting.dmg" && rm "dist/GitWriting.dmg"
create-dmg \
  --volname "GitWriting" \
  --volicon "github.ico" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "GitWriting.app" 175 120 \
  --hide-extension "GitWriting.app" \
  --app-drop-link 425 120 \
  "dist/GitWriting.dmg" \
  "dist/dmg/"
