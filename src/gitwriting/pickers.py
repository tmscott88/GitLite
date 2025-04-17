"""Contains pickers created using the 'pick' module"""
# Python Modules
import os
# My Modules
from picker import pick, Option
import file_utils
import app_utils as app
from commands import AppCommand, GitCommand
from config import AppConfig

# esc, q => quit
QUIT_KEYS = (27, ord("q"))
QUIT_OPTION = Option("\n--------------\n(esc|q - quit)", enabled=False)

class Picker():
    """Pick one entry from a list of entries"""
    app_cfg = AppConfig(quiet=True)
    app_cmd = AppCommand()
    current_index = 0
    current_option = ""

    """Select a commit from git log output. To show all entries on one page, set total_entries = -1"""
    def __init__(self, title, populator, total_entries=-1, default_index=0):
        self.title = title
        self.populator = populator
        self.total_entries = int(total_entries)
        self.default_index = default_index

    def show(self):
        """Initialize the picker without pagination (one scrolling page)"""
        options = []
        if self.populator is not None:
            options = self.populator()
            options.insert(0, Option(self.title, enabled=False))
        else:
            options.append(Option(self.title, enabled=False))
        options.append(QUIT_OPTION)
        app.clear(delay=0.05)
        # """Display and handle the picker interaction"""
        option, _ = pick(options, quit_keys=QUIT_KEYS, default_index=self.default_index)
        return option

    def show_paginated(self):
        """Initialize the picker"""
        app.clear(delay=0.05)
        options = []
        limit = 20
        opt_previous = "<-- Prev"
        opt_next = "Next -->"
        next_index = limit * self.current_index
        # Handle the last pagination forward
        if next_index + limit >= self.total_entries:
            limit = self.total_entries - next_index
        options.append(Option(self.title, enabled=False))
        if self.current_index > 0:
            options.insert(1, opt_previous)
        if next_index < self.total_entries:
            options.extend(self.populator(index=next_index, limit=limit))
            options.append(opt_next)
        if limit <= 0:
            options.append(Option("No further entries.", enabled=False))
        options.append(QUIT_OPTION)
        option, _ = pick(options, quit_keys=QUIT_KEYS)
        # Quit
        if not option:
            return
        # Go Back
        if option == opt_previous:
            if self.current_index == 0:
                self.show_paginated()
            else:
                self.current_index -= 1
                self.show_paginated()
        # Go Forward
        elif option == opt_next:
            self.current_index += 1
            self.show_paginated()
        # Pick Option
        else:
            self.current_option = option

class Browser():
    """Browse files and folders"""
    # esc, q => quit
    app_cfg = AppConfig(quiet=True)
    app_cmd = AppCommand()
    git_cmd = GitCommand()
    current_path = ""

    def __init__(self, start_path, config_mode=False):
        self.start_path = start_path
        self.current_path = start_path
        self.config_mode = config_mode

    def show(self):
        """Display the file browser, starting at start_path (Default=executable root)"""
        app.clear(delay=0.05)
        is_browser_hidden_files = self.app_cfg.is_browser_hidden_files_enabled()
        is_browser_readonly_mode = self.app_cfg.is_browser_readonly_mode_enabled()
        back_path = file_utils.get_path_head(self.current_path)
        start_index = 0
        options = []
        # Check for read access first
        if not self.config_mode:
            if not os.access(self.current_path, os.R_OK):
                start_index = 1
                options.append(Option(f"DIR: {self.current_path}", enabled=False))
                options.append("../")
                options.append(Option("Read access denied.", enabled=False))
            else:
                options = file_utils.get_entries_in_directory(self.current_path,
                    include_hidden=is_browser_hidden_files)
                # Then get the directory's entries
                if not options:
                    start_index = 1
                    options = []
                    options.append(Option(f"DIR: {self.current_path}", enabled=False))
                    options.append("../")
                else:
                    options.insert(start_index, Option(f"DIR: {self.current_path}", enabled=False))
                    if not self.__is_at_root_directory(back_path):
                        start_index = 1
                        options.insert(start_index, "../")
        options.append(f"[View Hidden Files: {is_browser_hidden_files}]")
        options.append(f"[Read-Only Mode: {is_browser_readonly_mode}]")
        options.append(QUIT_OPTION)
        option, index = pick(options, quit_keys=QUIT_KEYS)
        # Quit
        if not option:
            self.current_path = None
            return
        if not self.config_mode:
            # Go Back
            if index == start_index:
                if self.__is_at_root_directory(back_path):
                    self.show()
                else:
                    self.current_path = back_path
                    self.show()
        # Toggle Hidden Files
        if option.startswith("[View Hidden"):
            if not is_browser_hidden_files:
                self.app_cfg.set_browser_hidden_files("on")
            else:
                self.app_cfg.set_browser_hidden_files("off")
            self.show()
        # Toggle Read-Only Mode
        elif option.startswith("[Read-Only"):
            if not is_browser_readonly_mode:
                self.app_cfg.set_browser_readonly_mode("on")
            else:
                self.app_cfg.set_browser_readonly_mode("off")
            self.show()
        # Open File or Folder
        elif index in range (start_index + 1, len(options) - 3):
            next_path = os.path.join(self.current_path, option)
            self.__on_select_path(next_path, select_folder_only=False)

    def __is_at_root_directory(self, pending_path):
        """Is the pending directory at a higher level than the starting directory?"""
        return bool(len(pending_path) < len(self.start_path))

    def __on_select_path(self, next_path, select_folder_only=False):
        """Navigate up or down the directory tree (usually one level)"""
        if file_utils.is_file(next_path):
            if self.app_cfg.is_browser_readonly_mode_enabled():
                self.app_cmd.view_file(next_path)
            else:
                editor = self.app_cfg.get_app("editor")
                self.app_cmd.open_editor(editor, next_path)
        elif file_utils.is_directory(next_path):
            self.current_path = next_path
            if select_folder_only:
                self.select_directory()
            else:
                self.show()

    def select_directory(self):
        """Display the file browser, starting at the specified path (Default=executable root). (DIRECTORIES ONLY)"""
        app.clear(delay=0.05)
        back_path = file_utils.get_path_head(self.current_path)
        options = file_utils.get_folders_in_directory(self.current_path, include_hidden=False)
        if not options:
            options = []
            options.append(Option(f"DIR: {self.current_path}", enabled=False))
            options.append("../")
        else:
            options.insert(0, Option(f"DIR: {self.current_path}", enabled=False))
            options.insert(1, "../")
        if not os.access(self.current_path, os.R_OK):
            options.append(Option("Read access denied. Please choose a different folder.", enabled=False))
        else:
            options.append("[Confirm Folder & Quit]")
        options.append(QUIT_OPTION)
        option, index = pick(options, quit_keys=QUIT_KEYS)
        # Quit
        if not option:
            self.current_path = None
            return
        # Go Back
        if option == "../":
            if os.access(back_path, os.R_OK):
                self.current_path = back_path
                self.select_directory()
        # Select Folder
        elif option.startswith("[Confirm"):
            return
        # Next Folder
        elif index in range (1, len(options) - 2):
            next_path = os.path.join(self.current_path, option)
            if os.access(next_path, os.R_OK):
                self.__on_select_path(next_path, select_folder_only=True)
