import configparser  
import subprocess
import os
import sys
from datetime import datetime

__parser = configparser.ConfigParser()

def read_config(fpath):
    try:
        with open(fpath, 'r', encoding="utf-8") as file:
            __parser.read("config.ini")
    except FileNotFoundError:
        print(f"\nConfig file '{fpath}' not found!") 
        print(f"Ensure this script and '{fpath}' are both placed in your Git project's root directory.")
    except Exception as e:
        print(f"\nError while reading config file {fpath}: {e}")

def save_config(message):
    try:
        with open("config.ini", "w", encoding="utf-8") as newfile:
            __parser.write(newfile)
        print(f"\n{message}")
    except Exception as e:
        print(f"\nError while saving to config file {newfile}: {e}")

def main():
    read_config("config.ini")

    version_num = "0.8.3"
    parser_desc = "Settings are defined in 'config.ini'. See 'README.md' for a template config file."
    options_desc = "Options: [-h | --help | -H] [-o | --options | -O] [-v | --version | -V]"
    usage_desc = f"Usage: python3 | py {os.path.basename(__file__)} [-OPTION]"

    # Launch arguments
    while len(sys.argv) > 1:
        option = sys.argv[1]
        if option in ("-h", "--help", "-H"):
            print(parser_desc)
            print(usage_desc)
            print(options_desc)
        elif option in ("-o", "--options", "-O"):
            print_config()
        elif option in ("-v", "--version", "-V"):
            print(version_desc)
        else:
            print(f"\nUnknown Option: {option}")
            print(usage_desc)
            print(options_desc)
        sys.exit(1)
        sys.argv.pop(1)

    # Post-options flow
    print("------------------------------------")
    print(f"GitLite {version_num}")
    print("Author: Tom Scott (tmscott88)")
    print("\nhttps://github.com/tmscott88/GitLite")
    print("------------------------------------")
        
    print_stashes()
    print_changes()
    main_menu()

# Parser getters
def get_browser():
    return __parser.get('DEFAULT', 'browser')

def get_editor():
    return __parser.get('DEFAULT', 'editor')

def get_commit_limit():
    return __parser.get('DEFAULT', 'commit_limit')

def get_daily_notes_status():
    return __parser.get('DAILY_NOTES', 'status')

def get_daily_notes_dir():
    return __parser.get('DAILY_NOTES', 'path')

def set_browser(new_browser):
    try:
        subprocess.run(["which", new_browser], check=True, capture_output=True)
        __parser.set('DEFAULT', 'browser', new_browser)
        save_config(f"Updated browser: {new_browser}")
    except subprocess.CalledProcessError:
        print(f"\nBrowser '{new_browser}' not found on system. Cannot update browser setting.")
    except Exception as e:
        print(f"\nError while setting browser '{new_browser}'. {e}")

def set_editor(new_editor):
    try:
        subprocess.run(["which", new_editor], check=True, capture_output=True)
        __parser.set('DEFAULT', 'editor', new_editor)
        save_config(f"Updated editor: {new_editor}")
    except subprocess.CalledProcessError:
        print(f"\nEditor '{new_editor}' not found on system. Cannot update editor setting.")
    except Exception as e:
        print(f"\nError while setting editor '{new_editor}'. {e}")
    

def set_commit_limit(new_limit):
    limit = int(new_limit)
    if (limit < 1):
        print("\nLimit must be a positive integer")
        return
    else:
        try:
            __parser.set('DEFAULT', 'commit_limit', new_limit)
            save_config(f"Updated commit limit: {new_limit}")
        except Exception as e:
            print(f"\nError while setting commit limit {new_limit}. {e}")

def set_daily_notes_status(new_status):
    if (new_status == "true" or new_status == "false"):
        __parser.set('DAILY_NOTES', 'status', new_status)
        save_config(f"Daily Notes: {new_status}")
    else:
        print(f"\nUnexpected status {new_status}. Status must be 'true' or 'false'.")

def set_daily_notes_path(new_path):
    __parser.set('DAILY_NOTES', 'path', new_path)
    save_config(f"\nUpdated daily notes path: {new_path}")

