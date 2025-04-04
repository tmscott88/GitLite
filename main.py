# Python Modules
import os
import sys
import functools
from shutil import which
# My Modules
import app_utils
import file_utils
from config import AppConfig
from commands import GitCommand, AppCommand
from menu import Menu

config = AppConfig()
git_cmd = GitCommand()
app_cmd = AppCommand()

def main():
    # repo = GitRepository(".")
    while len(sys.argv) > 1:
        handle_launch_args()

    # TODO: interactive prompts for first-time config setup
    if not config.is_present():
        # config.generate()
        prompt_create_config()
    else:
        config.read()
    app_utils.show_splash()
        
    main_menu()

def prompt_create_config():
    print(f"\nWelcome to GitWriting!")
    print("\n* Let's get you set up and writing!")
    config.generate()
    print(f"? Questions? Visit '{app_utils.project_url}' for more information.")
    print("\n* First, please enter your preferred file editor. If you are unsure or wish to use your system's default editor, just press enter.")
    print()
    set_app("editor")
    print("\n* Next, please enter your preferred file browser. If you are unsure or wish to use your system's default editor, just press enter.")
    set_app("browser")

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
        app_utils.print_version()
    elif option in ("-r", "--readme", "-R"):
        app_cmd.view_file("README.md")
    else:
        print(f"\nUnknown Option: {option}")
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
    # menu.add_option(9, "Stash Changes", stash_menu)
    menu.add_option(10, "Git Checkout (Tracked)", git_cmd.checkout_patch)
    menu.add_option(11, "Git Clean (Untracked)", git_cmd.clean_interactive)
    menu.add_option(12, "Reset to Commit", commits_menu)
    menu.add_option(13, "Settings", settings_menu)
    menu.add_option(14, "Help", help_menu)
    menu.add_option(15, "About GitWriting", app_utils.show_about)
    menu.add_option(16, "Quit", sys.exit)

    git_cmd.show_changes()
    menu.show()

def start_menu():
    menu = Menu("Start")
    menu.add_option(1, "Back to Main Menu", main_menu)
    menu.add_option(2, "New/Open", new_file)
    menu.add_option(3, "Open Recent", recents_menu)
    menu.add_option(4, "Browse", functools.partial(open_app, "browser"))
    git_cmd.show_changes()
    menu.show()

def new_file():
    path = input("Enter new file name (or pass empty file name to cancel): ")
    if not path:
        print("\nCanceled operation.")
    else:
        if file_utils.is_existing_file(path):
            open_app("editor", path)
        else:
            file_utils.create_new_file(path)
            # Only open editor if file was created properly from the previous step
            if file_utils.is_existing_file(path):
                open_app("editor", path)
            # else:
                # print(f"\nCould not create or find file '{path}'")

def recents_menu():
    menu = Menu("Open Recent")
    # TODO: make switch flag in this menu set to "Last Modified" or "In Working Tree", reload menu based on toggle
    #   Also create new config setting
    options = git_cmd.get_changes_names_only()
    if not options:
        print("\nNo recent files to open.")
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
        print("\nNo tracked changes to analyze.")
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
        print("\nNo changes to stage or unstage.")
    else:
        menu.add_option(1, "Back to Main Menu", main_menu)
        menu.add_option(2, "Stage All", git_cmd.stage_all_changes)
        menu.add_option(3, "Unstage All", git_cmd.unstage_all_changes)
        menu.add_option(4, "Interactive Stage", git_cmd.stage_interactive)
        git_cmd.show_changes()
        menu.show()

def prompt_commit():
    if not git_cmd.get_staged_changes():
        print("\nNo staged changes to commit.")
    else:
        message = input("Enter commit message (or pass empty message to cancel): ")
        if message:
            git_cmd.commit_changes()
        else:
            print("\nCanceled commit.") 

def commits_menu():
    menu = Menu("Select a Commit")
    options = git_cmd.get_commits_hashes_only()
    if not options:
        print("\nNo commits available in this repo.")
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

