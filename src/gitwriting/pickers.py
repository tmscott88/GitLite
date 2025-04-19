"""Contains pickers created using the 'pick' module"""
# Python Modules
import os
from curses import KEY_LEFT, KEY_RIGHT
# My Modules
from picker import pick, Option, CONFIRM_KEYS
import file_utils
import app_utils as app
from commands import AppCommand, GitCommand
from config import AppConfig

# esc, q => quit
QUIT_KEYS = (27, ord("q"))

class DataPicker():
    """Pick one entry from a list of entries"""
    app_cfg = AppConfig(quiet=True)
    app_cmd = AppCommand()
    current_index = 0
    current_option = ""

    def __init__(self, title, populator, total_entries=-1, default_index=0):
        """Select a commit from git log output.
        To show all entries on one page, set total_entries = -1"""
        self.title = title
        self.populator = populator
        self.total_entries = int(total_entries)
        self.default_index = default_index

    def show(self):
        """Initialize the picker without pagination (one scrolling page)"""
        help_option = "(esc|q - quit, enter - select)"
        options = self.populator()
        if options is None:
            options = []
            options.append("No data entries.")
        app.clear(delay=0.05)
        # """Display and handle the picker interaction"""
        option, key_code = pick(options,
            title=self.title,
            footer=help_option,
            quit_keys=QUIT_KEYS,
            default_index=self.default_index)
        # Quit
        if key_code in QUIT_KEYS:
            return None
        # Confirm option
        if key_code in CONFIRM_KEYS:
            return option[0]
        return None

    def show_paginated(self):
        """Initialize the picker"""
        help_option = "(esc|q - quit, enter - select, <-- Prev | Next -->)"
        back_option = "../"
        app.clear(delay=0.05)
        options = []
        limit = 20
        next_index = limit * self.current_index
        # Handle the last pagination forward
        if next_index + limit >= self.total_entries:
            limit = self.total_entries - next_index
        if limit <= 0:
            options.append(back_option)
            options.append(Option("No more entries.", enabled=False))
        if next_index < self.total_entries:
            options.extend(self.populator(index=next_index, limit=limit))
        option, key_code = pick(options,
            title=self.title,
            footer=help_option,
            quit_keys=QUIT_KEYS,
            is_paginated=True)
        # Quit
        if option is None or key_code in QUIT_KEYS:
            return
        # Go Back
        if key_code == KEY_LEFT or (option[0] == back_option and key_code != KEY_RIGHT):
            if self.current_index == 0:
                self.show_paginated()
            else:
                self.current_index -= 1
                self.show_paginated()
        # Go Forward
        elif key_code == KEY_RIGHT:
            if limit <= 0:
                self.show_paginated()
            else:
                self.current_index += 1
                self.show_paginated()
        # Pick Option
        elif key_code in CONFIRM_KEYS and option[0] and limit > 0:
            self.current_option = option[0]

class FileBrowser():
    """Browse files and folders"""
    # esc, q => quit
    app_cfg = AppConfig(quiet=True)
    app_cmd = AppCommand()
    git_cmd = GitCommand()
    current_path = ""
    back_option = "../"
    help_option = "(esc|q - quit, enter - select)"
    help_option_full = "(esc|q - quit, enter - edit, v - view, h - hidden files)"
    OPTION_KEYS = (ord('h'), ord('v'))

    def __init__(self, start_path):
        self.start_path = start_path
        self.current_path = start_path

    def show(self):
        """Display the file browser, starting at start_path (Default=executable root)"""
        app.clear(delay=0.05)
        is_browser_hidden_files = self.app_cfg.is_browser_hidden_files_enabled()
        back_path = os.path.dirname(self.current_path)
        options = []
        first_opt_index = 1
        # Check for read access first
        if not os.access(self.current_path, os.R_OK):
            options.append(Option(f"DIR: {self.current_path}", enabled=False))
            options.append(self.back_option)
            options.append(Option("Read access denied.", enabled=False))
        else:
            options = file_utils.get_entries_in_directory(self.current_path,
                include_hidden=is_browser_hidden_files)
            # Then get the directory's entries
            if not options:
                options = []
                options.append(self.back_option)
            else:
                if not self.__is_at_root_directory(back_path):
                    options.insert(0, self.back_option)
                else:
                    first_opt_index = 0
        option, key_code = pick(options,
            title=f"DIR: {self.current_path}",
            footer=self.help_option_full,
            default_index=first_opt_index,
            option_keys=self.OPTION_KEYS,
            quit_keys=QUIT_KEYS, is_paginated=False)
        # Quit
        if option is None or key_code in QUIT_KEYS:
            self.current_path = None
            return
        # Go Back
        if option[0] == self.back_option and key_code != ord('h'):
            if self.__is_at_root_directory(back_path):
                self.show()
            else:
                self.current_path = back_path
                self.show()
        elif key_code == ord("h"):
            if not is_browser_hidden_files:
                self.app_cfg.set_browser_hidden_files("on")
            else:
                self.app_cfg.set_browser_hidden_files("off")
            self.show()
        # Open File or Folder
        elif (key_code in CONFIRM_KEYS or key_code == ord('v')):
            if option[0] and option[1] >= first_opt_index and key_code:
                next_path = os.path.normpath(os.path.join(self.current_path, option[0]))
                self.__on_select_path(key_code, next_path, select_folder_only=False)

    def __is_at_root_directory(self, pending_path):
        """Is the specified directory at a higher level than the starting directory?"""
        return bool(len(pending_path) < len(self.start_path))

    def __on_select_path(self, key_code, next_path, select_folder_only=False):
        """Navigate up or down the directory tree (usually one level).
        Triggers file editor by default"""
        if file_utils.is_file(next_path):
            if key_code == ord('v'):
                self.app_cmd.view_file(next_path)
            elif key_code in CONFIRM_KEYS:
                editor = self.app_cfg.get_app("editor")
                self.app_cmd.open_editor(editor, next_path)
        elif file_utils.is_directory(next_path):
            self.current_path = next_path
            if select_folder_only:
                self.select_directory()
            else:
                self.show()

    def select_directory(self):
        """Display the file browser, starting at the specified path (Default=executable root). 
            (DIRECTORIES ONLY)"""
        app.clear(delay=0.05)
        back_path = os.path.dirname(self.current_path)
        options = file_utils.get_folders_in_directory(self.current_path, include_hidden=False)
        if not options:
            options = []
            options.append(self.back_option)
        else:
            options.insert(0, self.back_option)
        if not os.access(self.current_path, os.R_OK):
            options.append(Option("Read access denied. Please choose a different folder.",
                enabled=False))
        else:
            options.append("[Select Folder]")
        option, key_code = pick(options,
            title=f"DIR: {self.current_path}",
            footer=self.help_option,
            quit_keys=QUIT_KEYS)
        # Quit
        if option is None or key_code in QUIT_KEYS:
            self.current_path = None
            return
        # Go Back
        if option[0] == self.back_option:
            if os.access(back_path, os.R_OK):
                self.current_path = back_path
                self.select_directory()
        # Select Folder
        elif option[1] == len(options):
            return
        # Next Folder
        elif option[0] and option[1] in range(1, len(options) - 1):
            next_path = os.path.normpath(os.path.join(self.current_path, option[0]))
            self.__on_select_path(option, next_path, select_folder_only=True)
