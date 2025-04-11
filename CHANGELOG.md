# CHANGELOG

## (WIP) 0.8.7

- [?] Make certain pickers paginated to improve performance on repos with a long history; display the full details of the selected commit after selection
- [?] Rework "Open Recent" menu to list files by different filters (modification date, uncommitted, etc). Provide different options.

- [] **Make the app portable.** Provide picker for selecting a work directory. If the directory is within a valid git repo, enable the `Source Control` menu. If not, just let the app be a simple file manager.
- [] Add further config file verification. **Allow it to be placed anywhere within the repo**, so long as it can be found.
- [] Add branches, rebasing, merging?
- [] Add option/choice to automatically stage changes before stashing.
- [] Create better settings "picker" for the flag options.

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
