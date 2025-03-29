import configparser  
import subprocess
import sys
from datetime import datetime

__parser = configparser.ConfigParser()

def main():
    __parser.read("config.ini")

    version_num = "0.8.2"
    version_desc = f"GitLite {version_num}"
    parser_desc = "Settings are defined in 'config.ini'. See 'README.md' for a template config file."
    options_desc = "Options: [-h | --help | -H] [-o | --options | -O] [-v | --version | -V]"
    usage_desc = "Usage: python3 start.py [-OPTION]"

    # Handle options
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
            print(f"Unknown Option: {option}")
            print(usage_desc)
            print(options_desc)
        sys.exit(1)
        sys.argv.pop(1)

    # Post-options flow
    print("-----------------------")
    print(version_desc)
    print("Author: Tom Scott (tmscott88)")
    print("\nhttps://github.com/tmscott88/GitLite")
    print("-----------------------")
        
    print_stashes()
    print_changes()
    main_menu()

# HELPER FUNCTIONS

def file_is_committed(fpath):
    script_status = subprocess.getoutput(f"git status {fpath} --short")
    return bool(script_status)

def get_changes():
    changes = subprocess.getoutput("git status --porcelain")
    return bool(changes)

def get_staged_changes():
    staged = subprocess.getoutput("git diff --name-status --cached")
    return bool(staged)

def get_stashes():
    stashes = subprocess.getoutput("git stash list")
    return bool(stashes)

def print_config():
    print(f"Browser: {__parser.get('DEFAULT', 'browser')}")
    print(f"Editor: {__parser.get('DEFAULT', 'editor')}")
    daily_notes_state = __parser.get('DAILY_NOTES', 'enabled')
    daily_notes_enabled = "Enabled" if daily_notes_state == "true" else "Disabled"
    print(f"Daily Notes: {daily_notes_enabled}")
    if (daily_notes_enabled == "Enabled"):
        print(f"Daily Notes Root Path: {__parser.get('DAILY_NOTES', 'folder')}")

def print_changes():
    if get_changes():
        print("\n---Changes---")
        git("status -s -u")
        print("-------------")

def print_stashes():
    if get_stashes():
        print("\n---Stashes---")
        git("stash list")
        print("-------------")

def print_options(options):
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")

def open_editor(fpath):
    editor = __parser.get('DEFAULT', 'editor')
    try:
        subprocess.run(f"{editor} {fpath}", shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"Verify that the editor is defined correctly in 'config.ini' and added to PATH.")

def open_daily_note(fpath):
    daily_notes_folder = __parser.get('DEFAULT', 'daily_notes_folder')
    open_editor(f"{daily_notes_folder}/{fpath}")

def open_browser():
    browser = __parser.get('DEFAULT', 'browser')
    try:
        subprocess.run(browser, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"Verify that the browser is defined correctly in 'config.ini' and added to PATH.")

