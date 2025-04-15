# CHANGELOG

## (TBD) 0.8.8

- [] Config profiles (different config file for each repository)
- [?] Recents menu: Store recents in a JSON file instead of walking the entire directory & subdirectories
  - [X] Shows most recent files
- [] Favorites menu?
- [] Shortcut to search for files within browser
- [] Interactive Git repo setup?
- [] Add branches, rebasing, merging?
- [] Add option/choice to automatically stage changes before stashing.
- [] Create better settings "picker" for the flag options.

## 0.8.7

- [X] **Make the app portable.** Generate config file inside the user's system config folder instead of the current working directory
- [X] Rework "Open Recent" menu to list files by different filters (modification date, uncommitted, etc). Provide different options.
- [X] Fork `pick` -> `picker` and fix flickering when the screen re-renders. Instead of clearing the curses screen, [erase it](https://lists.gnu.org/archive/html/bug-ncurses/2014-01/msg00007.html).
- [X] Display the full details of the selected commit after selection

## 0.8.6

- [x] Nest Git functions into a [Git] submenu (reduce clutter)
- [x] Create a custom file browser (similar to the Log menu), with read-only mode and hidden files toggle
- [x] Add the config file as a PyInstller resource to the app's build data.
- [x] If the working directory is not at the root of a Git repository, the `File` operations may still be used, but `Source Control` will be disabled.  

## 0.8.5

- [x] Major Refactoring: Split the main script into new modules
- [x] Add interactive "Setup" menu - If config file doesn't exist, walk through creating a new file instead of throwing ambiguous errors.
- [x] If an invalid app is specified during configuration, retry the input prompt
- [x] Add "Help" menu with offline access to the README
- [] BUG: macOS build not reading directory properly.

## 0.8.4

- [x] Feature: Add stashing
- [x] Add "About" option to main menu
- [x] Improve Settings menu to mimic `app_cfg.ini` structure. See `README.md` for the new base config file.
- [x] Remove unnecessary shell calls, change all subprocess calls to explicit parts
- [x] CRITICAL: prevent GitLite from attempting to load external app when invalid app reference is set in `app_cfg.ini` (i.e. by manual intervention, a previous session) outside of the Settings Menu.
- [x] Improve/clarify initial arguments
- [x] "View Diff" menu; Show `git diff` by choice of file rather than for all tracked, uncommitted files at once.

- [x] Cross-platform fixes (Windows, macOS, Linux)

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
