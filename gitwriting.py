#!/usr/bin/env python3

import configparser  
import subprocess
import os
import sys
import readchar
from shutil import which
from datetime import datetime

__parser = configparser.ConfigParser()
__version_num = "0.8.3-8"
__config = "config.ini"

def main():
    options_desc = "[Options] \nHelp: [-h | --help | -H] \nCheck Config: [-c | --config | -C] \nVersion: [-v | --version | -V]"
    usage_desc = f"\n[Usage] \n./{os.path.basename(__file__)} [OPTION]\n"
    parser_desc = f"\nSettings are defined in '{__config}'. See 'README.md' for a template config file."

    # Launch arguments
    while len(sys.argv) > 1:
        option = sys.argv[1]
        if option in ("-h", "--help", "-H"):
            print(usage_desc)
            print(options_desc)
            print(parser_desc)
        elif option in ("-c", "--config", "-C"):
            if not has_valid_config():
                print_config_not_found_error()
            else:
                print(f"\n> {__config}")
                print_config()
                print()
        elif option in ("-v", "--version", "-V"):
            print(f"Gitlite {__version_num}")
        else:
            print(f"\nUnknown Option: {option}")
            print(usage_desc)
            print(options_desc)
        sys.exit(1)
        sys.argv.pop(1)

    # Post-options flow
    print_splash()
    # TODO testing macOS package not finding proper directories
    if not is_valid_repo():
        print(f"\nError: Could not resolve a valid Git repo from the current folder.") 
        print("\nPlease place this executable in your Git repo's root directory.")
        prompt_exit()
    else:
        # initial config verification
        if not has_valid_config():
            print_config_not_found_error()
        print_stashes()
        print_changes()
        main_menu()

# check if we're inside a valid git repo
def is_valid_repo():
    try:
        git_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip()
        script_dir = get_current_dir()
        # match the path seperators
        # print(f"\n(DEBUG) Git Root: {git_root}")
        # print(f"(DEBUG) Script Dir: {script_dir}")
        return bool(git_root == script_dir)
    except subprocess.CalledProcessError:   
        print("\nPlease place this executable in your Git repo's root directory.")
        return False

def has_valid_config():
    try:
        with open(__config, 'r', encoding="utf-8") as file:
            __parser.read(__config)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"\nCould not read config file {__config}: {e}")
    return False

# def has_valid_sections():
#     for section in __parser.sections():
#         # TODO: check if section is within valid "Sections" enum
#         for key, value in __parser.items(section):
#             # TODO: check if key, value matches expected format? Key match is most important
#             print(f"{key} = {value}")

def save_to_config(message):
    try:
        with open(__config, "w", encoding="utf-8") as newfile:
            __parser.write(newfile)
        print(f"\n{message}")
    except Exception as e:
        print(f"\nCould not save to config file '{newfile}': {e}")

def get_platform():
    match(os.name):
        case "nt":
            return "Windows"
        case "posix":
            return "Unix"
        case _:
            return "Other"

def get_current_dir():
    current = os.path.dirname(os.path.abspath(sys.argv[0]))
    unix_converted = current.strip().replace(os.sep, '/')
    return unix_converted

def prompt_exit():
    print("\nPress any key to exit...")
    k = readchar.readchar()
    sys.exit()

# Parser getters
def get_browser():
    try:
        return __parser.get('APPS', 'browser')
    except Exception as e:
        print(f"\nCould not retrieve browser from '{__config}'. {e}")
        print(f"\nPlease check '{__config}' or visit Main Menu -> Settings to configure a valid browser.")
        # return get_system_browser()

def get_editor():
    try:
        return __parser.get('APPS', 'editor')
    except Exception as e:
        print(f"\nCould not retrieve editor from '{__config}'. {e}")
        print(f"\nPlease check '{__config}' or visit Main Menu -> Settings to configure a valid editor.")
        return get_system_editor()

def get_commit_limit():
    try:
        return __parser.get('MISC', 'commit_limit')
    except Exception as e:
        print(f"\nCould not retrieve commit limit from '{__config}'. {e}")
        print(f"\nPlease check '{__config}' or visit Main Menu -> Settings to configure a valid limit.")
        return -1

