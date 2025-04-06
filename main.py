# Python Modules
import os
import sys
import functools
from shutil import which
# My Modules
import app_utils as app
import file_utils as file
from config import AppConfig
from commands import GitCommand, AppCommand
from menu import Menu

config = AppConfig()
git_cmd = GitCommand()
app_cmd = AppCommand()

def main():
    while len(sys.argv) > 1:
        handle_launch_args()
    # TODO testing macOS package not finding proper directories
    app.show_splash()
    if not app.is_valid_repo():
        app.print_error(f"Failed to detect a valid Git repo from the current folder.") 
        app.print_warning("Please place this executable in your Git repo's root directory.", new_line=False)
        app.prompt_exit()
    else:
        if not config.is_present():
            prompt_create_config()
        else:
            config.read()
        main_menu()

def prompt_create_config():
    print(f"\nWelcome to GitWriting!")
    print("\nLet's get you set up and writing!")
    app.print_info("First, you will need to generate a configuration file. This file contains key app settings for GitWriting to use between sessions.")
    if not app.prompt_continue():
        print("\nBye.")
        sys.exit()
    else:
        app.print_info("Generating config file...")
        config.generate()
        config.show()
        app.print_question("Please enter your preferred file editor. (Or press enter to use the default editor)")
        set_app("editor")
        app.print_question("Please enter your preferred file browser. (Or press enter to use the default file browser)")
        set_app("browser")
        # Once finished
        config.show()
        app.print_success("That's all!")
        app.print_info("These settings can be changed anytime under [Main Menu -> Settings].")
        app.print_info("Get help anytime at these locations:", new_line=False)
        app.print_info("[Main Menu -> Help] or https://github.com/tmscott88/GitWriting/blob/main/README.md", new_line=False)
        app.print_info("[Main Menu -> About GitWriting] for more technical information.", new_line=False)
        if not app.prompt_continue():
            print("\nBye.")
            sys.exit()

def handle_launch_args():
    options_desc = "[Options] \nHelp: [-h | --help | -H] \nVerify Config: [-c | --config | -C] \nVersion: [-v | --version | -V], \nView README: [-r | --readme | -R]"
    usage_desc = f"\n[Usage] \n./{os.path.basename(__file__)} [OPTION]\n"
    parser_desc = f"\nSettings are defined in '{config.name}'. See 'README.md' for a template config file."

    option = sys.argv[1]
    if option in ("-h", "--help", "-H"):
        print(usage_desc)
        print(options_desc)
        print(parser_desc)
    elif option in ("-c", "--config", "-C"):
        config.read()
        config.show()
    elif option in ("-v", "--version", "-V"):
        app.print_version()
    elif option in ("-r", "--readme", "-R"):
        app_cmd.view_file("README.md")
    else:
        app.print_error(f"Unknown Option: {option}")
        print(usage_desc)
        print(options_desc)
    sys.exit(1)
    sys.argv.pop(1)

def main_menu():
    menu = Menu("Main Menu")
    menu.add_option(1, "Start", start_menu)
    menu.add_option(2, "Git Status", git_cmd.show_status)
    menu.add_option(3, "Git Log", git_cmd.show_log)
    menu.add_option(4, "Git Diff", diff_menu)
    menu.add_option(5, "Git Pull", git_cmd.pull_changes)
    menu.add_option(6, "Git Push", git_cmd.push_changes)
    menu.add_option(7, "Git Stage", stage_menu)
    menu.add_option(8, "Commit Changes", prompt_commit)
    menu.add_option(9, "Stash Changes", stash_menu)
    menu.add_option(10, "Git Checkout (Tracked)", git_cmd.checkout_patch)
    menu.add_option(11, "Git Clean (Untracked)", git_cmd.clean_interactive)
    menu.add_option(12, "Reset to Commit", commits_menu)
    menu.add_option(13, "Settings", settings_menu)
    menu.add_option(14, "Help", help_menu)
    menu.add_option(15, "About GitWriting", app.show_about)
    menu.add_option(16, "Quit", sys.exit)
    show_stashes_and_changes()
    menu.show(post_action=show_stashes_and_changes)

def start_menu():
    menu = Menu("Start")
    menu.add_option(1, "Back to Main Menu", main_menu)
    menu.add_option(2, "New/Open", new_file)
    menu.add_option(3, "Open Recent", recents_menu)
    menu.add_option(4, "Browse", functools.partial(open_app, "browser"))
    if config.is_daily_notes_enabled():
        menu.add_option(5, "Open Daily Note", open_daily_note)
    git_cmd.show_changes()
    menu.show(post_action=git_cmd.show_changes)