def is_existing_path(dir):
    return bool(os.path.isdir(dir) or os.path.isfile(dir))

def prompt_new_directory(dir):
    print(f"\nDirectory '{dir}' not found. Create a new directory at this location?")
    options = ["Yes", "No"]
    while True:
        for i, opt in enumerate(options):
            print(f"{i+1}. {opt}")
        try:
            choice = int(input("Choose an option: ")) - 1
            opt = options[choice]
            if opt == "Yes":
                os.makedirs(dir)
            elif opt == "No":
                break
        except (ValueError, IndexError):
            print("\nInvalid input.")
            continue
        except subprocess.CalledProcessError as e:
            print(f"\nError creating directory '{dir}'. {e}")
            break


# HELPER FUNCTIONS
def file_has_changes(fpath):
    script_status = subprocess.getoutput(f"git status {fpath} --short")
    return bool(script_status)

def repo_has_changes():
    changes = subprocess.getoutput("git status --porcelain")
    return bool(changes)

def repo_has_staged_changes():
    staged = subprocess.getoutput("git diff --name-status --cached")
    return bool(staged)

def repo_has_stashes():
    stashes = subprocess.getoutput("git stash list")
    return bool(stashes)

def is_daily_notes_enabled():
    enabled = get_daily_notes_status()
    return bool(enabled == "true")

def print_config():
    print("\n[config.ini]")
    print(f"* Browser: {get_browser()}")
    print(f"* Editor: {get_editor()}")
    print(f"* Daily Notes: {get_daily_notes_status()}")
    print(f"* Daily Notes Location: {get_daily_notes_dir()}")
    print(f"* Commit Display Limit: {get_commit_limit()}")

def print_changes():
    if repo_has_changes():
        print("\n[Changes]")
        git("status -s -u")

def print_stashes():
    if repo_has_stashes():
        print("\n[Stashes]")
        git("stash list")

def print_options(options, title):
    print(f"\n[{title}]")
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")

def open_editor(fpath):
    editor = get_editor()
    try:
        subprocess.run(f"{editor} {fpath}", shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"\nCould not open editor '{editor}'. Ensure that the editor is defined correctly in 'config.ini' and added to PATH.")

def open_daily_note(fpath):
    daily_notes_dir = get_daily_notes_dir()
    open_editor(f"{daily_notes_dir}/{fpath}")

def open_browser():
    browser = get_browser()
    try:
        subprocess.run(browser, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"\nCould not open browser '{browser}'. Ensure that the browser is defined correctly in 'config.ini' and added to PATH.")