def get_daily_notes_status():
    try:
        return __parser.get('DAILY_NOTES', 'status')
    except Exception as e:
        print(f"\nCould not retrieve daily notes status from '{__config}'. {e}")
        print(f"\nPlease check '{__config}' or visit Main Menu -> Settings to configure a valid status.")

def get_daily_notes_path():
    try:
        return __parser.get('DAILY_NOTES', 'path')
    except Exception as e:
        print(f"\nCould not retrieve daily notes path from '{__config}'. {e}")
        print(f"\nPlease check '{__config}' or visit Main Menu -> Settings to configure a valid path.")

def set_app(new_app, app_type):
    try:
        if (which(new_app)) is None:
            raise FileNotFoundError
        else:
            __parser.set('APPS', app_type, new_app)
            save_to_config(f"Set {app_type}: {new_app}")
    except FileNotFoundError:
        print_app_error(new_app)
    except Exception as e:
        print(f"\nCould not set {app_type} to '{new_app}'. {e}")
    

def set_commit_limit(new_limit):
    limit = int(new_limit)
    if (limit < 1):
        print("\nLimit must be a positive integer")
        return
    else:
        try:
            __parser.set('MISC', 'commit_limit', new_limit)
            save_to_config(f"Set commit limit: {new_limit}")
        except Exception as e:
            print(f"\nCould not set commit limit to '{new_limit}'. {e}")

def set_daily_notes_status(new_status):
    if (new_status == "on" or new_status == "off"):
        try:
            
            __parser.set('DAILY_NOTES', 'status', new_status)
            save_to_config(f"Set Daily Notes: {new_status}")
        except Exception as e:
            print(f"\nCould not set daily notes status: {e}")
    else:
        print(f"\nUnexpected status '{new_status}'. Status must be 'on' or 'off'.")

def set_daily_notes_path(new_path):
    try:
        __parser.set('DAILY_NOTES', 'path', new_path)
        save_to_config(f"Set daily notes path: {new_path}")
    except Exception as e:
        print(f"\nCould not set daily notes path: {e}")

def is_existing_file(path):
    return bool(os.path.isfile(path))
    
def is_existing_directory(dir):
    return bool(os.path.isdir(dir))

def create_new_file(new_path):
    # if file nor (conflicting) directory exist, create the file
    if not is_existing_file(new_path) and not is_existing_directory(new_path):
        try:
            # TODO test path normalization/input sanitization
            # normalized_path = os.path.normpath(new_path)    
            # print(new_path)
            # print(normalized_path)
            
            # Extract just path from full path. Create all intermediate directors up to file if needed, exist_ok=True to not raise error if directory already exists
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            # Create the file
            f = open(new_path, 'w')
            print(f"\nCreated file {new_path}.")
        except subprocess.CalledProcessError as e:
            print(f"\nCould not create file '{new_path}'. {e}")
            return
        # Only open editor if file was created properly from the previous step
        if is_existing_file(new_path):
            open_editor(new_path)
        else:
            print(f"\nCanceled file creation.")
    # if file doesn't exist but conflicting folder exists
    elif not is_existing_file(new_path):
        print(f"\nA folder '{new_path}' already exists in this directory. Please choose a different file name or path.")
    # file already exists, just open
    else:
        print(f"\nFile '{new_path}' already exists. Opening...")
        open_editor(new_path)

def create_new_directory(new_path):
    # if path doesn't exist, create the directory
    if not is_existing_directory(new_path) and not is_existing_file(new_path):
        try:
            # TODO test path normalization
            os.makedirs(new_path, exist_ok=True)
            if is_existing_directory(new_path):
                set_daily_notes_path(new_path)
                
            else:
                print(f"\nPath creation failed. Keep current path: '{get_daily_notes_path()}'.")
                return
        except Exception as e:
            print(f"\nCould not create directory '{new_path}'. {e}")
            return
    # if directory doesn't exist but conflicting file exists
    elif not is_existing_directory(new_path) and is_existing_file(new_path):
        print(f"\nA file '{new_path}' already exists in this directory. Please choose a different directory name or path.")
    else:
        set_daily_notes_path(new_path)
        
