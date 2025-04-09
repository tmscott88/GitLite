import sys
import functools
from shutil import which

import app_utils as app
import file_utils
from config import AppConfig
from commands import AppCommand, GitCommand
from menu import Menu
import prompts
from picker import Browser, CommitPicker

app_cmd = AppCommand(quiet=True)
git_cmd = GitCommand(quiet=True)
app_cfg = AppConfig(app.get_expected_config_path())

def main_menu():
    """The main menu of GitWriting. Note: Source Control is disabled when the working directory is outside of a git repository.""" 
    menu = Menu("Main Menu")
    menu.add_option(1, "File", file_menu)
    menu.add_option(2, "Source Control", git_menu)
    menu.add_option(3, "Settings", settings_menu)
    menu.add_option(4, "Help", help_menu)
    menu.add_option(5, "About GitWriting", app.show_about)
    menu.add_option(6, "Quit", sys.exit)
    menu.show()

def file_menu():
    """The file management menu. "New File" uses the config's "editor" key, while "Open..." uses the config's "browser" key."""
    menu = Menu("File")
    menu.add_option(1, "Back to Main Menu", main_menu)
    menu.add_option(2, "New File", open_new_file)
    menu.add_option(3, "Open...", functools.partial(open_app, "browser"))
    menu.add_option(4, "Open Recent", recents_menu)
    if app_cfg.is_daily_notes_enabled():
        menu.add_option(5, "Open Daily Note", open_daily_note)
    if not git_cmd.is_working_dir_at_git_repo_root():
        menu.show()
    else:
        git_cmd.show_changes()
        menu.show(post_action=git_cmd.show_changes)

def git_menu():
    """The source control menu. Disabled when the working directory is not within a Git repository."""
    if not git_cmd.is_working_dir_at_git_repo_root():
        app.print_warning("Source control is disabled.")
    else:
        menu = Menu("Source Control")
        menu.add_option(1, "Back to Main Menu", main_menu)
        menu.add_option(2, "Git Status", git_cmd.show_status)
        menu.add_option(3, "Git Log", git_cmd.show_log)
        menu.add_option(4, "Git Diff", diff_menu)
        menu.add_option(5, "Git Pull", git_cmd.pull_changes)
        menu.add_option(6, "Git Push", git_cmd.push_changes)
        menu.add_option(7, "Git Stage", stage_menu)
        menu.add_option(8, "Commit Changes", prompts.prompt_commit)
        menu.add_option(9, "Stash Changes", stash_menu)
        menu.add_option(10, "Git Checkout (Tracked)", git_cmd.checkout_patch)
        menu.add_option(11, "Git Clean (Untracked)", git_cmd.clean_interactive)
        menu.add_option(12, "Reset to Commit", commit_picker)
        git_cmd.show_stashes_and_changes()
        menu.show(post_action=git_cmd.show_stashes_and_changes)

def commit_picker():
    """Opens a Curses picker menu to select one commit from the Git repo's history."""
    picker = CommitPicker()
    commit = picker.show()
    if commit:
        reset_menu(commit[:7])

def recents_menu():
    """Shows a list of files from Git Index to open in the editor."""
    # TODO: make switch flag in this menu set to "Last Modified" or "In Working Tree", reload menu based on toggle
    #   Also create new config setting
    if not git_cmd.is_working_dir_at_git_repo_root():
        app.print_warning("Recents menu is disabled.")
    else:
        menu = Menu("Open Recent")
        options = git_cmd.get_changes_names_only()
        if not options:
            app.print_warning("No recent files to open.")
        else:
            menu.add_option(1, "Back to File Menu", file_menu)
            i = 2
            for opt in options:
                menu.add_option(i, opt, functools.partial(open_app, "editor", opt))
                i = i + 1
            menu.show()

def diff_menu():
    """Shows a list of tracked files from Git Index to view each individual diff."""
    menu = Menu("View Diff")
    options = git_cmd.get_diff_options()
    if not options:
        app.print_warning("No tracked changes to analyze.")
    else:
        menu.add_option(1, "Back to Git Menu", git_menu)
        i = 2
        for opt in options:
            menu.add_option(i, opt, functools.partial(git_cmd.show_diff_for_file, opt))
            i = i + 1
        menu.show()

def stage_menu():
    """Shows a list of tracked files from Git Index. Allows for quick or interactive stage/unstage."""
    if not git_cmd.get_changes():
        app.print_warning("No changes to stage or unstage.")
    else:
        menu = Menu("Stage")
        menu.add_option(1, "Back to Git Menu", git_menu)
        menu.add_option(2, "Stage All", git_cmd.stage_all_changes)
        menu.add_option(3, "Unstage All", git_cmd.unstage_all_changes)
        menu.add_option(4, "Interactive Stage", git_cmd.stage_interactive)
        git_cmd.show_changes()
        menu.show()

