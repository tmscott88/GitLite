"""Contains the interactive menus"""

import os
import sys
import functools
from shutil import which

import app_utils as app
import file_utils
from config import AppConfig
from commands import AppCommand, GitCommand
from menu import Menu
import prompts
from pickers import Browser, Picker

app_cmd = AppCommand()
git_cmd = GitCommand()
app_cfg = AppConfig()

def main_menu():
    """The main menu of GitWriting"""
    menu = Menu("Main Menu")
    menu.add_option(1, "File", file_menu)
    menu.add_option(2, "Source Control", git_menu)
    menu.add_option(3, "Settings", settings_menu)
    menu.add_option(4, "Help", help_menu)
    menu.add_option(5, "About GitWriting", functools.partial(app.show_splash, verbose=False))
    menu.add_option(6, "Quit", sys.exit)
    menu.show()

def file_menu():
    """The file management menu. "New File" => config "editor", "Open..." => config "browser"""
    menu = Menu("File")
    menu.add_option(1, "Back to Main Menu", main_menu)
    menu.add_option(2, "New File", __open_new_file)
    menu.add_option(3, "Open...", functools.partial(__open_app, "browser"))
    menu.add_option(4, "Open Recent", recent_files_menu)
    if app_cfg.is_daily_notes_enabled():
        menu.add_option(5, "Open Daily Note", __open_daily_note)
    if not git_cmd.is_inside_git_repo():
        menu.show()
    else:
        git_cmd.show_changes()
        menu.show(post_action=git_cmd.show_changes)

def git_menu():
    """The source control menu. Disabled when the working directory is not within a Git repo."""
    if not git_cmd.is_inside_git_repo():
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
        menu.add_option(0, "Revert...", __git_revert_menu)
        git_cmd.show_stashes_and_changes()
        menu.show(post_action=git_cmd.show_stashes_and_changes)

def __git_revert_menu():
    if not git_cmd.is_inside_git_repo():
        app.print_warning("Source control is disabled.")
    else:
        menu = Menu("Revert")
        menu.add_option(1, "Back to Git Menu", git_menu)
        menu.add_option(2, "Git Checkout (Tracked)", git_cmd.checkout_patch)
        menu.add_option(3, "Git Clean (Untracked)", git_cmd.clean_interactive)
        menu.add_option(4, "Reset to Commit", __commit_picker)
        git_cmd.show_stashes_and_changes()
        menu.show(post_action=git_cmd.show_stashes_and_changes)

def __commit_picker():
    """Opens a Curses picker menu to select one commit from the Git repo's history."""
    picker = Picker(
        title="[Commits]",
        populator=git_cmd.get_commits,
        total_entries=git_cmd.get_total_commits())
    picker.show_paginated()
    commit = picker.current_option
    if commit:
        reset_menu(commit[:7])

def __working_directory_picker():
    """Opens a Curses picker menu to select the working directory folder."""
    browser = Browser(os.getcwd())
    browser.select_directory()
    path = browser.current_path
    if path:
        print(f"Selected path {path}")
        if not git_cmd.is_inside_git_repo():
            app.print_error(f"Selected directory {path} is not a valid git repo.")
        else:
            app.change_working_directory(path)
            app_cfg.set_default_working_directory(path)

def recent_files_menu():
    """Gives different options for how to view "recent" files."""
    menu = Menu("Open Recent")
    menu.add_option(1, "Back to File Menu", file_menu)
    menu.add_option(2, "By Last Modified Date", functools.partial(__recent_file_picker, title="[Open Recent]", recents_filter="modified"))
    if git_cmd.is_inside_git_repo():
        menu.add_option(3, "By Git Index", functools.partial(__recent_file_picker, title="[Changes]", recents_filter="git_status"))
    menu.show()

def __recent_file_picker(recents_filter="modified", title="[Picker]"):
    """Opens a Curses picker menu to select a recently modified file."""
    match(recents_filter):
        case "git_status":
            if not git_cmd.is_inside_git_repo():
                app.print_warning("Cannot view recent files by git status. Not inside a git repo.")
            else:
                picker = Picker(title=title, populator=functools.partial(git_cmd.get_changes, names_only=True))
        case "modified":
            picker = Picker(title=title, populator=functools.partial(file_utils.get_all_files_by_modified_date, os.getcwd(), include_hidden=False))
        case _:
            picker = Picker(title=title, populator=functools.partial(file_utils.get_all_files_by_modified_date, os.getcwd(), include_hidden=False))
    picker.show()

def diff_menu():
    """Shows a list of tracked files to view each individual diff."""
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
    """Shows a list of tracked files. Allows for quick or interactive stage/unstage."""
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
    """Shows a list of stash operations: Create, Apply, Pop, Drop"""
    if not git_cmd.get_changes() and not git_cmd.get_stashes():
        app.print_warning("No changes or stashes available.")
        return
    menu = Menu("Stash")
    menu.add_option(1, "Back to Git Menu", git_menu)
    menu.add_option(2, "Create Stash", create_stash_menu)
    menu.add_option(3, "Apply Stash", functools.partial(__select_stash_menu, "apply"))
    menu.add_option(4, "Pop Stash", functools.partial(__select_stash_menu, "pop"))
    menu.add_option(5, "Drop Stash", functools.partial(__select_stash_menu, "drop"))
    git_cmd.show_stashes_and_changes()
    menu.show()