# HELPER FUNCTIONS

def file_has_changes(fpath):
    status = subprocess.check_output(['git', 'status', fpath, '--short'])
    return bool(status)

def repo_has_commits():
    commits = subprocess.check_output(['git', 'log', '--oneline', '-n', '1'])
    return bool(commits)

def repo_has_changes():
    changes = subprocess.check_output(['git', 'status', '--porcelain'])
    return bool(changes)

def repo_has_staged_changes():
    staged = subprocess.check_output(['git', 'diff', '--name-status', '--cached'])
    return bool(staged)

def repo_has_stashes():
    stashes = subprocess.check_output(['git', 'stash', 'list'])
    return bool(stashes)

def is_daily_notes_enabled():
    status = get_daily_notes_status()
    return bool(status == "on")

def print_splash():
    print(f"\n[GitLite {__version_num}]")
    print("Author: Tom Scott (tmscott88)")
    print("https://github.com/tmscott88/GitLite")

def print_config():
    for section in __parser.sections():
        print()
        print(f"[{section}]")
        for key, value in __parser.items(section):
            print(f"{key} = {value}")

def print_commits(limit):
    if repo_has_commits():
        print("\n[Commits]")
        run(['git', 'log', '--oneline', '--all', '--decorate', '-n', f"{limit}"], "")

def print_changes():
    if repo_has_changes():
        print("\n[Changes]")
        run(['git', 'status', '-s', '-u'], "")

def print_stashes():
    if repo_has_stashes():
        print("\n[Stashes]")
        run(['git', 'stash', 'list'], "")

def print_options(options, title):
    print(f"\n[{title}]")
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")

def print_app_error(name):
    print(f"\nApp '{name}' not found, or '{name}' just crashed. This may be due to a missing reference/installation, or perhaps something is wrong with {name}'s configuration.") 
    print(f"\nEnsure that the app's reference name is defined correctly in '{__config}' and installed systemwide.") 
    print(f"\nConsult {name}'s documentation and/or forums for more information.")
    print(f"\nIf '{name}' works fine outside of GitLite, and you are still experiencing issues here, please open an issue at:")
    print("\nhttps://github.com/tmscott88/GitLite/issues")

# def print_config_corrupt_error():
#     print(f"\nWarning: Config file '{__config}' has corrupt or missing properties. Functionality will be limited until this is resolved.") 
#     # print(f"\nPlease create and place `{__config}' in your Git repo's root directory.")
#     print(f"\nSee the included README or visit https://github.com/tmscott88/GitLite/blob/main/README.md for further instructions.")

def print_config_not_found_error():
    print(f"\nWarning: Config file '{__config}' not found. Functionality will be limited until this is resolved.") 
    print(f"\nPlease create and place `{__config}' in your Git repo's root directory.")
    print(f"\nSee the included README or visit https://github.com/tmscott88/GitLite/blob/main/README.md for further instructions.")

# TODO create custom CLI browser, maybe a menu similar to the Log() screen
def open_browser():
    if not has_valid_config():
        open_system_browser()
        return
    else: 
        browser = get_browser()
        try:
            if (which(browser)) is None:
                raise FileNotFoundError
            else:
                 run(browser, "")
        except (FileNotFoundError, subprocess.CalledProcessError):
            print_app_error(browser)
            open_system_browser()
        except Exception as e:
            print(f"\nCould not open browser '{browser}'. {e}")
            open_system_browser()

# TODO is this needed??
# def get_system_browser():
#     if get_platform() == "Unix":
#         editor = os.getenv('EDITOR')
#         return browser if browser else "nano"
#     elif get_platform() == "Windows":
#         print(f"\nWindows system browser coming soon.")
#         # TODO add default Windows browser
#         # open File Explorer