def stash_menu():
    """Shows a list of stash operations to continue with. Supported operations: Create, Apply, Pop, Drop"""
    if not git_cmd.get_changes() and not git_cmd.get_stashes():
        app.print_warning("No changes or stashes available.")
        return
    menu = Menu("Stash")
    menu.add_option(1, "Back to Git Menu", git_menu)
    menu.add_option(2, "Create Stash", create_stash_menu)
    menu.add_option(3, "Apply Stash", functools.partial(select_stash_menu, "apply"))
    menu.add_option(4, "Pop Stash", functools.partial(select_stash_menu, "pop"))
    menu.add_option(5, "Drop Stash", functools.partial(select_stash_menu, "drop"))
    git_cmd.show_stashes_and_changes()
    menu.show()

def select_stash_menu(operation):
    """Shows a list of stashes in the local history. Proceeds with the stash operation (Create/Apply/Pop/Drop) selected from stash_menu()."""
    menu = Menu("Select a Stash")
    options = git_cmd.get_stashes_names_only()
    if not options:
        app.print_warning("No stashes available in this repo.")
        return
    menu.add_option(1, "Back to Stash Menu", stash_menu)
    i = 2
    for opt in options:
        menu.add_option(i, opt, functools.partial(confirm_existing_stash_operation, operation, opt))
        i = i + 1
    menu.show()

def create_stash_menu():
    if not git_cmd.get_changes():
        app.print_warning("No changes available to stash.")
        return
    menu = Menu("Create Stash")
    menu.add_option(1, "Back to Stash Menu", stash_menu)
    menu.add_option(2, "Stash All", functools.partial(prompts.prompt_stash_message, include_untracked=True))
    menu.add_option(3, "Stash Staged Only", functools.partial(prompts.prompt_stash_message, include_untracked=False))
    git_cmd.show_changes()
    menu.show(post_action=select_stash_menu)

def confirm_existing_stash_operation(operation, stash):
    if not git_cmd.get_stashes():
        app.print_warning("No stashes available in this repo.")
        return
    match(operation):
        case "apply":
            app.print_warning("Note: This will apply the stored copy of the stash and preserve it in the local tree.")
        case "pop":
            app.print_warning("Note: This will apply the stored copy of the selected stash and remove it from the local tree.")
        case "drop":
            app.print_warning("Note: This will permanently remove the stored copy of the selected stash.")
        case _:
            app.print_error(f"Stash operation {operation} is invalid.")
            return
    menu = Menu(f"{operation.upper()} stash '{stash}'?")
    menu.add_option(1, "Yes", functools.partial(git_cmd.existing_stash_operation, operation, stash))
    menu.add_option(2, "No", stash_menu)
    menu.show(post_action=stash_menu)

def reset_menu(commit):
    menu = Menu(f"Selected Commit: {commit}")
    menu.add_option(1, "Back to Git Menu", git_menu)
    menu.add_option(2, "Back to Commit Picker", commit_picker)
    menu.add_option(3, "Mixed Reset", functools.partial(confirm_reset, "mixed", commit))
    menu.add_option(4, "Soft Reset", functools.partial(confirm_reset, "soft", commit))
    menu.add_option(5, "Hard Reset", functools.partial(confirm_reset, "hard", commit))
    menu.show()

def confirm_reset(reset_type, commit):
    menu = Menu(f"{reset_type.upper()} reset to commit {commit} ?")
    menu.add_option(1, "Yes", functools.partial(git_cmd.reset, reset_type, commit))
    menu.add_option(2, "No", functools.partial(reset_menu, commit))
    menu.show(post_action=git_menu)

def confirm_factory_reset():
    app.print_warning("Reset GitWriting back to default settings? THIS WILL ERASE THE EXISTING CONFIG FILE!")
    menu = Menu("Factory Reset")
    menu.add_option(1, "Yes", app_cfg.factory_reset)
    menu.add_option(2, "No", settings_menu)
    menu.show()

