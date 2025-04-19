# README

> Written in Python 3, **GitWriting** is a command-line app built for writers/editors using Git. I created this app in order to streamline my creative writing and Git workflow into one lightweight app, transitioning away from heavier GUI-based apps like Obsidian, VSCode, etc. Spend more time writing and less time typing commands.
>
> Builds are available for Windows and Linux, with a macOS build in the works. If using macOS, you may download the `GitWriting` binary and execute that instead from `Terminal`. See below for how to install and use this app.

***BIG DISCLAIMER**: THIS APP IS STILL UNDER DEVELOPMENT! Right now, **GitWriting** works best with personal, linear, one-branch projects. More advanced Git operations like merging, rebasing, and merge conflict resolution are not implemented at this time.*

## Requirements

GitWriting supports most modern Linux distributions, macOS, and Windows 11/10/7. However, you may experience unexpected issues on older operating systems which may not support the dependencies below. GitWriting does not currently handle Git authentication or create Git repositories for you, though I am open to adding a feature like that, if the need arises.

- Git (configured and authenticated)
- A valid Git repository
- *Python 3.5+ (latest is recommended, only needed for manual builds or development), pyinstaller*

## Usage

- Download the **GitWriting** executable for your platform `GitWriting.exe` for Windows, `GitWriting`. I would recommend placing it inside your system's apps folder or a similar directory.
- Run: `GitWriting.exe | ./GitWriting [-OPTION]`
- Options: `[-h | --help | -H]` `[-o | --options | -O]` `[-v | --version | -V]`

**GitWriting** works on Windows and Unix.

## Features

*Note: Any additional "core plugins" like Daily Notes are disabled by default.*

### Interactive Setup

Upon launching GitWriting for the first time, you will see a few prompts to configure settings for the first time. To delete the config file, Choose `Settings -> Factory Reset`, and the app will return to default state.

### Start Menu

- New/Open File -> Simply open the editor by passing a file name
- Resume Work -> Choose from uncommited files. *In a future release, I plan to add an option to populate this list by different filters.*
- Browse Files -> **Please install a command-line file browser to take advantage of this feature!** *Though in a future release, I want to make an interactive browser that doesn't rely on Windows Explorer or a third party Unix browser.*
- Open Daily Note (more info below)

### Daily Notes

Inspired by Obsidian, Daily Notes allow you to quickly create a diary within your project, organized by *Year/Year-Month/Year-Month-Day.md (e.g. 2025/2025-03/2025-03-01.md)* by default. I plan to add more flexibility to this path in a future release.

### Settings Menu

- Configure default browser, editor apps
- Enable/disable Daily Notes
- Set default folder to create Daily Notes from
- "Factory Reset" (deletes the config file)

### Git Operations

- Fetch/Status
- Log
- Diff (View diff per file)
- Pull/Push (Normal)
- Stage (Quick, Interactive)
- Commit
- Stash (Create, Apply, Pop, Drop)
- Checkout (Interactive)
- Clean (Interactive)
- Reset (Mixed, Soft, Hard)

## Build from Source

- Install [PyInstaller](https://pyinstaller.org/en/stable/) using `pip`. See [here](https://pip.pypa.io/en/stable/installation/) if you do not already have `pip` installed with Python.
- App dependencies are located in `requirements.txt`. See `Help` within the app to view this this `README.md`, and the changelog, `CHANGELOG.md`.
- Make the build script executable: `chmod +x build.sh`
- Run the build script: `build.sh`

## Default Configuration File

*Note: The config file, `gitwriting.ini`, is automatically generated in your system's user config folder. Here are sample files by platform for your reference.*

- Windows: C:\Users\"User"\AppData\Local\GitWriting\gitwriting.ini
- Mac: /Users/"user"/Library/Application Support/GitWriting/gitwriting.ini
- Linux: /home/"user"/.config/GitWriting/gitwriting.ini