def open_system_browser():
    # browser = get_system_browser()
    if get_platform() == "Unix":
        return
        # Unix lacks a default/standard file manager, while Windows lacks a standard TTY editor (unless you want to use 'copy con'). Pros and cons. You can't win them all...
    elif get_platform() == "Windows":
        # TODO add default Window browser
        # if get_platform() == "Windows":
        #     then open File Explorer
        print(f"\nWindows system browser coming soon.")
        
def open_editor(fpath):
    if not has_valid_config():
        # Open default system editor (Unix & Windows supported)
        open_system_editor(fpath)
        return
    else: 
        editor = get_editor()
        try:
            if (which(editor)) is None:
                raise FileNotFoundError
            else:
                 run([editor, fpath], "")
        except (FileNotFoundError, subprocess.CalledProcessError):
            print_app_error(editor)
            # open_system_editor(fpath)
        except Exception as e:
            print(f"\nCould not open editor '{editor}'. {e}")
            # open_system_editor(fpath)
            
def get_system_editor():
    if get_platform() == "Unix":
        editor = os.getenv('EDITOR')
        return editor if editor else "nano"
    elif get_platform() == "Windows":
        print(f"\nWindows system editor coming soon.")
        # TODO add default Windows editor
        # open Notepad or maybe search for nano and route there
    
def open_system_editor(fpath):
    editor = get_system_editor()
    if get_platform() == "Unix":
        print(f"\nWarning: No config file to read editor from. Opening default editor '{editor}'...")
        if editor:
            run([editor, fpath], "")
        else:
            print(f"\nCould not retrieve default editor.")
            return
    elif get_platform() == "Windows":
        print(f"\nWindows system editor function coming soon.")
        # TODO add default Windows editor
        # open Notepad or maybe search for nano and route there            
            
def open_daily_note(fpath):
    daily_notes_dir = get_daily_notes_path()
    open_editor({os.path.join(daily_notes_dir, fpath)})


def run(command_args, message):
    try:
        subprocess.run(command_args, check=True)
        if message != "":
            print(f"\n{message}")
    except FileNotFoundError as e:
        print(f"\nFileNotFoundError: {e}")
    except subprocess.CalledProcessError as e:
        print(f"\nCommand failed. {e}")    
        
def main_menu():
    options = ["Start", "Status", "Log", "Diff", "Pull", "Push", "Stage", "Commit", "Stash", "Revert", "Discard", "Reset", "Settings", "About", "Quit"]
    while True:
        print_options(options, "Main Menu")
        try:
            choice = int(input("Choose an option: ")) - 1
            if choice not in range(0, len(options)):
                raise ValueError()
            else: 
                match options[choice]:
                    case "Start":
                        prompt_start()
                    case "Status":
                        run(['git', 'fetch'], "")
                        print("\n[Status]") 
                        run(['git', 'status'], "")
                    case "Log":
                        prompt_log()
                    case "Diff":
                        diff = subprocess.check_output(['git', 'diff'])
                        if not diff:
                            print("\nNo tracked changes to analyze.")
                        else:
                            run(['git', 'diff'], "")
                    case "Pull":
                        run(['git', 'pull'], "")
                    case "Push":
                        run(['git', 'push'], "")
                    case "Stage":
                        prompt_stage()
                    case "Commit":
                        if not repo_has_staged_changes():
                            print("\nNo changes staged for commit. Please stage changes before committing.")
                        else:
                            prompt_commit()
                    case "Stash":
                        print("\nStash menu coming soon.")
                        if file_has_changes(__file__):
                            print("\nCannot safely stash because this script has been modified. Please commit this script first.")
                            continue
                        if not (repo_has_changes() or repo_has_stashes()):
                            print("\nNo changes to stash. No stashes to apply. Cannot proceed.")
                        elif repo_has_changes() and not repo_has_stashes():
                            print("\nNo stashes found. Create a stash?")
                            prompt_create_stash()
                        else:
                            prompt_stash_menu() 
                    case "Revert":
                        run(['git', 'checkout', '-p'], "")
                    case "Discard":
                        reset = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'])
                        if not reset:
                            print("\nNo untracked changes to discard.")
                        else:
                            run(['git', 'clean', '-i', '-d'], "")
                    case "Reset":
                        if not repo_has_commits:
                            print("\nNo commits in this repository.")
                        else:
                            prompt_select_commit()
                    case "Settings":
                        if not has_valid_config():
                            print("\nError: Settings menu disabled due to missing config file.")
                            print_config_not_found_error()
                        else:
                            prompt_settings()
                    case "About":
                        print_splash()
                        print(f"Platform: {get_platform()}")
                        print(f"Python: {sys.version[:7]}")
                    case "Quit":
                        sys.exit(1)  
                    case _:
                        raise IndexError
        except (ValueError, IndexError):
            print("\nInvalid input.")
        print_stashes()
        print_changes()

