# CHANGELOG

This is the Python version of a Bash script which I wrote for basic Git repo interactions.

See below for what has been successfully ported from `start.sh` -> `start.py`, and what is in progress.

## Main Features

- [x] Initial arguments (-h, -v)
- [] Git functions
- [x] File editor integration
- [x] File browser integration

### Git Functions

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
    - [x] Prohibit stash if the script has pending changes
    - [] Create
    - [] Apply
    - [] Pop
    - [] Drop
- [x] Revert
- [x] Discard
- [] Reset
    - [x] Mixed
    - [] Hard
    - [] Soft
- [x] Quit

### Planned Features
- [x] Configuration file with basic settings

### Bugs

- [x] Menu disappears after Stage/Unstage changes within loop
    - Moved the "options" enumerator inside the function's while(True) loop.
- [x] Daily Note: Shows 'DIARY/' instead of the full path
    - Instead of `git status --short`, used `git status -s -u` for the relative path to each file
