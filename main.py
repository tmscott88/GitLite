"""The entry point module for GitWriting"""
# Python Modules
import os
import sys
# My Modules
from config import AppConfig
from commands import GitCommand, AppCommand
import app_utils as app
import menus
import prompts

app_cfg = AppConfig(quiet=True)
git_cmd = GitCommand()
app_cmd = AppCommand()

def main():
    """Entry point method"""
    # Launch arguments
    while len(sys.argv) > 1:
        __handle_launch_args()
    app.show_splash()
    # Check for a config file
    try:
        app_cfg.read()
        # Use the working directory from the config file
        working_dir = app_cfg.get_default_working_directory()
        app.change_working_directory(working_dir)
    except FileNotFoundError:
        prompts.prompt_create_config()
    # Check is we're in a Git repo
    if not git_cmd.is_inside_git_repo():
        prompts.prompt_select_repo()
    menus.main_menu()


def __handle_launch_args():
    """Handle launch arguments when the app is launched"""
    options_desc = "[Options] \nHelp: [-h | --help | -H] \
        \nSetup/View Config: [-c | --config | -C]  \
        \nVersion: [-v | --version | -V],  \
        \nView README: [-r | --readme | -R] \
        \nView App Dependencies: [-d | --dependencies | -D]"
    usage_desc = f"\n[Usage] \n./{os.path.basename(__file__)} [OPTION]\n"

    option = sys.argv[1]
    if option in ("-h", "--help", "-H"):
        print(usage_desc)
        print(options_desc)
    elif option in ("-c", "--config", "-C"):
        try:
            app_cfg.read()
            app_cfg.show()
        except FileNotFoundError:
            app.print_question("Would you like to create a new config file?")
            if app.prompt_continue():
                prompts.prompt_create_config(is_full_launch=False)
    elif option in ("-v", "--version", "-V"):
        app.print_version()
    elif option in ("-r", "--readme", "-R"):
        app_cmd.show_readme()
    elif option in ("-d", "--dependencies", "-D"):
        app_cmd.show_requirements()
    else:
        app.print_error(f"Unknown Option: {option}")
        print(usage_desc)
        print(options_desc)
    sys.argv.pop(1)
    sys.exit(1)

if __name__ == "__main__":
    main()