# PROMPT FUNCTIONS
def prompt_start():
    # TODO name these better lol
    options = ["Back to Main Menu", "New/Open", "Open Recent", "Browse"]
    if not has_valid_config():
        print_config_not_found_error()
    else:
        if is_daily_notes_enabled():
            options = ["Back to Main Menu", "New/Open", "Open Recent" "Browse", "Open Daily Note"]
    while True:
        print_options(options, "Start")
        try:
            choice = int(input("Choose an option: ")) - 1
            if choice not in range(0, len(options)):
                raise ValueError()
            else: 
                match options[choice]:
                    case "Back to Main Menu":
                        break
                    case "New/Open":
                        # ask for filename (accept path or directory)
                        file_name = input("Enter new file name (or pass empty message to cancel): ")
                        if file_name:
                            create_new_file(os.path.join(get_current_dir(), file_name).replace("\\","/"))
                        else:
                            print("\nCanceled new file.")
                    case "Open Recent":
                        prompt_resume()
                    case "Browse":
                        open_browser()
                    case "Open Daily Note":
                        if not is_daily_notes_enabled():
                            print("\nDaily Notes disabled. See Main Menu -> Settings to enable this feature.")
                        else:
                            root = get_daily_notes_path()
                            now = datetime.now().strftime("%F")
                            # ['YEAR', 'MONTH', 'DAY'] 
                            date_arr = now.split("-")
                            day = date_arr[2]
                            year_month = f"{date_arr[0]}-{date_arr[1]}"
                            note_filename = f"{date_arr[0]}-{date_arr[1]}-{date_arr[2]}.md"
                            # root/YEAR/YEAR-MONTH/YEAR-MONTH-DAY.md
                            full_note_path = os.path.join(root, date_arr[0], year_month, note_filename)
                            create_new_file(full_note_path)
                    case _:
                        raise IndexError()
        except (ValueError, IndexError):
            print("\nInvalid input.")

def prompt_resume():
    # TODO: make switch flag in this menu set to "Last Modified" or "In Working Tree", reload menu based on toggle
    #   Also create new config setting
    files = []
    # Cut leading status letter (e.g. "M")
    try:
        statuses = subprocess.check_output(['git', 'status', '-s', '-u'], text=True).splitlines()
        files = [file[3:] for file in statuses] 
    except subprocess.CalledProcessError as e:
        print(f"\nCould not get available files: {e}") 
    if not files:
        return
    else:
        options = ["Back to Main Menu"] + files 
        while True:
            for i, file in enumerate(options):
                print(f"{i+1}. {file}")
            try:
                choice = int(input("Choose an option: ")) - 1
                if choice not in range(0, len(options)):
                    raise ValueError()
                elif choice == 0:
                    break
                else:
                    file = options[choice]
                    open_editor(file)
                    break
            except (ValueError, IndexError):
                print("\nInvalid input.")

