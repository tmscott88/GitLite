# README

> Written for Python 3.x, this is a command-line app meant to simplify common Git interactions from the command line.

***BIG DISCLAIMER**: THIS APP IS STILL IN DEVELOPMENT! At its core, **GitLite** is designed for personal, linear, one-branch projects. Merging, Rebasing, merge conflict resolution, and other "advanced" Git operations are not implemented at this time.*

*I am not responsible for headaches or heartbreaks if you rely on this script for a multi-million dollar, mission-critical project for your job. Just **please** use VSCode, SourceTree, or something more robust if that is you.*

## Usage

- Place the **GitLite-X.X.X** executable in the root directory of your local Git repository. Add an appropriate pattern to your repository's `.gitignore` if you don't want the app committed.
- Launch the executable.
- Run: `python3 | py gitlite.py [-OPTION]`
- Options: `[-h | --help | -H]` `[-o | --options | -O]` `[-v | --version | -V]`

Note: A `config.ini` configuration file must be created and placed in the repo's root directory (alongside the **GitLite** executable) in order to save and read app settings. certain features will be limited or blocked. See below for a working template.

**GitLite** is written to work across terminals on Windows, macOS, and Linux. MacOS builds are not building on my *ancient* MacBook Air, so Linux and Windows are the ideal platforms to use right now.

### Build from Source

- Install [PyInstaller](https://pyinstaller.org/en/stable/) using `pip`. See [here](https://pip.pypa.io/en/stable/installation/) if you do not already have `pip` installed with Python.
- Based on your platfrm, run one of these command from the root directory of your Git repo to create a build.

#### Windows & Linux (Recommended)

> pyinstaller -F -n GitLite --recursive-copy-metadata readchar gitlite.py

#### macOS (NOT WORKING RIGHT NOW)

`-w | --windowed | --noconsole` enables building an OSX `.app` bundle and Unix executable instead of a `console` document.

> pyinstaller -F -w -n GitLite --recursive-copy-metadata readchar gitlite.py

## Configuration File

```ini
[APPS]
browser = glow
editor = micro

[DAILY_NOTES]
status = off
path = daily

[MISC]
commit_limit = 15
```

1. Create `config.ini` in the project's root directory
2. Copy the attributes above to `config.ini`.
3. Each setting can be interactively modified through the *Main Menu -> Settings* interface.

## Features

### Start Menu

- New File -> Simply open the editor defined in `config.ini`
- Resume Work -> Choose from uncommited files
- Browse Files -> **Please install a command-line file browser to take advantage of this feature!**
- Open Daily Note (more info below)

### Daily Notes

Inspired by Obsidian, Daily Notes allow you to quickly create a diary within your project, organized by *Year/Year-Month/Year-Month-Day.md (e.g. 2025/2025-03/2025-03-01.md)* by default. I plan to add more flexibility to this path in a future release.

### Settings Menu

- Configure default browser, editor apps
- Enable/disable Daily Notes 
- Set default folder to create Daily Notes from
- Set max number of commits to display in menus where `git log...` is used

### Git Operations

- Fetch/Status
- Log (Default, Simple, Verbose)
- Diff (Interactive)
- Pull/Push (Normal)
- Stage (Quick, Interactive)
- Commit
- *Stash (Create, Apply, Pop, Drop) -> Coming Soon*
- Revert (Interactive Checkout)
- Discard (Interactive Clean)
- Reset (Mixed, Soft, Hard)
