"""Contains pickers created using the 'pick' module"""

import os
from pick import pick, Option
import file_utils
import app_utils as app
from commands import AppCommand, GitCommand
from config import AppConfig

INDICATOR = "->"
QUIT_KEYS = (27, ord("q"))
QUIT_OPTION = Option("\n--------------\n(esc|q - quit)", enabled=False)

# class RecentsPicker(Picker):
#     """TODO Select a file from "Recents Menu. Toggle to sort by git status or recently modified/created"""
# pass

class CommitPicker():
    """Select a commit from git log output"""
    # esc, q => quit
    def show(self):
        """Display the commit picker"""
        cmd = GitCommand()
        options = cmd.get_commits()
        options.append(QUIT_OPTION)
        option, index = pick(options, indicator=INDICATOR, quit_keys=QUIT_KEYS)
        # Commit Hash
        if index in range (0, len(options) - 1):
            return option
        return None

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
        if self.is_at_root_directory(back_path):
            options.insert(start_index, Option(f"DIR: {self.start_path}", enabled=False))
        else:
            start_index = 1
            options.insert(0, Option(f"DIR: {self.current_path}", enabled=False))
            options.insert(start_index, "../")
        options.append(Option(f"[View Hidden Files: {is_browser_hidden_files}]"))
        options.append(Option(f"[Read-Only Mode: {is_browser_readonly_mode}]"))
        options.append(QUIT_OPTION)
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
        # Toggle Hidden Notes
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

    # def select_directory(self):
    #     """Display the file browser, starting at the specified path (Default=executable root). (DIRECTORIES ONLY)"""
    #     is_browser_hidden_files = self.app_cfg.is_browser_hidden_files_enabled()
    #     back_path = file_utils.get_path_head(self.current_path)
    #     options = file_utils.get_folders_in_directory(self.current_path, include_hidden=is_browser_hidden_files)
    #     options.insert(0, Option(f"DIR: {self.current_path}", enabled=False))
    #     options.insert(1, "../")
    #     options.append(Option(f"[View Hidden Files: {is_browser_hidden_files}]"))
    #     options.append(Option("[Confirm Folder & Quit]"))
    #     options.append(QUIT_OPTION)
    #     option, index = pick(options, indicator=INDICATOR, quit_keys=QUIT_KEYS)
    #     # print(f"Selected option {self.current_path} at index {index}, total options: {len(options)}")
    #     # Quit
    #     if index == len(options) or index == -1:
    #         return
    #     # Go Back
    #     if index == 1:
    #         # What happens once we reach the system's root path?
    #         self.current_path = back_path
    #         self.select_directory()
    #     # Toggle Hidden Notes
    #     elif index == len(options) - 3:
    #         if not is_browser_hidden_files:
    #             self.app_cfg.set_browser_hidden_files("on")
    #         else:
    #             self.app_cfg.set_browser_hidden_files("off")
    #         self.select_directory()
    #     # Select Folder
    #     elif index == len(options) - 2:
    #         # print(f"Confirm {self.current_path} at index {index}")
    #         app.change_working_directory(self.current_path)
    #         return
    #     # Next Folder
    #     elif index in range (1, len(options) - 3):
    #         next_path = os.path.join(self.current_path, option)
    #         self.on_select_path(next_path, select_folder_only=True)