def prompt_log():
    # FALLBACK
    limit = -1
    config_limit = get_commit_limit()
    options = ["Back to Main Menu", "Simple", "Standard", "Verbose"]
    if (has_valid_config() and config_limit != -1):
        limit = config_limit
        options = ["Back to Main Menu", "Simple", "Standard", "Verbose", "Commit Limit"]
    while True:
        if int(limit) == 1:
            print(f"\nLimit: {limit} commit")
        elif int(limit) > 0:
            print(f"\nLimit: {limit} commits")
        print_options(options, "Log")
        try:
            choice = int(input("Choose an option: ")) - 1
            if choice not in range (0, len(options)):
                raise ValueError()
            else:
                match options[choice]:
                    case "Back to Main Menu":
                        break
                    case "Simple":
                        print_commits(limit)
                    case "Standard":
                        run(['git', 'log', '--name-status', '--all', '-n', f'{limit}'], "")
                    case "Verbose":
                        run(['git', 'log', '--oneline', '-p', '-n', f'{limit}'], "")
                    case "Commit Limit":
                        prompt_set_commit_limit()
                        current_limit = get_commit_limit()
                        if int(current_limit) > 0:
                            limit = current_limit                 
                    case _:
                        raise IndexError()
        except (ValueError, IndexError):
            print("\nInvalid input.")

def prompt_commit():
    message = input("Enter commit message (or pass empty message to cancel): ")
    if message:
        run(['git', 'commit', '-m', f"{message}"], "") 
    else:
        print("\nCanceled commit.")

def prompt_set_commit_limit():
    new_limit = input("Set new commit display limit (or pass empty message to cancel): ")
    if new_limit:
        set_commit_limit(new_limit)
        limit = get_commit_limit()
    else:
        print(f"\nCanceled. Keep current display limit: {get_commit_limit()}")

def prompt_stage():
    options = ["Back to Main Menu", "Stage-All", "Unstage-All", "Stage-Interactive"]
    while True:
        print_options(options, "Stage")
        try:
            choice = int(input("Choose an option: ")) - 1
            if choice not in range(0, len(options)):
                raise ValueError()
            match options[choice]:
                case "Back to Main Menu":
                    break
                case "Stage-All":
                    run(['git', 'add', '-A'], "Staged all changes.")
                case "Unstage-All":
                    run(['git', 'restore', '--staged', '.'], "Unstaged all changes")
                case "Stage-Interactive":
                    run(['git', 'add', '-i'], "")
                case _:
                    raise IndexError
        except (ValueError, IndexError):
            print("\nInvalid input.")
        print_changes()

def prompt_create_stash():
    print("\nNOTE: Patch mode does not include untracked files.")
    options = ["Go Back", "Stash All", "Stash Staged"]
    while True:
        print_options(options, "Create Stash")
        try:
            choice = int(input("Choose an option: ")) - 1
            if choice not in range(0, len(options)):
                raise ValueError()
            match options[choice]:
                case "Go Back":
                    break
                case "Stash All":
                    message = input("Enter stash message (or pass empty message to cancel): ")
                    if message:
                        run(['git', 'stash', 'push', '-u', '-m', f"{message}"], "Stashed all changes.")
                    else:
                        print("\nCanceled stash.")
                    break
                case "Stash Staged":
                    message = input("Enter stash message (or pass empty message to cancel): ")
                    if message:
                        run(['git', 'stash', 'push', '--staged', '-m', f"{message}"], "Stashed all staged changes.")
                    break
                case _:
                    IndexError
        except (ValueError, IndexError):
            print("\nInvalid input.")

