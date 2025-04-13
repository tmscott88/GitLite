#!/bin/bash
# Ref.: https://www.pythonguis.com/tutorials/packaging-pyqt5-applications-pyinstaller-macos-dmg/


#################################################
# Print app information, prompt for build
#################################################
main() {
    echo "GitWriting Builder"
    echo "Author: Tom Scott (tmscott88)"
    PS3="Choose an option: "
    select opt in Build Quit; do
        case $opt in
        Build)
        build
        ;;
        Quit)
        exit 1
        ;;
        *)
        echo "Invalid choice"
        ;;
    esac
    REPLY=
    done
}

#################################################
# Create app file using pyinstaller
#################################################
build() {
    # Remove existing build data
    rm -rf ./build/* ./dist/*
    pyinstaller --name 'GitWriting' \
                --icon './src/gitwriting/github.ico' \
                --onefile  \
                --add-data='./src/gitwriting/requirements.txt:.' \
                --add-data='./CHANGELOG.md:.' \
                --add-data='./README.md:.' \
                --recursive-copy-metadata 'appdirs' \
                --recursive-copy-metadata 'readchar' \
                './src/gitwriting/main.py'
}

main
