# Python Modules
import os
import sys
# My Modules
from config import AppConfig
from commands import GitCommand, AppCommand
import app_utils as app
import file_utils
import menus
import prompts

app_cfg = AppConfig(app.get_expected_config_path(), quiet=True)
git_cmd = GitCommand(quiet=True)
app_cmd = AppCommand()
# __target_directory = app.os.getcwd()()

def main():
    """Entry point method"""
    while len(sys.argv) > 1:
        handle_launch_args()
    # TODO testing macOS package not finding proper directories
    app.show_splash()
    try:
        app_cfg.read()
    except FileNotFoundError:
        prompts.prompt_create_config()

    if not git_cmd.is_working_dir_at_git_repo_root():
        app.print_warning(f"The working directory '{os.getcwd()}' is not the root directory of a valid Git repository.")
        app.print_warning("Source control is disabled. To re-enable source control, please exit and move the GitWriting executable and config file to the root directory of a valid Git repository.")    
    else:
        # Set the working directory to the repo root
        app.change_working_directory(git_cmd.get_repo_root())
    menus.main_menu()

def handle_launch_args():
    """Handle launch arguments when the app is launched"""
    options_desc = "[Options] \nHelp: [-h | --help | -H] \nSetup/View Config: [-c | --config | -C] \nVersion: [-v | --version | -V], \nView README: [-r | --readme | -R]\nView App Dependencies: [-d | --dependencies | -D]"
    usage_desc = f"\n[Usage] \n./{os.path.basename(__file__)} [OPTION]\n"
    parser_desc = f"\nSettings are defined in '{file_utils.get_path_tail(app_cfg.path)}'. See 'README.md' for a template config file."

    option = sys.argv[1]
    if option in ("-h", "--help", "-H"):
        print(usage_desc)
        print(options_desc)
        print(parser_desc)
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
