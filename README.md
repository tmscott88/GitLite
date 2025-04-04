# README

> Written in Python 3, **GitWriting** is a command-line app built for writers/editors using Git. I created this app in order to streamline my creative writing and Git workflow into one lightweight app, transitioning away from heavier GUI-based apps like Obsidian, VSCode, etc. Spend more time writing and less time typing commands.
>
> Builds are available for Windows and Linux, with a macOS build in the works. If using macOS, you may download `gitwriting.py` and execute that instead from `Terminal`. See below for how to install and use this app.

***BIG DISCLAIMER**: THIS APP IS STILL UNDER DEVELOPMENT! Right now, **GitWriting** works best with personal, linear, one-branch projects. More advanced Git operations like merging, rebasing, and merge conflict resolution are not implemented at this time.*

## Usage

Using the executable

- Place the **GitWriting-X.X.X** executable in the root directory of your local Git repository. Add an appropriate pattern to your repository's `.gitignore`, i.e. `*GitWriting`
- Launch the executable.

Using the script

- Place the **gitwriting.py** script in the root directory of your local Git repository. Add an appropriate pattern to your repository's `.gitignore` if you don't want the app committed, i.e. `*GitWriting*`
- Run: `./gitwriting.py [-OPTION]`
  - If the script won't execute, update its permissions to be executable: `chmod +x gitwriting.py`
- Options: `[-h | --help | -H]` `[-o | --options | -O]` `[-v | --version | -V]`

Note: A `config.ini` configuration file must be created and placed in the repo's root directory (alongside the **GitWriting** executable) in order to save and read app settings. certain features will be limited or blocked. See below for a working template.

**GitWriting** is written to work across terminals on Windows, macOS, and Linux. MacOS native builds are not working on my *ancient* MacBook Air, so Linux and Windows are the best platforms to use right now.

### Build from Source

- Install [PyInstaller](https://pyinstaller.org/en/stable/) using `pip`. See [here](https://pip.pypa.io/en/stable/installation/) if you do not already have `pip` installed with Python.
- Based on your platfrm, run one of these command from the root directory of your Git repo to create a build.

#### Windows & Linux (Recommended)

> pyinstaller -F -n GitWriting --recursive-copy-metadata readchar gitwriting.py

#### macOS (NOT WORKING RIGHT NOW)

`-w | --windowed | --noconsole` enables building an OSX `.app` bundle and Unix executable instead of a `console` document.

> pyinstaller -F -w -n GitWriting --recursive-copy-metadata readchar gitwriting.py

## Configuration File

```ini
[APPS]
browser = glow
editor = micro

[DAILY_NOTES]
status = off
path = daily
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

Making some changes down here.