def git(command):
    try:
        subprocess.run(f"git {command}", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Could not run Git operation. {e}")    

def save_config(message):
    try:
        with open("config.ini", 'w') as newfile:
            __parser.write(newfile)
        print(message)
    except Exception as e:
        print(f"Error while saving config: {e}")

def main_menu():
    options = ["Start", "Fetch", "Log", "Diff", "Pull", "Push", "Stage", "Commit", "Stash", "Revert", "Discard", "Reset", "Settings", "Quit"]
    while True:
        print_options(options)
        try:
            choice = int(input("Choose an option: ")) - 1
            if choice not in range(0, len(options)):
                raise ValueError()
            else: 
                match options[choice]:
                    case "Start":
                        prompt_start()
                    case "Fetch":
                        git("fetch origin")
                        git("status -b")
                    case "Log":
                        prompt_log()
                    case "Diff":
                        if not subprocess.getoutput("git diff"):
                            print("\nNo tracked changes to analyze.")
                        else:
                            git("diff")
                    case "Pull":
                        git("pull origin")
                    case "Push":
                        git("push origin")
                    case "Stage":
                        prompt_stage()
                    case "Commit":
                        if not get_staged_changes():
                            print("\nNo changes staged for commit. Please stage changes before committing.")
                        else:
                            prompt_commit()
                    case "Stash":
                        # If this script has uncommitted changes, 
                        if not file_is_committed(__file__):
                            print("Cannot safely stash because this script has been modified. Please commit this script first.")
                            continue
                        if not (get_changes() or get_stashes()):
                            print("\nNo changes to stash. No stashes to apply. Cannot proceed.")
                        elif get_changes() and not get_stashes():
                            print("\nNo stashes found. Create a stash?")
                            prompt_create_stash()
                        else:
                            prompt_stash_menu()
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
            print("Invalid choice.")
            continue
        print_stashes()
        print_changes()

# PROMPT FUNCTIONS
def prompt_start():
    options = ["Back to Main Menu", "New", "Resume", "Browse", "Daily-Note"]
    while True:
        print_options(options)
        try:
            choice = int(input("Choose an option: ")) - 1
            if choice not in range(0, len(options)):
                raise ValueError()
            else: 
                match options[choice]:
                    case "Back to Main Menu":
                        break
                    case "New":
                        _open_editor("")
                    case "Resume":
                        prompt_resume()
                    case "Browse":
                        _open_browser()
                    case "Daily-Note":
                        path = f"{datetime.now().strftime('%Y-%m')}/{datetime.now().strftime('%F')}.md"
                        _open_editor(path)
                    case _:
                        raise IndexError()
        except (ValueError, IndexError):
            print("Invalid choice.")
            continue

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
                # Back to main menu
                elif choice == 0:
                    break
                else:
                    file = options[choice]
                    open_editor(file)
                    break
            except (ValueError, IndexError):
                print("Invalid choice.")
                continue

def prompt_log():
    options = ["Back to Main Menu", "Standard", "Simple", "Verbose"]
    while True:
        print_options(options)
        try:
            choice = int(input("Choose an option: ")) - 1
            if choice not in range (0, len(options)):
                raise ValueError()
            else:
                match options[choice]:
                    case "Back to Main Menu":
                        break
                    case "Standard":
                        git("log --name-status --all")
                        break
                    case "Simple":
                        git("log --oneline --all")
                        break
                    case "Verbose":
                        git("log --oneline -p")
                        break
                    case _:
                        raise IndexError
        except (ValueError, IndexError):
            print("Invalid choice.")
            continue

def prompt_commit():
    message = input("Enter commit message (or pass empty message to cancel): ")
    if message:
        git(f'commit -m "{message}"')
        # try:
        #     subprocess.run(f'git commit -m "{message}"', shell=True, check=True)
        # except subprocess.CalledProcessError as e:
        #     print(f"Git commit failed. {e}")   
    else:
        print("\nCanceled commit.")

def prompt_stage():
    options = ["Back to Main Menu", "Stage-All", "Unstage-All", "Stage-Interactive"]
    while True:
        print_options(options)
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
            print("Invalid choice.")
            continue
        print_changes()

def prompt_create_stash():
    print("\nNOTE: Patch mode does not include untracked files.")
    options = ["Go Back", "Stash All", "Stash Staged"]
    while True:
        print_options(options)
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
            print("Invalid choice.")
            continue

def prompt_stash_menu():
    back_stash_menu = "Back to Stash Menu"
    stashes = subprocess.getoutput("git stash list").splitlines()
    stashes_trim = [x.split(":")[0] for x in stashes]
    print_stashes()
    options = ["Back to Main Menu", "Create Stash", "Apply Stash", "Pop Stash", "Drop Stash"]
    while True:
        print_options(options)
        try:
            choice = int(input("Choose an option: ")) - 1
            if choice not in range(0, len(options)):
                raise ValueError()
            match options[choice]:
                case "Back to Main Menu":
                    break
                case "Create Stash":
                    if not get_changes():
                        print("There are no changes to stash.")
                    else:
                        prompt_create_stash()
                    break
                case "Apply Stash":
                    if not get_stashes():
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
                                print("Invalid choice.")
                                continue
                case "Pop Stash":
                    if not get_stashes():
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
                                print("Invalid choice.")
                                continue
                case "Drop Stash":
                    if not get_stashes():
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
                                    print(f"Drop stash {stash}? THIS STASH WILL BE DISCARDED!")
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
                                            print("Invalid choice.")
                                            continue
                                    break
                            except (ValueError, IndexError):
                                print("Invalid choice.")
                                continue
                        
                case _:
                    raise IndexError
            print_stashes()
            stashes = subprocess.getoutput("git stash list").splitlines()
            stashes_trim = [x.split(":")[0] for x in stashes]
        except (ValueError, IndexError):
            print("Invalid choice.")
            continue

def prompt_select_commit():
    print("Select a commit to reset to.")
    subprocess.run("git log --oneline --all -n 10", shell=True)
    commits = subprocess.getoutput("git log --oneline --all -n 10 | cut -c -7").splitlines()
    if not commits:
        return
    else:
        options = ["Back to Main Menu"] + commits
        while True:
            for i, commit in enumerate(options):
                print(f"{i+1}. {commit}")
            try:
                choice = int(input("Choose an option: ")) - 1
                if choice not in range(0, len(options)):
                    raise ValueError()
                # Back to main menu
                elif choice == 0:
                    break
                else:
                    commit = options[choice]
                    print(f"Selected {commit}")
                    prompt_reset(commit)
                    break
            except (ValueError, IndexError):
                print("Invalid choice.")
                continue

def prompt_reset(commit):
    options = ["Back to Main Menu", "Mixed", "Soft", "Hard", ]
    while True:
        print_options(options)
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
                    print(f"Hard reset to commit {commit}? ALL CHANGES WILL BE DISCARDED!")
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
                            print("Invalid choice.")
                            continue
                    break
                case _:
                    raise IndexError
        except (ValueError, IndexError):
            print("Invalid choice.")
            continue

def prompt_settings():
    options = ["Back to Main Menu", "Browser", "Editor", "Daily Notes"]
    while True:
        print_config()
        print_options(options)
        try:
            choice = int(input("Choose an option: ")) - 1
            match options[choice]:
                case "Back to Main Menu":
                    break
                case "Browser":
                    current_browser = __parser.get('DEFAULT', 'browser')
                    new_browser = input("Set new default browser (or pass empty message to continue): ")
                    if new_browser:
                        __parser.set('DEFAULT', 'browser', new_browser)
                        save_config(f"Updated browser: {new_browser}")
                        # test if setting is valid. if not, re-prompt
                    else:
                        print(f"Browser kept as {current_browser}")
                case "Editor":
                    current_editor = __parser.get('DEFAULT', 'editor')
                    new_editor = input("Set new default editor (or pass empty message to continue): ")
                    if new_editor:
                        __parser.set('DEFAULT', 'editor', new_editor)
                        save_config(f"Updated editor: {new_editor}")
                        # test if setting is valid. if not, re-prompt
                    else:
                        print(f"Editor kept as {current_editor}")
                case "Daily Notes":
                    dn_options = ["Back to Settings", "Enable", "Disable", "Location"]
                    while True:
                        for i, dn_opt in enumerate(dn_options):
                            print(f"{i+1}. {dn_opt}")
                        try:
                            dn_choice = int(input("Choose an option: ")) - 1
                            match dn_options[dn_choice]:
                                case "Back to Settings":
                                    break
                                case "Enable":
                                    __parser.set('DAILY_NOTES', 'enabled', 'true')
                                    save_config(f"Enabled daily notes.")
                                case "Disable":
                                    __parser.set('DAILY_NOTES', 'enabled', 'false')
                                    save_config(f"Disabled daily notes.")
                                case "Location":
                                    # Prompt for location
                                    current_root = __parser.get('DAILY_NOTES', 'folder')
                                    new_root = input("Set new default daily notes folder (or pass empty message to continue): ")
                                    if new_root:
                                        __parser.set('DAILY_NOTES', 'folder', new_root)
                                        save_config(f"Updated daily notes folder: {new_root}")
                                        # test if setting is valid. if not, re-prompt
                                    else:
                                        print(f"Daily notes folder kept as: {current_root}")  
                                case _:
                                    raise IndexError
                        except (ValueError, IndexError):
                            print("Invalid choice.")
                            continue
                case _:
                    raise IndexError
        except (ValueError, IndexError):
            print("Invalid choice.")
            continue

if __name__ == "__main__":
    main()
