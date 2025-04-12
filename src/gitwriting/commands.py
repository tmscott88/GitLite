"""Contains subprocess functions and classes to hold Git & App-specific commands"""
import subprocess
import app_utils as app

class Command:
    """Base class for the commands module.
        Simply used to run commands or get command output using subprocess"""
    def __init__(self, quiet=True):
        self.quiet = quiet

    def run(self, command, has_input_message=False, is_shell=False):
        """Execute a command. If has_input_message is True,
            you MUST pass the command as an array with explicit arguments
            (e.g. ['git', 'commit', '-m', f"{message}"])
            """
        try:
            if has_input_message:
                subprocess.run(command, text=True, check=True, shell=is_shell)
            else:
                subprocess.run(command.split(), text=True, check=True, shell=is_shell)
        except subprocess.CalledProcessError as e:
            if not self.quiet:
                app.print_error(f"Failed to run command '{command}: {e}'")

    def get_output(self, command):
        """Verify and return the array output of a command."""
        try:
            return subprocess.check_output(
                command.split(),
                text=True,
                stderr=subprocess.DEVNULL).splitlines()
        except subprocess.CalledProcessError as e:
            if not self.quiet:
                app.print_error(f"Failed to get output from command '{command}: {e}'")
            raise

class GitCommand(Command):
    """Runs git commands"""
    def get_repo_root(self):
        """Returns the root of the Git repo"""
        return self.get_output("git rev-parse --show-toplevel")[0]

    def get_changes(self, names_only=False):
        """Returns the Git repo's uncommitted changes (full or names only)"""
        changes = self.get_output("git status -s -u")
        if changes and names_only:
            return [fname[3:] for fname in self.get_changes()]
        return changes

    def get_commits(self, hashes_only=False, index=0, limit=-1):
        """Returns the Git repo's commit history (full or hashes only)"""
        commits = self.get_output(f"git log --oneline HEAD~{index} -n {limit}")
        if commits and hashes_only:
            return [c[:7] for c in commits]
        return commits

    def get_total_commits(self):
        """Returns the total number of commits in the repo's history (not counting merges)"""
        return self.get_output("git rev-list HEAD --count --no-merges")[0]

    def get_stashes(self, names_only=False):
        """Returns the Git repo's local stashes (full or names only)"""
        stashes = self.get_output("git stash list")
        if stashes and names_only:
            return [name.split(":")[0] for name in stashes]
        return stashes

    def get_staged_changes(self):
        """Returns the Git repo's local staged changes"""
        return self.get_output("git diff --name-status --cached")

    def get_diff_options(self):
        """Returns the Git repo's local changes, compared to their previous commit if available"""
        return self.get_output("git diff --name-only")

    def push_changes(self):
        """Pushes all pending changes from the local repo to the Git remote"""
        self.run("git push")

    def pull_changes(self):
        """Fetches all pending changes from the Git remote, updat es the local repo"""
        self.run("git pull")

    def stage_all_changes(self):
        """Stages all local changes (including untracked)"""
        self.run("git add -A")
        self.show_changes()

    def unstage_all_changes(self):
        """Unstages all local changes (including untracked)"""
        self.run("git restore --staged .")
        self.show_changes()

    def stage_interactive(self):
        """Opens Git's interactive staging menu"""
        self.run("git add -i")
        self.show_changes()

    def commit_changes(self, message):
        """Commits all staged local changes"""
        self.run(['git', 'commit', '-m', f"{message}"], has_input_message=True)

    def stash_all_changes(self, message):
        """Stashes all local changes"""
        self.run(['git', 'stash', 'push', '-u', '-m', f"{message}"], has_input_message=True)

    def stash_staged_changes(self, message):
        """Stashes all staged local changes"""
        self.run(['git', 'stash', 'push', '--staged', '-m', f"{message}"], has_input_message=True)

    def existing_stash_operation(self, operation, stash):
        """Executes the Git stash operation on the specified stash (apply, pop, or drop)"""
        match(operation):
            case "apply":
                self.run(f"git stash apply {stash}")
            case "pop":
                self.run(f"git stash pop {stash}")
            case "drop":
                self.run(f"git stash drop {stash}")

    def checkout_patch(self):
        """Opens Git's interactive checkout menu"""
        self.run("git checkout -p")

    def clean_interactive(self):
        """Opens Git's interactive cleaning menu"""
        self.run("git clean -i -d")

    def reset(self, reset_type, commit):
        """Opens Git's interactive cleaning menu"""
        self.run(f"git reset --{reset_type} {commit}")

    def show_changes(self):
        """Displays all local changes in a compact list"""
        if self.get_changes():
            print("\n[Changes]")
            self.run("git status -s -u")

    def show_stashes(self):
        """Displays all local stashes in a compact list"""
        if self.get_stashes():
            print("\n[Stashes]")
            self.run("git stash list")

    def show_status(self):
        """Fetches and displays the full Git status"""
        self.run("git fetch")
        self.run("git status")

    def show_log(self):
        """Displays the commit history in a compact list"""
        self.run("git log --oneline --graph --name-status")

    def show_diff_for_file(self, file):
        """Shows the Git diff for the specified file"""
        self.run(f"git diff {file}")

    def show_commit_details(self, commit_hash):
        """Shows more details for the specified Git commit"""
        self.run(f"git show {commit_hash}")

    def show_stashes_and_changes(self):
        """Shows local Git stashes and changes"""
        self.show_stashes()
        self.show_changes()

    def is_inside_git_repo(self):
        """If the working directory is inside a git repo, changes working directory to root of the git repo"""
        try:
            path = self.get_repo_root()
            if "fatal" in path:
                raise subprocess.CalledProcessError
            return True
        except subprocess.CalledProcessError:
            return False


class AppCommand(Command):
    """Command class for app-specific commands"""
    git_cmd = GitCommand()
    def open_browser(self, browser):
        """Opens the specified browser"""
        self.run(browser)

    def open_editor(self, editor, fpath):
        """Opens the specified editor."""
        self.run(f"{editor} {fpath}")

    def view_file(self, fpath):
        """Opens the specified file in read-only mode"""
        if app.platform_is_windows():
            self.run(f"more {fpath}", is_shell=True)
        else:
            self.run(f"less {fpath}")

    def show_changelog(self):
        """Fetches the app's changelog path"""
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
