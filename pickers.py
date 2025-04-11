"""Contains pickers created using the 'pick' module"""
import os
# import time
from pick import pick, Option
import file_utils
import app_utils as app
from commands import AppCommand
from config import AppConfig

INDICATOR = "->"
# esc, q => quit
QUIT_KEYS = (27, ord("q"))
QUIT_OPTION = Option("\n--------------\n(esc|q - quit)", enabled=False)

class Picker():
    """Pick one entry from a list of entries"""
    app_cfg = AppConfig(app.get_expected_config_path(), quiet=True)
    app_cmd = AppCommand()
    current_index = 0
    current_option = ""

    """Select a commit from git log output. total_entries is optional"""
    def __init__(self, title, populator, total_entries=-1):
        self.title = title
        self.populator = populator
        self.total_entries = int(total_entries)

    def show(self):
        """Initialize the picker (no pagination)"""
        is_browser_hidden_files = self.app_cfg.is_browser_hidden_files_enabled()
        is_browser_readonly_mode = self.app_cfg.is_browser_readonly_mode_enabled()
        options = self.populator()
        options.insert(0, Option(self.title, enabled=False))
        options.append(Option(f"[View Hidden Files: {is_browser_hidden_files}]"))
        options.append(Option(f"[Read-Only Mode: {is_browser_readonly_mode}]"))
        options.append(QUIT_OPTION)
        app.clear()
        # """Display and handle the picker interaction"""
        option, index = pick(options, indicator=INDICATOR, quit_keys=QUIT_KEYS)
        # print(f"Selected option {option} at index {index}, total options: {len(options)}")
        # Return the selected option
        if index in range (1, len(options) - 3):
            self.on_select_file(option)
            return option
        # Toggle Hidden Files
        if index == len(options) - 3:
            if not is_browser_hidden_files:
                self.app_cfg.set_browser_hidden_files("on")
            else:
                self.app_cfg.set_browser_hidden_files("off")
            self.show()
        # Toggle Read-Only Mode
        elif index == len(options) - 2:
            if not is_browser_readonly_mode:
                self.app_cfg.set_browser_readonly_mode("on")
            else:
                self.app_cfg.set_browser_readonly_mode("off")
            self.show()
        return None

    def show_paginated(self):
        """Initialize the picker"""
        options = []
        start_index = 0
        limit = 20
        next_index = limit * self.current_index
        # print(f"Current index = {self.current_index}")
        # print(f"Next index = {next_index}")
        # Handle the last pagination forward
        if next_index + limit >= self.total_entries:
            limit = self.total_entries - next_index
            # print(f"Next index {next_index} + limit {limit} >= total entries {self.total_entries}, limit = {limit}")
        options.append(Option(self.title, enabled=False))
        if self.current_index > 0:
            start_index = 1
            options.insert(1, "<-- Prev")
        if next_index < self.total_entries:
            options.extend(self.populator(index=next_index, limit=limit))
            options.append("Next -->")
        if limit <= 0:
            options.append(Option("No further entries.", enabled=False))
        options.append(QUIT_OPTION)

        # """Display and handle the picker interaction"""
        app.clear()
        option, index = pick(options, indicator=INDICATOR, quit_keys=QUIT_KEYS)
        # print(f"Selected option {option} at index {index}, total options: {len(options)}")
        # print(f"Start index = {start_index}")
        # <-- Previous Page
        if index == start_index:
            if self.current_index == 0:
                self.show_paginated()
            else:
                self.current_index -= 1
                self.show_paginated()
        # Next Page -->
        if index == len(options) - 2 and option.startswith("Next"):
            self.current_index += 1
            self.show_paginated()
        # Set option
        if index in range(start_index + 1, len(options) - 2):
            self.current_option = option
            # print(f"Index {index} is in range ({start_index + 1}, {len(options) - 2})")

    def on_select_file(self, fpath):
        """Handle the file selection"""
        if file_utils.is_file(fpath):
            if self.app_cfg.is_browser_readonly_mode_enabled():
                self.app_cmd.view_file(fpath)
            else:
                editor = self.app_cfg.get_app("editor")
                self.app_cmd.open_editor(editor, fpath)

class Browser():
    """Browse files and folders"""
    # esc, q => quit
    app_cfg = AppConfig(app.get_expected_config_path(), quiet=True)
    app_cmd = AppCommand()
    current_path = ""

    def __init__(self, start_path):
        self.start_path = start_path
        self.current_path = start_path

    def show(self):
        """Display the file browser, starting at start_path (Default=executable root)"""
        is_browser_hidden_files = self.app_cfg.is_browser_hidden_files_enabled()
        is_browser_readonly_mode = self.app_cfg.is_browser_readonly_mode_enabled()
        back_path = file_utils.get_path_head(self.current_path)
        options = file_utils.get_entries_in_directory(self.current_path,
            include_hidden=is_browser_hidden_files)
        start_index = 0
        options.insert(start_index, Option(f"DIR: {self.start_path}", enabled=False))
        if not self.is_at_root_directory(back_path):
            start_index = 1
            options.insert(start_index, "../")
        options.append(Option(f"[View Hidden Files: {is_browser_hidden_files}]"))
        options.append(Option(f"[Read-Only Mode: {is_browser_readonly_mode}]"))
        options.append(QUIT_OPTION)
        app.clear()
        option, index = pick(options, indicator=INDICATOR, quit_keys=QUIT_KEYS)
        # print(f"Selected option {option} at index {index}, total options: {len(options)}")
        # Quit
        if index == len(options) or index == -1:
            return
        # Go Back
        if index == start_index:
            if self.is_at_root_directory(back_path):
                self.show()
            else:
                self.current_path = back_path
                self.show()
        # Toggle Hidden Files
        elif index == len(options) - 3:
            if not is_browser_hidden_files:
                self.app_cfg.set_browser_hidden_files("on")
            else:
                self.app_cfg.set_browser_hidden_files("off")
            self.show()
        # Toggle Read-Only Mode
        elif index == len(options) - 2:
            if not is_browser_readonly_mode:
                self.app_cfg.set_browser_readonly_mode("on")
            else:
                self.app_cfg.set_browser_readonly_mode("off")
            self.show()
        # File or Folder
        elif index in range (start_index + 1, len(options) - 3):
            next_path = os.path.join(self.current_path, option)
            self.on_select_path(next_path, select_folder_only=False)

    def is_at_root_directory(self, pending_path):
        """Is the pending directory at a higher level than the starting directory?"""
        return bool(len(pending_path) < len(self.start_path))

    def on_select_path(self, next_path, select_folder_only=False):
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