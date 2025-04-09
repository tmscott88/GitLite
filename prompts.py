import sys
from shutil import which

import app_utils as app
import file_utils
from config import AppConfig
from commands import GitCommand

app_cfg = AppConfig(app.get_expected_config_path())
git_cmd = GitCommand(quiet=True)

def prompt_create_config(is_full_launch=True):
    # When running without the config launch argument
    if is_full_launch:
        print("\nWelcome to GitWriting!")
        print("\nLet's get you set up and writing!")
        app.print_info("First, let's generate a configuration file_utils. This file contains some helpful app settings for GitWriting to use between sessions.")
        app.print_info(f"The config file 'gitwriting.ini' will be generated at: {app.get_runtime_directory(convert=False)}")
        if not app.prompt_continue():
            print("\nBye.")
            sys.exit()

    app.print_info("Generating config file...")
    app_cfg.generate()
    app_cfg.show()
    app.print_question("Please enter your preferred file editor. (Or press enter to use the default editor)")
    set_app("editor")
    app.print_question("Please enter your preferred file browser. (Or press enter to use the default file browser)")
    set_app("browser")
    app.print_question("Enable daily notes? This feature serves as a shortcut to create a new note each day, neatly organized by date.")
    if app.prompt_continue():
        app_cfg.set_daily_notes_status("on")
    else:
        app_cfg.set_daily_notes_status("off")
    if app_cfg.is_daily_notes_enabled():
        app.print_question("Since you enabled daily notes, you may set the default path for daily notes now. (Or press enter to use the default path)")
        set_daily_notes_path()
    else:
        app.print_info("Skipping daily notes path selection since it is disabled...")
    app_cfg.show()
    app.print_success("That's all!")
    app.print_info("These settings can be changed anytime under [Main Menu -> Settings].")
    app.print_info("Get help anytime at these locations:", new_line=False)
    app.print_info("[Main Menu -> Help] or https://github.com/tmscott88/GitWriting/blob/main/README.md", new_line=False)
    app.print_info("[Main Menu -> About GitWriting] for more technical information.", new_line=False)
    if is_full_launch:
        if not app.prompt_continue():
            print("\nBye.")
            sys.exit()

def prompt_commit():
    if not git_cmd.get_staged_changes():
        app.print_warning("No staged changes to commit.")
    else:
        message = input("Enter commit message (or pass empty message to cancel): ")
        if message:
            git_cmd.commit_changes(message)
        else:
            print()
            app.print_error("Canceled commit.")

def prompt_stash_message(include_untracked=False):
    message = input("Enter stash message (or pass empty message to cancel): ")
    if message:
        if include_untracked:
            git_cmd.stash_all_changes(message)
        else:
            git_cmd.stash_staged_changes(message)
    else:
        print()
        app.print_error("Canceled stash.")

def set_daily_notes_path():
    new_path = input("Set new Daily Notes path (or pass empty path to cancel): ")
    if new_path:
        file_utils.create_new_directory(new_path)
        app_cfg.set_daily_notes_path(new_path)
    else:
        print()
        app.print_error(f"Canceled. Keep current path: '{app_cfg.get_daily_notes_root_path()}'")

def set_app(app_type):
    while True:
        new_app = input(f"Set new {app_type} app: ")
        if not new_app:
            print()
            app.print_error(f"Canceled. Keep current {app_type} app: {app_cfg.get_app(app_type)}")
            break
        if new_app == "default":
            app_cfg.set_app(app_type, new_app)
            break
        try:
            if (which(new_app)) is None:
                raise FileNotFoundError
            app_cfg.set_app(app_type, new_app)
            break
        except FileNotFoundError:
            app.show_app_not_found_error(new_app)