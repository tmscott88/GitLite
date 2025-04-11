# README

> Written in Python 3, **GitWriting** is a command-line app built for writers/editors using Git. I created this app in order to streamline my creative writing and Git workflow into one lightweight app, transitioning away from heavier GUI-based apps like Obsidian, VSCode, etc. Spend more time writing and less time typing commands.
>
> Builds are available for Windows and Linux, with a macOS build in the works. If using macOS, you may download the `GitWriting` binary and execute that instead from `Terminal`. See below for how to install and use this app.

***BIG DISCLAIMER**: THIS APP IS STILL UNDER DEVELOPMENT! Right now, **GitWriting** works best with personal, linear, one-branch projects. More advanced Git operations like merging, rebasing, and merge conflict resolution are not implemented at this time.*

## Requirements

GitWriting supports most modern Linux distributions, macOS, and Windows 11/10/7. However, you may experience unexpected issues on older operating systems which may not support the dependencies below. GitWriting does not currently handle Git authentication or create Git repositories for you, though I am open to adding a feature like that, if the need arises.

- Git (configured and authenticated)
- A valid Git repository
- *Python 3 (only needed for development or building from source)*

## Usage

- Download and place the **GitWriting** executable for your platform `GitWriting-X-X-X.exe` for Windows, `GitWriting-X-X-X` for Unix in the root directory of your local Git repository.
- Add a new pattern to your repository's `.gitignore` if you don't want the app tracking, i.e. `*GitWriting*`
- Run: `GitWriting.exe | GitWriting [-OPTION]`
- Options: `[-h | --help | -H]` `[-o | --options | -O]` `[-v | --version | -V]`

Note: A `gitwriting.ini` configuration file must be created and placed in the repo's root directory (alongside the **GitWriting** executable) in order to save and read app settings. certain features will be limited or blocked. See below for a working template.

**GitWriting** is intended to work across terminals on Windows, macOS, and Linux.

*However, MacOS native builds are not working on my ancient MacBook Air, so Linux and Windows are the best platforms to use right now.*

## Features

*Note: Any additional "core plugins" like Daily Notes are disabled by default.*

### Interactive Setup

Upon launching GitWriting for the first time (or if you move the executable and forget to bring the config file over), you will see a few prompts. They ask which apps you would like to use.

For now, they just ask for your browser and editor of choice. As I develop more features, I plan to add more helpful interactions to the app.

First priority is ensuring everything works between Unix and Windows.

Second priority is learning and setting up `pyproject.toml` to streamline the distribution process.

### Start Menu

- New/Open File -> Simply open the editor defined in `gitwriting.ini` by passing a file name
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
- Based on your platfrm, run one of these command from the root directory of your Git repo to create a build.
- Like most other Python projects, app dependencies are located in `requirements.txt`, or see `Help -> View App Dependencies` within the app.
- (Optional, do at your own risk): Add `--noconfirm` to the end of the command chain to bypass the override warning.

### Windows & Linux (Recommended)

`pyinstaller -F -n GitWriting --add-data="gitwriting.ini;." --add-data="CHANGELOG.md;." --add-data="README.md;." --add-data="requirements.txt;." --recursive-copy-metadata readchar --recursive-copy-metadata pick main.py`

### macOS (NOT WORKING RIGHT NOW)

`-w | --windowed | --noconsole` enables building an OSX `.app` bundle and Unix executable instead of a `console` document

`pyinstaller -F -n GitWriting --add-data="gitwriting.ini:." --add-data="CHANGELOG.md:." --add-data="README.md:." --add-data="requirements.txt:." --recursive-copy-metadata readchar --recursive-copy-metadata pick main.py`

## Default Configuration File

*Note: This config is automatically generated if requested after launch. But here is a working file for reference.

### Unix

```ini
[PATHS]
editor = nano
browser = default
daily_notes = daily

[FLAGS]
daily_notes = off
browser_hidden_files = off
browser_readonly_mode = off
```

### Windows

```ini
[PATHS]
editor = notepad.exe
browser = default
daily_notes = daily

[FLAGS]
daily_notes = off
browser_hidden_files = off
browser_readonly_mode = off
```

1. Create `gitwriting.ini` in the project's root directory
2. Copy the attributes above to `gitwriting.ini`.
3. Each setting can be changed through the *Main Menu -> Settings* interface.
