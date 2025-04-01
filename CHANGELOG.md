# CHANGELOG

See below for what has been successfully ported from `start.sh` -> `gitlite.py`, and what reamins in development. I started at version 0.8.0 for this repo since I already migrated about 80% of the former script to the current script.

## (TBD) 0.8.5

- [] Interactive "Setup" menu - make **GitLite** friendlier. If config file doesn't exist, ask to auto-generate new file with appropriate parameters
- [] Add further config file verification, section by section, key by key
- [] Keep the app as flexible as possible, even without a valid config file. Use reasonable defaults, perhaps offer to create the config.ini file with pre-populated vallues. Upload to the repo without including it in tracking.
- [] Rework "Open Recent" menu to list files by different filters (modification date, uncommitted, etc). Provide different options.
- [] Create "Diff" menu; Show `git diff` by choice of file rather than for all tracked, uncommitted files at once.
- [] Create a custom file browser (similar to the Log menu)

## (WIP) 0.8.4

- [x] Add "About" option to main menu
- [x] Improve Settings menu to mimic `config.ini` structure. See `README.md` for the new base config file.
- [x] Remove unnecessary shell calls, change all subprocess calls to explicit parts
- [x] Improve error when an app cannot be found or crashes on execution.
- [x] CRITICAL: prevent GitLite from attempting to load external app when invalid app reference is set in `config.ini` (i.e. by manual intervention, a previous session) outside of the Settings Menu.

- [] Feature: Add stashing
- [] Cross-platform fixes (Windows, macOS, Linux)
- [] BUG: macOS build not reading directory properly.
- [] Improve/clarify initial arguments

## 0.8.3

- Add more settings
  - Commit Limit (for Git Log, Git Reset)
- Rewrite prompt menu labels and feedback to be more intuitive
  - Improved formatting for this feedback
- Lots of refactoring

## 0.8.2

New Features

- Feature: Configuration file with basic settings
- Various Bugfixes
  - Fix for menu disappears after Stage/Unstage changes within loop
    - Moved the "options" enumerator inside the function's while(True) loop.
  - Daily Note: Shows 'DIARY/' instead of the full path
    - Instead of `git status --short`, used `git status -s -u` for the relative path to each file
  - Do not allow negative number input in menus

## 0.8.0 - 0.8.1

- ~80% migrated functions from Bash -> Python
- Basic file editor integration
- Basic file browser integration
- Planning & Testing

## Development

### Git Functions

- [x] Prohibit `stash`, `reset` if the script has pending changes
- [x] Start
  - [x] New
  - [x] Resume
  - [x] Browse
  - [x] Daily Note
  - [x] Cancel
- [x] Fetch
- [x] Log
  - [x] Standard
  - [x] Simple
  - [x] Verbose
- [x] Diff
- [x] Pull
- [x] Push
- [x] Stage
  - [x] Stage All
  - [x] Unstage All
  - [x] Interactive
- [x] Commit
  - [x] Message
  - [x] No Message (cancel)
- [] Stash
  - [] Create
  - [] Apply
  - [] Pop
  - [] Drop
- [x] Revert
- [x] Discard
- [x] Reset
  - [x] Mixed
  - [x] Hard
  - [x] Soft
- [x] Quit
