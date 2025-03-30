# README

> Written for Python 3.x, this is a script meant to simplify common Git interactions from the command line.

***Big Disclaimer**: At its core, **GitLite** is designed for personal, linear, one-branch projects. Merging, Rebasing, merge conflict resolution, and other "advanced" Git operations are not implemented at this time.*

*I am not responsible for headaches and heartbrack if you trust this script with say, a multi-million dollar, mission-critical project for your job. Just **pretty please** use VSCode, SourceTree, or something more robust if that is you.*

## Usage

- Place this script in the root directory `/` of your repository.
- `python3 | py gitlite.py [-OPTION]`
- Options: `[-h | --help | -H]` `[-o | --options | -O]` `[-v | --version | -V]`

## Configuration File

1. Make a file in the project's root directory called `config.ini`.
2. Copy the attributes below to `config.ini`.
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

Inspired by Obsidian, Daily Notes allow you to quickly create a diary within your project, organized by *Year/Year-Month/Year-Month-Day.md (e.g. 2025-03/2025-03-01.md)* by default.

```ini
[DEFAULT]
browser = glow ; Highly recommended if using a vault of Markdown files
editor = nano
commit_limit = 10

[DAILY_NOTES]
status = true
path = DAILY
```