def settings_menu():
    menu = Menu("Settings")
    menu.add_option(1, "Back to Main Menu", main_menu)
    menu.add_option(2, "Set Browser", functools.partial(set_app, "browser"))
    menu.add_option(3, "Set Editor", functools.partial(set_app, "editor"))
    menu.add_option(4, "Enable Daily Notes", functools.partial(set_daily_notes_status, "on"))
    menu.add_option(5, "Disable Daily Notes", functools.partial(set_daily_notes_status, "off"))
    menu.add_option(6, "Set Daily Notes Path", set_daily_notes_path)
    # menu.add_option(7, "Set Commit Display Limit", set_commit_limit)
    config.read()
    config.show()
    menu.show()

def help_menu():
    menu = Menu("About")
    menu.add_option(1, "Back to Main Menu", main_menu)
    menu.add_option(2, "View Config (Template)", app_utils.show_config_template)
    menu.show()

def set_daily_notes_status(new_status):
    if (new_status == "on" or new_status == "off"):
        try:
            config.set_daily_notes_status(new_status)
        except Exception as e:
            print(f"\nCould not set daily notes status: {e}")
    else:
        print(f"\nUnexpected status '{new_status}'. Status must be 'on' or 'off'.")

def set_daily_notes_path():    
    new_path = input("Set new Daily Notes path (or pass empty message to cancel): ")
    if new_path:
        file_utils.create_new_directory(new_path)
    else:
        print(f"\nCanceled. Keep current path: '{config.get_daily_notes_path()}'")  
    try:
        config.set_daily_notes_path()
    except Exception as e:
        print(f"\nCould not set daily notes path: {e}")

def set_app(app_type):
    new_app = input(f"Set new {app_type} app (or pass empty message to cancel): ")
    if not new_app:
        print(f"\nCanceled. Keep current {app_type} app: {config.get_app(app_type)}")
    else:
        try:
            if (which(new_app)) is None:
                raise FileNotFoundError
            else:
                config.set_app(app_type, new_app)
        except FileNotFoundError:
            config.show_app_not_found_error(new_app)
        except Exception as e:
            print(f"\nCould not set {app_type} to '{new_app}'. {e}")

# def set_commit_limit():
#     new_limit = input("Set new commit display limit (or pass empty message to cancel): ")
#     if not new_limit:
#         print(f"\nCanceled. Keep current commit limit: {config.get_commit_limit()}")
#     elif (int(new_limit) < 1):
#         print("\nLimit must be a positive integer")
#     else:
#         try:
#             config.set_commit_limit(new_limit)
#         except Exception as e:
#             print(f"\nCould not set commit limit to '{new_limit}'. {e}")

def reset(reset_type, commit):
    git_cmd.reset
    confirm_reset()

# TODO create custom CLI browser, maybe a menu similar to the Log() screen
def open_app(app_type, fpath=""):
    # # if not has_valid_config():
    #     open_system_browser()
    #     return
    # else:
    valid_app_types = ["browser", "editor"]
    if app_type not in valid_app_types:
        print(f"\nUnknown app type {app_type}. Valid app types are {valid_app_types}.")
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
        except (FileNotFoundError):
            config.show_app_not_found_error(app)
            # open_system_browser()
        except Exception as e:
            print(f"\nCould not open {app_type} app '{app}'. {e}")
            # open_system_browser()

# TODO create custom browser instead
# def open_system_browser():
#     # browser = get_system_browser()
#     if app_utils.get_platform() == "Unix":
#         return
#         # Unix lacks a default/standard file manager, while Windows lacks a standard TTY editor (unless you want to use 'copy con'). Pros and cons. You can't win them all...
#     elif app_utils.get_platform() == "Windows":
#         # TODO add default Window browser
#         # if get_platform() == "Windows":
#         #     then open File Explorer
#         print(f"\nWindows system browser coming soon.")
    
def open_system_app(fpath):
    app = app_cmd.get_system_editor()
    if app_utils.get_platform() == "Unix":
        print(f"\nWarning: No config file to read editor from. Opening default editor '{editor}'...")
        if editor:
            open_app(editor, fpath)
        else:
            print(f"\nCould not retrieve default editor.")
            return
    elif get_platform() == "Windows":
        print(f"\nWindows system editor function coming soon.")
        # TODO add default Windows editor
        # open Notepad or maybe search for nano and route there            


# def open_daily_note(fpath):
#     daily_notes_dir = get_daily_notes_path()
#     self.open_editor({os.path.join(daily_notes_dir, fpath)})

if __name__ == "__main__":
    main()