def __select_stash_menu(operation):
    """Shows a list of stashes in the local history. Proceeds with the stash operation."""
    if operation in ("apply", "pop") and git_cmd.get_changes():
        app.print_warning("Cannot safely apply a stash. Please commit, stash, or clean your changes first.")
        return
    menu = Menu("Select a Stash")
    options = git_cmd.get_stashes(names_only=True)
    if not options:
        app.print_warning("No stashes available in this repo.")
        return
    menu.add_option(1, "Back to Stash Menu", stash_menu)
    i = 2
    for opt in options:
        menu.add_option(i, opt, functools.partial(__confirm_existing_stash_operation, operation, opt))
        i = i + 1
    menu.show()

def create_stash_menu():
    """Stash all (including untracked changes), or stash staged changes only."""
    if not git_cmd.get_changes():
        app.print_warning("No changes available to stash.")
        return
    menu = Menu("Create Stash")
    menu.add_option(1, "Back to Stash Menu", stash_menu)
    menu.add_option(2, "Stash All",
        functools.partial(prompts.prompt_stash_message, include_untracked=True))
    menu.add_option(3, "Stash Staged Only",
        functools.partial(prompts.prompt_stash_message, include_untracked=False))
    git_cmd.show_changes()
    menu.show(post_action=stash_menu)

def __confirm_existing_stash_operation(operation, stash):
    """Shows options to apply, pop, or drop the selected stash."""
    if not git_cmd.get_stashes():
        app.print_warning("No stashes available in this repo.")
        return
    match(operation):
        case "apply":
            app.print_warning(f"This will apply stash '{stash}' and preserve it in the worktree.")
        case "pop":
            app.print_warning(f"This will apply stash '{stash}' and remove it from the worktree.")
        case "drop":
            app.print_warning(f"This will permanently remove stash '{stash}' from the worktree.")
        case _:
            app.print_error(f"Stash operation {operation} is invalid.")
            return
    menu = Menu(f"{operation.upper()} stash '{stash}'?")
    menu.add_option(1, "Yes", functools.partial(git_cmd.existing_stash_operation, operation, stash))
    menu.add_option(2, "No", stash_menu)
    menu.show(post_action=stash_menu)

def reset_menu(commit):
    """Shows options to soft, mixed, or hard reset to the selected commit."""
    menu = Menu(f"Selected Commit: {commit}")
    menu.add_option(1, "Back to Git Menu", git_menu)
    menu.add_option(2, "Back to Commit Picker", __commit_picker)
    menu.add_option(3, "Review Commit", functools.partial(git_cmd.show_commit_details, commit))
    menu.add_option(4, "Mixed Reset", functools.partial(__confirm_reset, "mixed", commit))
    menu.add_option(5, "Soft Reset", functools.partial(__confirm_reset, "soft", commit))
    menu.add_option(6, "Hard Reset", functools.partial(__confirm_reset, "hard", commit))
    menu.show()

def __confirm_reset(reset_type, commit):
    """Shows Yes/No menu whether to reset to the selected commit."""
    menu = Menu(f"{reset_type.upper()} reset to commit {commit} ?")
    menu.add_option(1, "Yes", functools.partial(git_cmd.reset, reset_type, commit))
    menu.add_option(2, "No", functools.partial(reset_menu, commit))
    menu.show(post_action=git_menu)

def __confirm_factory_reset():
    """Shows Yes/No menu whether to remove the GitWriting config file."""
    app.print_warning("Factory reset GitWriting?")
    menu = Menu("Factory Reset")
    menu.add_option(1, "Yes", app_cfg.factory_reset)
    menu.add_option(2, "No", settings_menu)
    menu.show()

def settings_menu():
    """Shows the app settings menu, each of which modify the GitWriting config file."""
    menu = Menu("Settings")
    menu.add_option(1, "Back to Main Menu", main_menu)
    menu.add_option(2, "Default Apps", __default_apps_menu)
    menu.add_option(3, "Browser Settings", __browser_settings_menu)
    menu.add_option(4, "Daily Notes", __daily_notes_menu)
    menu.add_option(5, "Working Directory", prompts.prompt_select_repo)
    # TODO convert the Flags settings to a settings picker?
    menu.add_option(0, "\u26A0 Factory Reset \u26A0",
        __confirm_factory_reset)
    app_cfg.read()
    app_cfg.show()
    menu.show(post_action=app_cfg.show)

