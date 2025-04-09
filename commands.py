import os
import subprocess
import app_utils as app

class Command:
    """Base class for the commands module. Simply used to run commands or get command output using subprocess"""
    def __init__(self, quiet=False):
        self.quiet = quiet

    def run(self, command, has_input_message=False):
        """Execute a command. If has_input_message is True, you MUST pass the command as an array with explicit arguments (e.g. ['git', 'commit', '-m', f"{message}"])"""
        try:
            if has_input_message:
                subprocess.run(command, text=True, check=True)
            else:
                subprocess.run(command.split(), text=True, check=True)
        except subprocess.CalledProcessError:
            app.print_error(f"Failed to run command '{command}'")
        
    def run_shell_mode(self, command):
        """Execute a command with shell enabled. DO NOT CALL THIS UNLESS NECESSARY! IF THE COMMAND WORKS FINE WITH 'Command.run()', USE THAT INSTEAD!"""
        try:
            subprocess.run(command.split(), text=True, shell=True, check=True)
        except subprocess.CalledProcessError:
            app.print_error(f"Failed to run shell command '{command}'")

    def get_output(self, command):
        """Verify and return the array output of a command."""
        try:
            if not self.quiet:
                return subprocess.check_output(command.split(), text=True).splitlines()
            return subprocess.check_output(command.split(), text=True, stderr=subprocess.DEVNULL).splitlines()
        except subprocess.CalledProcessError:
            if not self.quiet:
                app.print_error(f"Failed to get output from command '{command}'")
            raise

class GitCommand(Command):
    """Place Git commands """
    def __init__(self, quiet=False):
        super().__init__(quiet)
        self.quiet = quiet

    def get_repo_root(self):
        return self.get_output("git rev-parse --show-toplevel")[0]

    def get_changes(self):
        return self.get_output("git status -s -u")

    def get_commits(self):
        return self.get_output("git log --oneline --all")

    def get_stashes(self):
        return self.get_output("git stash list")

    def get_stashes_names_only(self):
        return [name.split(":")[0] for name in self.get_stashes()]

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
        self.run(['git', 'commit', '-m', f"{message}"], has_input_message=True) 

    def stash_all_changes(self, message):
        self.run(['git', 'stash', 'push', '-u', '-m', f"{message}"], has_input_message=True)

    def stash_staged_changes(self, message):
        self.run(['git', 'stash', 'push', '--staged', '-m', f"{message}"], has_input_message=True)

    def existing_stash_operation(self, operation, stash):
        match(operation):
            case "apply":
                self.run(f"git stash apply {stash}")
            case "pop":
                self.run(f"git stash pop {stash}")
            case "drop":
                self.run(f"git stash drop {stash}")

    def checkout_patch(self):
        self.run("git checkout -p")

    def clean_interactive(self):
        self.run("git clean -i -d")
    
    def reset(self, reset_type, commit):
        self.run(f"git reset --{reset_type} {commit}")
    
    def show_changes(self):
        if self.get_changes():
            print("\n[Changes]")
            self.run("git status -s -u")

    def show_stashes(self):
        if self.get_stashes():
            print("\n[Stashes]")
            self.run("git stash list")
        
    def show_commits(self):
        self.run("git log --oneline --all")

    def show_status(self):
        self.run("git fetch")
        self.run("git status")
           
    def show_log(self):
        self.run("git log --oneline --all --decorate")
        
    def show_diff_for_file(self, file):
        self.run(f"git diff {file}")

    def show_stashes_and_changes(self):
        self.show_stashes()
        self.show_changes()

    def is_working_dir_at_git_repo_root(self):
        """Check if the working directory at the top level of a git repo"""
        try:
            return bool(self.get_repo_root() == os.getcwd())
        except subprocess.CalledProcessError:   
            return False

class AppCommand(Command):
    def __init__(self, quiet=False):
        super().__init__(quiet)
        self.quiet = quiet

    def open_browser(self, browser):
        app.print_info(f"Opening browser '{browser}'...")
        self.run(browser)
    
    def open_editor(self, editor, fpath, quiet=False):
        if not quiet:
            app.print_info(f"Opening '{fpath}' in '{editor}'...")
            self.run(f"{editor} {fpath}")

    def view_file(self, fpath):
        """View a file in readonly mode"""
        if not self.quiet:
            app.print_info(f"Opening '{fpath}' in readonly mode...")
        if app.platform_is_windows():
            self.run_shell_mode(f"more {fpath}")
        else:
            self.run(f"less {fpath}")     

    def show_changelog(self):
        """Fetches the app's CHANGELOG path"""
        path = app.get_resource_path("CHANGELOG.md")
        if path:
            self.view_file(path)

    def show_readme(self):
        """Fetches the app's README path"""
        path = app.get_resource_path("README.md")
        if path:
            self.view_file(path)

    def show_requirements(self):
        """Fetches the app's Python requirements (dependencies) path"""
        path = app.get_resource_path("requirements.txt")
        if path:
            self.view_file(path)
