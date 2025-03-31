# README

> Written for Python 3.x, this is a script meant to simplify common Git interactions from the command line.

***Big Disclaimer**: At its core, **GitLite** is designed for personal, linear, one-branch projects. Merging, Rebasing, merge conflict resolution, and other "advanced" Git operations are not implemented at this time.*

*I am not responsible for headaches and heartbrack if you trust this script with say, a multi-million dollar, mission-critical project for your job. Just **pretty please** use VSCode, SourceTree, or something more robust if that is you.*

## Platforms (and caveats/specifics for each)

### Windows

- If `config.ini` is not found, GitLite will open the default text/Markdown editor.

### macOS/Linux

## Usage

- Place the **GitLite** executable in the root directory of your local Git repository. Add it to your repository's `.gitignore` if desired.
- Launch the executable.
  - If you do not have a `config.ini` configuration file in the repo's root directory as well, you will see an error when accessing the *Start* or *Settings* menus. Since **GitLite** is written to work across terminals on Windows, macOS, and Linux, this file is necessary to...
- `python3 | py gitlite.py [-OPTION]`
- Options: `[-h | --help | -H]` `[-o | --options | -O]` `[-v | --version | -V]`

### Build from Source

- Install [PyInstaller](https://pyinstaller.org/en/stable/) using `pip`. See [here](https://pip.pypa.io/en/stable/installation/) if you do not already have `pip` installed with Python.
- Run this command from the root project directory to create a build.

> pyinstaller --onefile --name GitLite --recursive-copy-metadata readchar gitlite.py

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
- Browse Files -> **Please install a file browser to take advantage of this feature!**
- Open Daily Note (more info below)

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

### Daily Notes

Inspired by Obsidian, Daily Notes allow you to quickly create a diary within your project, organized by *Year/Year-Month/Year-Month-Day.md (e.g. 2025/2025-03/2025-03-01.md)* by default.