def prompt_stash_menu():
    back_stash_menu = "Back to Stash Menu"
    stashes = subprocess.check_output(['git', 'stash', 'list'], text=True).splitlines()
    stashes_trim = [x.split(":")[0] for x in stashes]
    print_stashes()
    options = ["Back to Main Menu", "Create Stash", "Apply Stash", "Pop Stash", "Drop Stash"]
    while True:
        print_options(options, "Stash Menu")
        try:
            choice = int(input("Choose an option: ")) - 1
            if choice not in range(0, len(options)):
                raise ValueError()
            match options[choice]:
                case "Back to Main Menu":
                    break
                case "Create Stash":
                    if not repo_has_changes():
                        print("There are no changes to stash.")
                    else:
                        prompt_create_stash()
                    break
                case "Apply Stash":
                    if not repo_has_stashes():
                        print("There are no stashes in this repo.")
                    else:
                        print("Note: This will apply the stored copy of the stash and preserve it in the local tree.")
                        stash_options = ["Back to Main Menu"] + stashes_trim
                        while True:
                            for i, stash in enumerate(stashes_trim):
                                print(f"{i+1}. {stash}")
                            try:
                                stash_choice = int(input("Choose an option: ")) - 1
                                if stash_choice not in range(0, len(stashes_trim)):
                                    raise ValueError()
                                else:
                                    stash = stashes_trim[stash_choice]
                                    run(['git', 'stash', 'apply', stash], f"Applied stash {stash} onto working tree.")
                                    break
                            except (ValueError, IndexError):
                                print("\nInvalid input.")
                                continue
                case "Pop Stash":
                    if not repo_has_stashes():
                        print("There are no stashes in this repo.")
                    else:
                        print("Note: This will apply the stored copy of the selected stash and remove it from the local tree.")
                        stash_options = ["Back to Main Menu"] + stashes_trim
                        while True:
                            for i, stash in enumerate(stashes_trim):
                                print(f"{i+1}. {stash}")
                            try:
                                stash_choice = int(input("Choose an option: ")) - 1
                                if stash_choice not in range(0, len(stashes_trim)):
                                    raise ValueError()
                                else:
                                    stash = stashes_trim[stash_choice]
                                    run(['git', 'stash', 'pop', stash], f"Popped stash {stash} onto working tree.")
                                    break
                            except (ValueError, IndexError):
                                print("\nInvalid input.")
                                continue
                case "Drop Stash":
                    if not repo_has_stashes():
                        print("There are no stashes in this repo.")
                    else:
                        print("Note: This will drop the stored copy of the selected stash.")
                        stash_options = ["Back to Main Menu"] + stashes_trim
                        while True:
                            for i, stash in enumerate(stashes_trim):
                                print(f"{i+1}. {stash}")
                            try:
                                stash_choice = int(input("Choose an option: ")) - 1
                                if stash_choice not in range(0, len(stashes_trim)):
                                    raise ValueError()
                                else:
                                    stash = stashes_trim[stash_choice]
                                    print(f"\nDrop stash {stash}? THIS STASH WILL BE DISCARDED!")
                                    drop_confirm_options = ["Yes", "No"]
                                    while True:
                                        for i, opt in enumerate(drop_confirm_options):
                                            print(f"{i+1}. {opt}")
                                        try:
                                            drop_choice = int(input("Choose an option: ")) - 1
                                            if drop_choice not in range(0, len(stashes_trim)):
                                                raise ValueError()
                                            else:
                                                drop_opt = {stashes_trim[stash_choice]}
                                                match drop_opt:
                                                    case "Yes":
                                                        run(['git', 'stash', 'drop', drop_opt], f"Dropped stash {drop_opt} from repository.")
                                                        break
                                                    case "No":
                                                        break
                                                    case _:
                                                        raise IndexError
                                        except (ValueError, IndexError):
                                            print("\nInvalid input.")
                                            continue
                                    break
                            except (ValueError, IndexError):
                                print("\nInvalid input.")
                        
                case _:
                    raise IndexError
            print_stashes()
            stashes = subprocess.check_output(['git', 'stash', 'list'], text=True).splitlines()
            stashes_trim = [x.split(":")[0] for x in stashes]
        except (ValueError, IndexError):
            print("\nInvalid input.")

def prompt_select_commit():
    # FALLBACK
    limit = -1
    config_limit = get_commit_limit()
    if (has_valid_config() and config_limit != -1):
        limit = config_limit
    print_commits(limit)
    commits = subprocess.check_output(['git', 'log', '--oneline', '--all', '-n', f"{limit}"], text=True).splitlines()
    hashes = [c[:7] for c in commits]
    if not hashes:
        print(f"\nNo commit hashes found.")
        return
    else:
        options = ["Back to Main Menu"] + hashes
        while True:
            print("\n[Select Commit]")
            for i, commit in enumerate(options):
                print(f"{i+1}. {commit}")
            try:
                choice = int(input("Choose an option: ")) - 1
                if choice not in range(0, len(options)):
                    raise ValueError()
                elif choice == 0:
                    break
                else:
                    commit = options[choice]
                    print(f"\nSelected {commit}")
                    prompt_reset(commit)
                    break
            except (ValueError, IndexError):
                print("\nInvalid input.")