def new_file():
    path = input("Enter new file name (or pass empty name to cancel): ")
    if not path:
        print()
        app.print_error(f"Canceled operation.")
    else:
        if file.is_existing_file(path):
            open_app("editor", path)
        else:
            file.create_new_file(path)
            # Only open editor if file was created properly from the previous step
            if file.is_existing_file(path):
                open_app("editor", path)
            else:
                app.print_error(f"Failed to create or find file '{path}'")

def recents_menu():
    menu = Menu("Open Recent")
    # TODO: make switch flag in this menu set to "Last Modified" or "In Working Tree", reload menu based on toggle
    #   Also create new config setting
    options = git_cmd.get_changes_names_only()
    if not options:
        app.print_warning("No recent files to open.")
    else:
        menu.add_option(1, "Back to Main Menu", main_menu)
        i = 2
        for opt in options:
            menu.add_option(i, opt, functools.partial(open_app, "editor", opt))
            i = i + 1
        menu.show()

def diff_menu():
    menu = Menu("View Diff")
    options = git_cmd.get_diff_options()
    if not options:
        app.print_warning("No tracked changes to analyze.")
    else:
        menu.add_option(1, "Back to Main Menu", main_menu)
        i = 2
        for opt in options:
            menu.add_option(i, opt, functools.partial(git_cmd.show_diff_for_file, opt))
            i = i + 1
        menu.show()

def stage_menu():
    menu = Menu("Stage")
    if not git_cmd.get_changes():
        app.print_warning("No changes to stage or unstage.")
    else:
        menu.add_option(1, "Back to Main Menu", main_menu)
        menu.add_option(2, "Stage All", git_cmd.stage_all_changes)
        menu.add_option(3, "Unstage All", git_cmd.unstage_all_changes)
        menu.add_option(4, "Interactive Stage", git_cmd.stage_interactive)
        git_cmd.show_changes()
        menu.show()

def prompt_commit():
    if not git_cmd.get_staged_changes():
        app.print_warning("No staged changes to commit.")
    else:
        message = input("Enter commit message (or pass empty message to cancel): ")
        if message:
            git_cmd.commit_changes(message)
        else:
            print()
            app.print_error(f"Canceled commit.")

def stash_menu():
    menu = Menu(f"Stash")
    menu.add_option(1, "Back to Main Menu", main_menu)
    menu.add_option(2, "Create Stash", prompt_create_stash)
    menu.add_option(3, "Apply Stash", functools.partial(stashes_menu, "apply"))
    menu.add_option(4, "Pop Stash", functools.partial(stashes_menu, "pop"))
    menu.add_option(5, "Drop Stash", functools.partial(stashes_menu, "drop"))
    show_stashes_and_changes()
    menu.show()

def prompt_create_stash():
    if not git_cmd.get_changes():
        app.print_warning("No changes available to stash.")
        return
    else:
        menu = Menu(f"Create Stash")
        menu.add_option(1, "Go Back", stash_menu)
        menu.add_option(2, "Stash All", functools.partial(prompt_stash_message, include_untracked=True))
        menu.add_option(3, "Stash Staged Only", functools.partial(prompt_stash_message, include_untracked=False))
        git_cmd.show_changes()
        menu.show(post_action=stash_menu)

def prompt_stash_message(include_untracked=False):
    message = input("Enter stash message (or pass empty message to cancel): ")
    if message:
        if include_untracked:
            git_cmd.stash_all_changes(message)
        else:
            git_cmd.stash_staged_changes(message)
    else:
        print()
        app.print_error(f"Canceled stash.")

def stashes_menu(operation):
    menu = Menu(f"Select a Stash")
    options = git_cmd.get_stashes_names_only()
    if not options:
        app.print_warning("No stashes available in this repo.")
        return
    else:
        menu.add_option(1, "Back to Stash Menu", stash_menu)
        i = 2
        for opt in options:
            menu.add_option(i, opt, functools.partial(confirm_existing_stash_operation, operation, opt))
            i = i + 1
        menu.show()
    

def confirm_existing_stash_operation(operation, stash):
    if not git_cmd.get_stashes():
        app.print_warning("No stashes available in this repo.")
        return
    else: 
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

def commits_menu():
    menu = Menu("Select a Commit")
    options = git_cmd.get_commits_hashes_only()
    if not options:
        app.print_warning("No commits available in this repo.")
    else:
        git_cmd.show_commits()
        menu.add_option(1, "Back to Main Menu", main_menu)
        i = 2
        for opt in options:
            menu.add_option(i, opt, functools.partial(reset_menu, opt))
            i = i + 1
        menu.show()

def reset_menu(commit):
    menu = Menu(f"Selected Commit <{commit}>")
    menu.add_option(1, "Back to Commits Menu", commits_menu)
    menu.add_option(2, "Mixed Reset", functools.partial(confirm_reset, "mixed", commit))
    menu.add_option(3, "Soft Reset", functools.partial(confirm_reset, "soft", commit))
    menu.add_option(4, "Hard Reset", functools.partial(confirm_reset, "hard", commit))
    menu.show()

