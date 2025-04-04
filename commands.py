import subprocess
import os

class Command:
    def run(self, command):
        """Execute a command."""
        try:
            subprocess.run(command.split(), text=True)
        except Exception as e:
            print(f"Error: {e}")
        
    def get_output(self, command):
        """Verify and return the output of a command"""
        try:
            return subprocess.check_output(command.split(), text=True).splitlines()
        except Exception as e:
            print(f"Error: {e}")

class GitCommand(Command):
    def __init__(self, repo_path="."):
        self.repo_path = repo_path
    
    def get_changes(self):
        return self.get_output("git status -s -u")

    def get_commits(self):
        return self.get_output("git log --oneline --all")

    def get_commits_hashes_only(self):
        return [c[:7] for c in self.get_commits()]

    def get_changes_names_only(self):
        return [fname[3:] for fname in self.get_changes()]

    def get_staged_changes(self):
        return self.get_output("git diff --name-status --cached")

    def get_diff_options(self):
        return self.get_output("git diff --name-only")

    def push_changes(self):
        self.run("git push")

    def pull_changes(self):
        self.run("git pull")

    def stage_all_changes(self):
        self.run("git add -A")
        self.show_changes()

    def unstage_all_changes(self):
        self.run("git restore --staged .")
        self.show_changes()

    def stage_interactive(self):
        self.run("git add -i")

    def commit_changes(self, message):
        self.run("git commit -m f'{message}'") 

    def checkout_patch(self):
        self.run("git checkout -p")

    def clean_interactive(self):
        self.run("git clean -i -d")
    
    def reset(self, type, commit):
        self.run(f"git reset --{type} {commit}")
    
    def show_changes(self):
        print("\n[Changes]")
        self.run("git status -s -u")
    
    def show_commits(self):
        self.run("git log --oneline --all")

    def show_status(self):
        self.run("git fetch")
        self.run("git status")
           
    def show_log(self):
        self.run("git log --oneline --all --decorate")
        
    def show_diff_for_file(self, file):
        self.run(f"git diff {file}")


class AppCommand(Command):
    # TODO create custom CLI browser, maybe a menu similar to the Log() screen
    def open_browser(self, browser):
        self.run(browser)
        
    def open_editor(self, editor, fpath):
        self.run(f"{editor} {fpath}")

    # TODO maybe use this later in the custom file browser
    def view_file(self, fpath):
        """View a file in readonly mode"""
        self.run(f"less {fpath}")

    # TODO create custom browser instead
    # def open_system_browser():
    #     # browser = get_system_browser()
    #     if utils.get_platform() == "Unix":
    #         return
    #         # Unix lacks a default/standard file manager, while Windows lacks a standard TTY editor (unless you want to use 'copy con'). Pros and cons. You can't win them all...
    #     elif utils.get_platform() == "Windows":
    #         # TODO add default Window browser
    #         # if get_platform() == "Windows":
    #         #     then open File Explorer
    #         print(f"\nWindows system browser coming soon.")
    # def open_system_editor(self, fpath):
    #     editor = get_system_editor()
    #     if get_platform() == "Unix":
    #         print(f"\nWarning: No config file to read editor from. Opening default editor '{editor}'...")
    #         if editor:
    #             self.run(f"{editor} {fpath}")
    #         else:
    #             print(f"\nCould not retrieve default editor.")
    #             return
    #     elif get_platform() == "Windows":
    #         print(f"\nWindows system editor function coming soon.")
    #         # TODO add default Windows editor
    #         # open Notepad or maybe search for nano and route there            