def prompt_reset(commit):
    options = ["Back to Main Menu", "Mixed", "Soft", "Hard", ]
    while True:
        print_options(options, "Reset")
        try:
            choice = int(input("Choose an option: ")) - 1
            match options[choice]:
                case "Back to Main Menu":
                    break
                case "Mixed":
                    print(f"\nMixed reset to commit {commit}? This will keep the working tree but reset index.")
                    prompt_reset_again("--mixed", commit)
                    break
                case "Soft":
                    print(f"\nSoft reset to commit {commit}? This will keep all changes but reset HEAD.")
                    prompt_reset_again("--soft", commit)
                    break
                case "Hard":
                    print(f"\nHard reset to commit {commit}? ALL CHANGES WILL BE DISCARDED!")
                    prompt_reset_again("--hard", commit)
                    break
                case _:
                    raise IndexError
        except (ValueError, IndexError):
            print("\nInvalid input.")

def prompt_reset_again(reset_arg, commit):
    reset_label = ""
    match(reset_arg):
        case "--mixed":
            reset_label = "Mixed"
        case "--soft":
            reset_label = "Soft"
        case "--hard":
            reset_label = "Hard"
    reset_options = ["Yes", "No"]
    while True:
        for i, reset_opt in enumerate(reset_options):
            print(f"{i+1}. {reset_opt}")
        try:
            reset_choice = int(input("Choose an option: ")) - 1
            reset_opt = reset_options[reset_choice]
            if reset_opt == "Yes":
                run(['git', 'reset', reset_arg, commit], f"{reset_label} reset to commit {commit}.")
                # FALLBACK
                limit = -1
                config_limit = get_commit_limit()
                if (has_valid_config and config_limit != -1):
                    limit = config_limit
                print_commits(limit)
                break
            elif reset_opt == "No":
                break
        except (ValueError, IndexError):
            print("\nInvalid input.")
            continue

def prompt_settings():
    options = ["Back to Main Menu", "Browser", "Editor", "Daily Notes", "Commit Limit"]
    while True:
        print_config()
        print_options(options, "Settings")
        try:
            choice = int(input("Choose an option: ")) - 1
            match options[choice]:
                case "Back to Main Menu":
                    break
                case "Browser":
                    new_browser = input("Set new default browser (or pass empty message to cancel): ")
                    if new_browser:
                        set_app(new_browser, "browser")
                    else:
                        print(f"\nCanceled. Keep current browser: '{get_browser()}'")
                case "Editor":
                    new_editor = input("Set new default editor (or pass empty message to cancel): ")
                    if new_editor:
                        set_app(new_editor, "editor")
                    else:
                        print(f"\nCanceled. Keep current editor: '{get_editor()}'")
                case "Daily Notes":
                    dn_options = ["Back to Settings", "Enable", "Disable", "Path"]
                    while True:
                        print("\n[Daily Notes]")
                        for i, dn_opt in enumerate(dn_options):
                            print(f"{i+1}. {dn_opt}")
                        try:
                            dn_choice = int(input("Choose an option: ")) - 1
                            match dn_options[dn_choice]:
                                case "Back to Settings":
                                    break
                                case "Enable":
                                    set_daily_notes_status("on")
                                case "Disable":
                                    set_daily_notes_status("off")
                                case "Path":
                                    new_path = input("Set new Daily Notes path (or pass empty message to cancel): ")
                                    if new_path:
                                        create_new_directory(new_path)
                                    else:
                                        print(f"\nCanceled. Keep current path: '{current_path}'")  
                                case _:
                                    raise IndexError
                        except (ValueError, IndexError):
                            print("\nInvalid input.")
                            continue
                case "Commit Limit":
                    prompt_set_commit_limit()
                case _:
                    raise IndexError
        except (ValueError, IndexError):
            print("\nInvalid input.")

if __name__ == "__main__":
    main()