def confirm_reset(reset_type, commit):
    menu = Menu(f"{reset_type.upper()} reset to commit <{commit}>?")
    menu.add_option(1, "Yes", functools.partial(reset, reset_type, commit))
    menu.add_option(2, "No", commits_menu)
    git_cmd.show_commits()
    menu.show()

def confirm_factory_reset():
    app.print_warning("Reset GitWriting back to default settings?  (! THIS WILL ERASE THE EXISTING CONFIG FILE !)")
    menu = Menu("Factory Reset")
    menu.add_option(1, "Yes", config.factory_reset)
    menu.add_option(2, "No", settings_menu)
    menu.show()


def settings_menu():
    menu = Menu("Settings")
    menu.add_option(1, "Back to Main Menu", main_menu)
    menu.add_option(2, "Set Browser", functools.partial(set_app, "browser"))
    menu.add_option(3, "Set Editor", functools.partial(set_app, "editor"))
    menu.add_option(4, "Enable Daily Notes", functools.partial(set_daily_notes_status, "on"))
    menu.add_option(5, "Disable Daily Notes", functools.partial(set_daily_notes_status, "off"))
    menu.add_option(6, "Set Daily Notes Path", set_daily_notes_path)
    menu.add_option(7, "Factory Reset", confirm_factory_reset)
    # menu.add_option(7, "Set Commit Display Limit", set_commit_limit)
    config.read()
    config.show()
    menu.show(post_action=config.show)

def help_menu():
    menu = Menu("Help")
    menu.add_option(1, "Back to Main Menu", main_menu)
    menu.add_option(2, "View Config Example", config.show_config_template)
    menu.show()

def set_daily_notes_status(new_status):
    if (new_status == "on" or new_status == "off"):
        try:
            config.set_daily_notes_status(new_status)
        except Exception as e:
            app.print_error(f"Failed to set daily notes status: {e}")
    else:
        app.print_error(f"Unexpected status '{new_status}'. Status must be 'on' or 'off'.")

def set_daily_notes_path():
    new_path = input("Set new Daily Notes path (or pass empty path to cancel): ")
    if new_path:
        try:
            file.create_new_directory(new_path)
            config.set_daily_notes_path(new_path)
        except (Exception, FileExistsError):
            app.print_error(f"Failed to set daily notes path to '{new_path}'")
    else:
        print()
        app.print_error(f"Canceled. Keep current path: '{config.get_daily_notes_root_path()}'")


def set_app(app_type):
    while True:
        new_app = input(f"Set new {app_type} app (or pass empty name to cancel): ")
        if not new_app:
            print()
            app.print_error(f"Canceled. Keep current {app_type} app: {config.get_app(app_type)}")
            break
        else:
            try:
                if (which(new_app)) is None:
                    raise FileNotFoundError
                else:
                    config.set_app(app_type, new_app)
                    break
            except (FileNotFoundError, Exception):
                config.show_app_not_found_error(new_app)

def reset(reset_type, commit):
    git_cmd.reset
    confirm_reset()

# TODO create custom CLI browser, maybe a menu similar to the Log() screen
def open_app(app_type, fpath=""):
    # if config isn't there (unlikely at this point but could happen), fallback to the system default app
    if not config.is_present():
        open_system_app(app_type, fpath)
        app.print_warning("Config file not found. Opening default system app...")
        return
    else:
        valid_app_types = ["browser", "editor"]
        if app_type not in valid_app_types:
            app.print_error(f"Unknown app type {app_type}. Valid app types are {valid_app_types}.")
            return
        else:
            app = config.get_app(app_type)
            try:
                if (which(app)) is None:
                    raise FileNotFoundError
                else:
                    match(app_type):
                        case "browser":
                            app_cmd.open_browser(app)
                        case "editor":
                            app_cmd.open_editor(app, fpath)
            except (FileNotFoundError, Exception):
                config.show_app_not_found_error(app)
                open_system_app(app_type, fpath)

def open_system_app(app_type, fpath=""):
    app = app.get_system_app(app_type)
    match app_type:
        case "editor":
            app_cmd.open_editor(app, fpath)
        case "browser":
            app_cmd.open_browser(app)
        case _:
            app.print_error(f"App type '{app_type}' is not supported. Failed to retrieve default app for this type.")

def open_daily_note():
    if not config.is_daily_notes_enabled():
        print("\nDaily Notes disabled. See Main Menu -> Settings to enable this feature.")
    else:
        fpath = config.get_today_note_path()
        file.create_new_file(fpath)
        open_app("editor", fpath)

def show_stashes_and_changes():
    git_cmd.show_stashes()
    git_cmd.show_changes()

if __name__ == "__main__":
    main()