def settings_menu():
    menu = Menu("Settings")
    menu.add_option(1, "Back to Main Menu", main_menu)
    menu.add_option(2, "Set Browser", functools.partial(prompts.set_app, "browser"))
    menu.add_option(3, "Set Editor", functools.partial(prompts.set_app, "editor"))
    # TODO convert the Flags settings to a settings picker?
    menu.add_option(4, "Enable Daily Notes", functools.partial(set_daily_notes_status, "on"))
    menu.add_option(5, "Disable Daily Notes", functools.partial(set_daily_notes_status, "off"))
    menu.add_option(6, "Set Daily Notes Path", prompts.set_daily_notes_path)
    menu.add_option(7, "Enable Hidden Files (Browser)", functools.partial(set_browser_hidden_files_status, "on"))
    menu.add_option(8, "Disable Hidden Files (Browser)", functools.partial(set_browser_hidden_files_status, "off"))
    menu.add_option(9, "Enable Read-Only Mode (Browser)", functools.partial(set_browser_readonly_mode_status, "on"))
    menu.add_option(10, "Disable Read-Only Mode (Browser)", functools.partial(set_browser_readonly_mode_status, "off"))
    menu.add_option(11, "\u26A0 Factory Reset \u26A0", confirm_factory_reset)
    app_cfg.read()
    app_cfg.show()
    menu.show(post_action=app_cfg.show)

def help_menu():
    menu = Menu("Help")
    menu.add_option(1, "Back to Main Menu", main_menu)
    menu.add_option(2, "View README", app_cmd.show_readme)
    menu.add_option(3, "View Changelog", app_cmd.show_changelog)
    menu.add_option(4, "View Config Example", app_cfg.show_config_template)
    menu.add_option(5, "View App Dependencies", app_cmd.show_requirements)
    menu.show()

def open_app(app_type, fpath=""):
    # if config isn't there, fallback to the system default app
    if not app_cfg.is_in_current_dir():
        open_system_app(app_type, fpath)
        app.print_warning("Config file not found. Opening default system app...")
        return
    valid_app_types = ["browser", "editor"]
    if app_type not in valid_app_types:
        app.print_error(f"Unknown app type {app_type}. Valid app types are {valid_app_types}.")
        return
    app_name = app_cfg.get_app(app_type)
    if app_type == "browser" and app_name == "default":
        open_default_browser()
        return
    try:
        if (which(app_name)) is None:
            raise FileNotFoundError
        match(app_type):
            case "browser":
                app_cmd.open_browser(app_name)
            case "editor":
                app_cmd.open_editor(app_name, fpath)
    except FileNotFoundError:
        app.show_app_not_found_error(app_name)
        open_system_app(app_type, fpath)

def open_system_app(app_type, fpath=""):
    """As of 0.8.6, this will open the integrated file browser instead of explorer.exe."""
    app_name = app.get_system_app(app_type)
    match app_type:
        case "editor":
            app_cmd.open_editor(app_name, fpath)
        case "browser":
            open_default_browser()
        case _:
            app.print_error(f"App type '{app_type}' is not supported. Failed to retrieve default app for this type.")

# def default_browser(select_folder_mode=False):
def open_default_browser():
    browser = Browser(app.get_runtime_directory(convert=False))
    browser.show()
    # if select_folder_mode:
    #     browser.select_directory()
    #     path = browser.current_path
    #     if path:
    #         app.print_success(f"Selected directory '{path}'")
    #         app.
    # (path)
    #     else:
    #         app.print_error("Canceled directory selection.")
    # else:

def open_new_file():
    path = input("Enter new file name (or pass empty name to cancel): ")
    if not path:
        print()
        app.print_error("Canceled operation.")
    else:
        if file_utils.is_file(path):
            open_app("editor", path)
        else:
            file_utils.create_new_file(path)
            # Only open editor if file was created properly from the previous step
            if file_utils.is_file(path):
                open_app("editor", path)
            else:
                app.print_error(f"Failed to create or find file '{path}'")

def open_daily_note():
    if not app_cfg.is_daily_notes_enabled():
        print("\nDaily Notes disabled. See Main Menu -> Settings to enable this feature.")
    else:
        fpath = app_cfg.get_today_note_path()
        file_utils.create_new_file(fpath)
        open_app("editor", fpath)

def set_daily_notes_status(new_status):
    if new_status in ("on","off"):
        app_cfg.set_daily_notes_status(new_status)
    else:
        app.print_error(f"Unexpected status '{new_status}'. Status must be 'on' or 'off'.")

def set_browser_hidden_files_status(new_status):
    if new_status in ("on", "off"):
        app_cfg.set_browser_hidden_files(new_status)
    else:
        app.print_error(f"Unexpected status '{new_status}'. Status must be 'on' or 'off'.")

def set_browser_readonly_mode_status(new_status):
    if new_status in ("on", "off"):
        app_cfg.set_browser_readonly_mode(new_status)
    else:
        app.print_error(f"Unexpected status '{new_status}'. Status must be 'on' or 'off'.")