def __default_apps_menu():
    """Shows the sub-menu to set default apps settings"""
    menu = Menu("Default Apps")
    menu.add_option(1, "Back to Settings",
        settings_menu)
    menu.add_option(2, "Browser",
        functools.partial(prompts.set_app, "browser"))
    menu.add_option(3, "Editor",
        functools.partial(prompts.set_app, "editor"))
    menu.show(post_action=app_cfg.show)

def __browser_settings_menu():
    """Shows the sub-menu to set the internal browser settings"""
    menu = Menu("Browser Settings")
    menu.add_option(1, "Back to Settings",
        settings_menu)
    menu.add_option(2, "Enable Hidden Files (Browser)",
        functools.partial(__set_browser_hidden_files_status, "on"))
    menu.add_option(3, "Disable Hidden Files (Browser)",
        functools.partial(__set_browser_hidden_files_status, "off"))
    menu.add_option(4, "Enable Read-Only Mode (Browser)",
        functools.partial(__set_browser_readonly_mode_status, "on"))
    menu.add_option(5, "Disable Read-Only Mode (Browser)",
        functools.partial(__set_browser_readonly_mode_status, "off"))
    menu.show(post_action=app_cfg.show)

def __daily_notes_menu():
    """Shows the sub-menu to set daily notes settings"""
    menu = Menu("Daily Notes")
    menu.add_option(1, "Back to Settings",
        settings_menu)
    menu.add_option(2, "Enable Daily Notes",
        functools.partial(__set_daily_notes_status, "on"))
    menu.add_option(3, "Disable Daily Notes",
        functools.partial(__set_daily_notes_status, "off"))
    menu.add_option(4, "Daily Notes Path",
        prompts.set_daily_notes_path)

    menu.show(post_action=app_cfg.show)
def help_menu():
    """Shows the app help menu."""
    menu = Menu("Help")
    menu.add_option(1, "Back to Main Menu", main_menu)
    menu.add_option(2, "View README", app_cmd.show_readme)
    menu.add_option(3, "View Changelog", app_cmd.show_changelog)
    menu.add_option(4, "View Config Example", app_cfg.show_config_template)
    menu.add_option(5, "View App Dependencies", app_cmd.show_requirements)
    menu.show()

def __open_app(app_type, fpath=""):
    """Open an app with specified app type.
        If the GitWriting config isn't found, fallback to the system default app.
        """
    valid_app_types = ["browser", "editor"]
    if app_type not in valid_app_types:
        app.print_error(f"Unknown app type {app_type}. Valid app types are {valid_app_types}.")
        return
    app_name = app_cfg.get_app(app_type)
    if app_type == "browser" and app_name == "default":
        __open_default_browser()
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
        __open_system_app(app_type, fpath)

def __open_system_app(app_type, fpath=""):
    """Opens the default app for a specified app (if supported)."""
    app_name = app.get_system_app(app_type)
    match app_type:
        case "editor":
            app_cmd.open_editor(app_name, fpath)
        case "browser":
            __open_default_browser()
        case _:
            app.print_error(f"App type '{app_type}' is not supported by GitWriting.")

# def default_browser(select_folder_mode=False):
def __open_default_browser():
    """As of 0.8.6, this will open the integrated file browser instead of explorer.exe."""
    browser = Browser(os.getcwd())
    browser.show()

def __open_new_file():
    """Prompt new file. If the file already exists, opens the file in the defined editor."""
    path = input("Enter new file name (or pass empty name to cancel): ")
    if not path:
        app.print_error("Canceled operation.")
    else:
        if file_utils.is_file(path):
            __open_app("editor", path)
        else:
            file_utils.create_new_file(path)
            # Only open editor if file was created properly from the previous step
            if file_utils.is_file(path):
                __open_app("editor", path)
            else:
                app.print_error(f"Failed to create or find file '{path}'")

def __open_daily_note():
    """If Daily Notes features is enabled, creates and/or opens today's note at a generated path."""
    if not app_cfg.is_daily_notes_enabled():
        print("\nDaily Notes disabled. See Main Menu -> Settings to enable this feature.")
    else:
        fpath = app_cfg.get_today_note_path()
        file_utils.create_new_file(fpath)
        __open_app("editor", fpath)

def __set_daily_notes_status(new_status):
    """Helper function to enable or disable the Daily Notes feature."""
    if new_status in ("on","off"):
        app_cfg.set_daily_notes_status(new_status)
    else:
        app.print_error(f"Unexpected status '{new_status}'. Status must be 'on' or 'off'.")

def __set_browser_hidden_files_status(new_status):
    """Helper function to enable or disable hidden files visibility in the default browser."""
    if new_status in ("on", "off"):
        app_cfg.set_browser_hidden_files(new_status)
    else:
        app.print_error(f"Unexpected status '{new_status}'. Status must be 'on' or 'off'.")

def __set_browser_readonly_mode_status(new_status):
    """Helper function to enable or disable read-only mode in the default browser."""
    if new_status in ("on", "off"):
        app_cfg.set_browser_readonly_mode(new_status)
    else:
        app.print_error(f"Unexpected status '{new_status}'. Status must be 'on' or 'off'.")
