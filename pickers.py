import os
from pick import pick, Option
import file_utils as file
import app_utils as app
from commands import AppCommand, GitCommand
from config import AppConfig

class RecentsPicker:
    """TODO Select a file from "Recents Menu. Toggle to sort by git status or recently modified/created"""
    pass

class CommitPicker:
    """Select a commit from git log output"""
    # esc, q => quit
    QUIT_KEYS = (27, ord("q"))
    
    def show(self):
        cmd = GitCommand()
        """Display the commit picker""" 
        options = cmd.get_commits()
        start_index = 0
        options.append(Option("\n--------------\n(esc|q - quit)", enabled=False))
        option, index = pick(options, indicator="->", quit_keys=self.QUIT_KEYS)
        # Quit
        if index == len(options) or index == -1:
            return
        # Commit Hash
        elif index in range (0, len(options) - 1):
            return option

class Browser:
    """Browse files and folders"""
    # esc, q => quit
    QUIT_KEYS = (27, ord("q"))
    config = AppConfig()
    app_cmd = AppCommand()
    __current_path = ""

    def __init__(self, start_path):
        self.start_path = start_path
        self.__current_path = start_path

    def show(self):
        """Display the file browser, starting at the specified path (Default=executable root)""" 
        is_hidden_files = self.config.is_hidden_files_enabled()
        back_path = file.get_one_directory_higher(self.__current_path)
        options = file.get_files_in_directory(self.__current_path, include_hidden=is_hidden_files)
        start_index = 0
        if self.is_at_root_directory(back_path):
            options.insert(start_index, Option(f"DIR: {self.start_path}", enabled=False))
        else:
            start_index = 1
            options.insert(0, Option(f"DIR: {self.__current_path}", enabled=False))
            options.insert(start_index, "../")
        options.append(Option(f"Hidden Files: {is_hidden_files}"))
        options.append(Option("\n--------------\n(esc|q - quit)", enabled=False))
        option, index = pick(options, indicator="->", quit_keys=self.QUIT_KEYS)
        # print(f"Selected option {option} at index {index}, total options: {len(options)}")
        # Quit
        if index == len(options) or index == -1:
            return
        # Go Back
        elif index == start_index:
            if self.is_at_root_directory(back_path):
                self.show()
            else:
                self.__current_path = back_path
                self.show()
        # Toggle Hidden Notes
        elif index == len(options) - 2:
            if not is_hidden_files:
                self.config.set_hidden_files("on")
            else:
                self.config.set_hidden_files("off")
            self.show()
        # File or Folder
        elif index in range (start_index + 1, len(options) - 2):
            next_path = os.path.join(self.__current_path, option)
            self.on_select(next_path)

    def is_at_root_directory(self, pending_path):
        return bool(len(pending_path) < len(self.start_path))

    def on_select(self, next_path):
        """Navigate up or down the directory tree (usually one level)"""
        if file.is_file(next_path):
            editor = self.config.get_app("editor")
            self.app_cmd.open_editor(editor, next_path)
        elif file.is_directory(next_path):
            self.__current_path = next_path
            self.show()