def git(command):
    try:
        subprocess.run(f"git {command}", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nCould not run Git operation. {e}")    
        
def main_menu():
    options = []
    if file_has_changes(__file__):
        options = ["Start", "Status", "Log", "Diff", "Pull", "Push", "Stage", "Commit", "Revert", "Discard", "Reset", "Settings", "Quit"]
    else:
        options = ["Start", "Status", "Log", "Diff", "Pull", "Push", "Stage", "Commit", "Stash", "Revert", "Discard", "Reset", "Settings", "Quit"]
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
                        print("\n[Remote]") 
                        git("fetch")
                        git("status")
                    case "Log":
                        prompt_log()
                    case "Diff":
                        if not subprocess.getoutput("git diff"):
                            print("\nNo tracked changes to analyze.")
                        else:
                            git("diff")
                    case "Pull":
                        git("pull")
                    case "Push":
                        git("push")
                    case "Stage":
                        prompt_stage()
                    case "Commit":
                        if not repo_has_staged_changes():
                            print("\nNo changes staged for commit. Please stage changes before committing.")
                        else:
                            prompt_commit()
                    case "Stash":
                        print("\nStash menu coming soon.")
                        # if file_has_changes(__file__):
                        #     print("\nCannot safely stash because this script has been modified. Please commit this script first.")
                        #     continue
                        # if not (repo_has_changes() or repo_has_stashes()):
                        #     print("\nNo changes to stash. No stashes to apply. Cannot proceed.")
                        # elif repo_has_changes() and not repo_has_stashes():
                        #     print("\nNo stashes found. Create a stash?")
                        #     prompt_create_stash()
                        # else:
                        #     prompt_stash_menu()
                    case "Revert":
                        git("checkout -p")
                    case "Discard":
                        if not subprocess.getoutput("git ls-files --others --exclude-standard"):
                            print("\nNo untracked changes to discard.")
                        else:
                            git("clean -i -d")
                    case "Reset":
                        prompt_select_commit()
                    case "Settings":
                        prompt_settings()
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
    options = []
    if is_daily_notes_enabled():
        options = ["Back to Main Menu", "New", "Resume", "Browse", "Open Daily Note"]
    else:
        options = ["Back to Main Menu", "New", "Resume", "Browse"]
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
                    case "New":
                        open_editor("")
                    case "Resume":
                        prompt_resume()
                    case "Browse":
                        open_browser()
                    case "Open Daily Note":
                        if not is_daily_notes_enabled():
                            print("\nDaily Notes disabled. See Main Menu -> Settings to enable this feature.")
                        else:
                            root = get_daily_notes_dir()
                            # root/YYYY-MM
                            date_path = f"{root}/{datetime.year}/{datetime.now().strftime('%Y-%m')}"
                            # root/YYYY-MM/YYYY-MM-DD.md
                            note_path = f"{date_path}/{datetime.now().strftime('%F')}.md"
                            # if file already exists, open in editor
                            if is_existing_path(note_path):
                                open_editor(note_path)
                            else:
                                try:
                                    # if folder path doesn't exist, prompt
                                    if not is_existing_path(date_path):
                                        prompt_new_directory(date_path)
                                        # Only create new daily note if prompt completed successfully
                                        if is_existing_path(note_path):
                                            subprocess.run(["touch", note_path], check=True, capture_output=True)
                                        else:
                                            print(f"\nCancelled daily note creation.")
                                            break
                                    open_editor(note_path)
                                except subprocess.CalledProcessError as e:
                                    print(f"\nError while creating new daily note: {e}")
                    case _:
                        raise IndexError()
        except (ValueError, IndexError):
            print("\nInvalid input.")

def prompt_resume():
    files = subprocess.getoutput("git status -s -u | cut -c4-").splitlines()
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
    options = ["Back to Main Menu", "Standard", "Simple", "Verbose"]
    limit = get_commit_limit()
    while True:
        print_options(options, "Log")
        try:
            choice = int(input("Choose an option: ")) - 1
            if choice not in range (0, len(options)):
                raise ValueError()
            else:
                match options[choice]:
                    case "Back to Main Menu":
                        break
                    case "Standard":
                        git(f"log --name-status --all -n {limit}")
                        break
                    case "Simple":
                        git(f"log --oneline --all -n {limit}")
                        break
                    case "Verbose":
                        git(f"log --oneline -p -n {limit}")
                        break
                    case _:
                        raise IndexError()
        except (ValueError, IndexError):
            print("\nInvalid input.")

def prompt_commit():
    message = input("Enter commit message (or pass empty message to cancel): ")
    if message:
        git(f'commit -m "{message}"') 
    else:
        print("\nCanceled commit.")

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
                    git("add -A")
                    print("\nStaged all changes.")
                case "Unstage-All":
                    git("restore --staged .")
                    print("\nUnstaged all changes.")
                case "Stage-Interactive":
                    git("add -i")
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
                        git(f"stash push -u -m '{message}'")
                    else:
                        print("\nCanceled stash.")
                    break
                case "Stash Staged":
                    message = input("Enter stash message (or pass empty message to cancel): ")
                    if message:
                        git(f"stash push --staged -m '{message}'")
                    break
                case _:
                    IndexError
        except (ValueError, IndexError):
            print("\nInvalid input.")

def prompt_stash_menu():
    back_stash_menu = "Back to Stash Menu"
    stashes = subprocess.getoutput("git stash list").splitlines()
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
                        print("There are no stashes in this repository.")
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
                                    git(f"stash apply {stash}")
                                    break
                            except (ValueError, IndexError):
                                print("\nInvalid input.")
                                continue
                case "Pop Stash":
                    if not repo_has_stashes():
                        print("There are no stashes in this repository.")
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
                                    git(f"stash pop {stash}")
                                    break
                            except (ValueError, IndexError):
                                print("\nInvalid input.")
                                continue
                case "Drop Stash":
                    if not repo_has_stashes():
                        print("There are no stashes in this repository.")
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
                                                        git(f"stash drop {drop_opt}")
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
            stashes = subprocess.getoutput("git stash list").splitlines()
            stashes_trim = [x.split(":")[0] for x in stashes]
        except (ValueError, IndexError):
            print("\nInvalid input.")

def prompt_select_commit():
    limit = get_commit_limit()
    print("\n[Commits]")
    git(f"log --oneline --all -n {limit}")
    commits = subprocess.getoutput(f"git log --oneline --all -n {limit} | cut -c -7").splitlines()
    if not commits:
        return
    else:
        options = ["Back to Main Menu"] + commits
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
                    git(f"reset --mixed {commit}")
                    break
                case "Soft":
                    git(f"reset --soft {commit}")
                    break
                case "Hard":
                    print(f"\nHard reset to commit {commit}? ALL CHANGES WILL BE DISCARDED!")
                    hard_reset_options = ["Yes", "No"]
                    while True:
                        for i, hard_opt in enumerate(hard_reset_options):
                            print(f"{i+1}. {hard_opt}")
                        try:
                            reset_choice = int(input("Choose an option: ")) - 1
                            hard_opt = hard_reset_options[reset_choice]
                            if hard_opt == "Yes":
                                git(f"reset --hard {commit}")
                                break
                            elif hard_opt == "No":
                                break
                        except (ValueError, IndexError):
                            print("\nInvalid input.")
                            continue
                    break
                case _:
                    raise IndexError
        except (ValueError, IndexError):
            print("\nInvalid input.")

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
                    current_browser = get_browser()
                    new_browser = input("Set new default browser (or pass empty message to cancel): ")
                    if new_browser:
                        set_browser(new_browser)
                    else:
                        print(f"\nBrowser kept at: {current_browser}")
                case "Editor":
                    current_editor = get_editor()
                    new_editor = input("Set new default editor (or pass empty message to cancel): ")
                    if new_editor:
                        set_editor(new_editor)
                    else:
                        print(f"\nEditor kept at: {current_editor}")
                case "Daily Notes":
                    dn_options = ["Back to Settings", "Enable", "Disable", "Format"]
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
                                    set_daily_notes_status("true")
                                case "Disable":
                                    set_daily_notes_status("false")
                                case "Format":
                                    current_path = get_daily_notes_dir()
                                    new_path = input("Set new daily notes path (or pass empty message to cancel): ")
                                    if current_path.capitalize() == new_path.capitalize():
                                        print(f"\nPath reference '{new_path}' matches current path '{current_path}'. No change necessary.")
                                    elif new_path and not is_existing_path(new_path):
                                        prompt_new_directory(new_path)
                                        # Only proceed to set path if directory was created properly
                                        if is_existing_path(new_path):
                                            set_daily_notes_path(new_path)
                                        else:
                                            print(f"\nDid not set new path. Keep path at: {current_path}")
                                    else:
                                        print(f"\nDaily notes path kept at: {current_path}")  
                                case _:
                                    raise IndexError
                        except (ValueError, IndexError):
                            print("\nInvalid input.")
                            continue
                case "Commit Limit":
                    current_limit = get_commit_limit()
                    new_limit = input("Set new commit display limit (or pass empty message to cancel): ")
                    if new_limit:
                        set_commit_limit(new_limit)
                    else:
                        print(f"\nCommit display limit kept at: {current_limit}")
                case _:
                    raise IndexError
        except (ValueError, IndexError):
            print("\nInvalid input.")

if __name__ == "__main__":
    main()
