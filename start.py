import configparser
import subprocess
import sys
from datetime import datetime

def main():
    # Initialize config file and read values
    config = configparser.ConfigParser()
    config.read('config.ini')
    browser = config.get('DEFAULT', 'browser')
    editor = config.get('DEFAULT', 'editor')
    # Default format: daily_notes_path/YYYY-MM/YYYY-MM-DD.md
    daily_notes_path = config.get('DEFAULT', 'daily_notes_path')

    # Handle options
    while len(sys.argv) > 1:
        option = sys.argv[1]
        version = config.get('PROGRAM', 'version')
        config_desc = "Options are specified in 'config.ini'"
        options_desc = "Options: [-h | --help | -H] [-o | --options | -O] [-v | --version | -V]"
        usage_desc = "Usage: python3 start.py [-OPTION]"

        if option in ("-h", "--help", "-H"):
            print(config_desc)
            print(usage_desc)
            print(options_desc)
        elif option in ("-o", "--options", "-O"):
            print(f'Browser: {browser}')
            print(f'Editor: {editor}')
            print(f'Daily Notes Path: {daily_notes_path}')
        elif option in ("-v", "--version", "-V"):
            print(f"GitLite {version}")
        else:
            print(f"Unknown Option: {option}")
            print(usage_desc)
            print(options_desc)
        sys.exit(1)
        sys.argv.pop(1)

    # Post-options flow
    print_stashes()
    print_changes()
    prompt_main()

# HELPER FUNCTIONS

def script_is_committed():
    script_status = subprocess.getoutput("git status __file__ --short")
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

def print_changes():
    if get_changes():
        print("\n---Changes---")
        subprocess.call("git status -s -u", shell=True)
        print("-------------")

def print_stashes():
    if get_stashes():
        print("\n---Stashes---")
        subprocess.call("git stash list", shell=True)
        print("-------------")

def prompt_main():
    options = ["Start", "Fetch", "Log", "Diff", "Pull", "Push", "Stage", "Commit", "Stash", "Revert", "Discard", "Reset", "Quit"]
    while True:
        for i, opt in enumerate(options):
            print(f"{i+1}. {opt}")
        try:
            choice = int(input("Choose an option: ")) - 1
            opt = options[choice]
        except (ValueError, IndexError):
            print("Invalid choice.")
            continue

        if opt == "Start":
            prompt_start()
        elif opt == "Fetch":
            subprocess.call("git fetch", shell=True)
            subprocess.call("git status", shell=True)
        elif opt == "Log":
            prompt_log()
        elif opt == "Diff":
            if not subprocess.getoutput("git diff"):
                print("\nNo tracked changes to analyze.")
            else:
                subprocess.call("git diff", shell=True)
        elif opt == "Pull":
            subprocess.call("git pull", shell=True)
        elif opt == "Push":
            subprocess.call("git push", shell=True)
        elif opt == "Stage":
            prompt_stage()
        elif opt == "Commit":
            if not get_staged_changes():
                print("\nNo changes staged for commit. Please stage changes before committing.")
            else:
                prompt_commit()
        elif opt == "Stash":
            if not script_is_committed():
                print("Cannot safely stash because this script has been modified. Please commit this script first.")
                continue
            if not (get_changes() or get_stashes()):
                print("\nNo changes to stash. No stashes to apply. Cannot proceed.")
            elif get_changes() and not get_stashes():
                print("\nNo stashes found. Create a stash?")
                prompt_stash_create()
            else:
                prompt_stash_full()
        elif opt == "Revert":
            subprocess.call("git checkout -p", shell=True)
        elif opt == "Discard":
            if not subprocess.getoutput("git ls-files --others --exclude-standard"):
                print("\nNo untracked changes to discard.")
            else:
                subprocess.call("git clean -i -d", shell=True)
        elif opt == "Reset":
            prompt_select_commit()
        elif opt == "Quit":
            sys.exit(1)

        print_stashes()
        print_changes()

# PROMPT FUNCTIONS

def prompt_start():
    options = ["New", "Resume", "Browse", "Daily-Note", "Cancel"]
    while True:
        for i, opt in enumerate(options):
            print(f"{i+1}. {opt}")
        try:
            choice = int(input("Choose an option: ")) - 1
            opt = options[choice]
        except (ValueError, IndexError):
            print("Invalid choice")
            continue
        if opt == "New":
            subprocess.call(editor, shell=True)
        elif opt == "Resume":
            prompt_resume()
        elif opt == "Browse":
            subprocess.call(browser, shell=True)
        elif opt == "Daily-Note":
            path = f"{daily_notes_path}/{datetime.now().strftime('%Y-%m')}/{datetime.now().strftime('%F')}.md"
            subprocess.call(f"{editor} {path}", shell=True)
        elif opt == "Cancel":
            break
        else:
            print("Invalid choice")

def prompt_resume():
    files = subprocess.getoutput("git status -s -u | cut -c4-").splitlines()
    if not files:
        return
    else:
        options = files + ["Cancel"]
        for i, file in enumerate(options):
            print(f"{i+1}. {file}")
        while True:
            try:
                choice = int(input("Choose an option: ")) - 1
                file = options[choice]
                if choice == len(files):
                    break
                elif choice >= 0 and choice < len(files):
                    subprocess.call(f"{editor} {file}", shell=True)
                    break
                else:
                    print("Invalid choice")
            except (ValueError, IndexError):
                print("Invalid choice")

def prompt_log():
    options = ["Standard", "Simple", "Verbose", "Cancel"]
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")
    while True:
        try:
            choice = int(input("Choose an option: ")) - 1
            opt = options[choice]
            if opt == "Standard":
                subprocess.call("git log --name-status --all", shell=True)
                break
            elif opt == "Simple":
                subprocess.call("git log --oneline --all", shell=True)
                break
            elif opt == "Verbose":
                subprocess.call("git log -p --oneline", shell=True)
                break
            elif opt == "Cancel":
                break
            else:
                print("Invalid choice")
        except (ValueError, IndexError):
            print("Invalid choice")

def prompt_commit():
    message = input("Enter commit message (or pass empty message to cancel): ")
    if message:
        subprocess.call(f"git commit -m '{message}'", shell=True)
    else:
        print("\nCanceled commit.")

def prompt_stage():
    options = ["Stage-All", "Unstage-All", "Stage-Interactive", "Cancel"]
    while True:
        for i, opt in enumerate(options):
            print(f"{i+1}. {opt}")
        try:
            choice = int(input("Choose an option: ")) - 1
            opt = options[choice]
        except (ValueError, IndexError):
            print("Invalid choice")
            continue
        if opt == "Stage-All":
            subprocess.call("git add -A", shell=True)
            print("\nStaged all changes.")
        elif opt == "Unstage-All":
            subprocess.call("git restore --staged .", shell=True)
            print("\nUnstaged all changes.")
        elif opt == "Stage-Interactive":
            subprocess.call("git add -i", shell=True)
        elif opt == "Cancel":
            break
        else:
            print("Invalid choice.")

        print_changes()

def prompt_stash_create():
    print("\nNOTE: Patch mode does not include untracked files.")
    options = ["Stash All", "Stash Staged", "Cancel"]
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")
    while True:
        try:
            choice = int(input("Choose an option: ")) - 1
            opt = options[choice]
            if opt == "Stash All":
                message = input("Enter stash message (or pass empty message to cancel): ")
                if message:
                    subprocess.call(f"git stash push -u -m '{message}'", shell=True)
                else:
                    print("\nCanceled stash.")
                break
            elif opt == "Stash Staged":
                message = input("Enter stash message (or pass empty message to cancel): ")
                if message:
                    subprocess.call("git stash push --staged -m '{message}'", shell=True)
                break
            elif opt == "Cancel":
                break
            else:
                print("Invalid choice.")
        except (ValueError, IndexError):
            print("Invalid choice")

def prompt_stash_full():
    stashes = subprocess.getoutput("git stash list").splitlines()
    stashes_trim = [x.split(":")[0] for x in stashes]
    print_stashes()
    options = ["Create Stash", "Apply Stash", "Pop Stash", "Drop Stash", "Cancel"]
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")
    while True:
        try:
            choice = int(input("Choose an option: ")) - 1
            opt = options[choice]
            if opt == "Create Stash":
                if not get_changes():
                    print("There are no changes to stash.")
                else:
                    prompt_stash_create()
                break
            elif opt == "Apply Stash":
                if not get_stashes():
                    print("There are no stashes in this repository.")
                else:
                    print("Note: This will apply the stored copy of the stash and preserve it in the local tree.")
                    for i, stash in enumerate(stashes_trim + ["Cancel"]):
                        print(f"{i+1}. {stash}")
                    while True:
                        try:
                            stash_choice = int(input("Choose an option: ")) - 1
                            stash = stashes_trim[stash_choice]
                            if stash_choice == len(stashes_trim):
                                break
                            elif stash_choice >= 0 and stash_choice < len(stashes_trim):
                                subprocess.call(f"git stash apply {stash}", shell=True)
                                break
                            else:
                                print("Invalid choice.")
                        except (ValueError, IndexError):
                            print("Invalid choice.")
                break
            elif opt == "Pop Stash":
                if not get_stashes():
                    print("There are no stashes in this repository.")
                else:
                    print("Note: This will apply the stored copy of the selected stash and remove it from the local tree.")
                    for i, stash in enumerate(stashes_trim + ["Cancel"]):
                        print(f"{i+1}. {stash}")
                    while True:
                        try:
                            stash_choice = int(input("Choose an option: ")) - 1
                            if stash_choice == len(stashes_trim):
                                break
                            elif stash_choice >= 0 and stash_choice < len(stashes_trim):
                                subprocess.call(f"git stash pop {stashes_trim[stash_choice]}", shell=True)
                                break
                            else:
                                print("Invalid choice.")
                        except (ValueError, IndexError):
                            print("Invalid choice.")
                break
            elif opt == "Drop Stash":
                if not get_stashes():
                    print("There are no stashes in this repository.")
                else:
                    print("Note: This will drop the stored copy of the selected stash.")
                    for i, stash in enumerate(stashes_trim + ["Cancel"]):
                        print(f"{i+1}. {stash}")
                    while True:
                        try:
                            stash_choice = int(input("Choose an option: ")) - 1
                            if stash_choice == len(stashes_trim):
                                break
                            elif stash_choice >= 0 and stash_choice < len(stashes_trim):
                                print(f"Drop stash {stashes_trim[stash_choice]}? THIS STASH WILL BE DISCARDED!")
                                drop_confirm_options = ["Yes", "No"]
                                for i, opt in enumerate(drop_confirm_options):
                                    print(f"{i+1}. {opt}")
                                while True:
                                    try:
                                        drop_choice = int(input("Choose an option: ")) - 1
                                        drop_opt.drop_confirm_options[drop_choice]
                                        if drop_opt == "Yes":
                                            subprocess.call(f"git stash drop {stashes_trim[stash_choice]}", shell=True)
                                            break
                                        elif drop_opt == "No":
                                            break
                                        else:
                                            print("Invalid choice.")
                                    except (ValueError, IndexError):
                                        print("Invalid choice.")
                                break
                            else:
                                print("Invalid choice.")
                        except (ValueError, IndexError):
                            print("Invalid choice.")
                break
            elif opt == "Cancel":
                break
            else:
                print("Invalid choice")
                print_stashes()
                stashes = subprocess.getoutput("git stash list").splitlines()
                stashes_trim = [x.split(":")[0] for x in stashes]
        except (ValueError, IndexError):
            print("Invalid choice.")

def prompt_select_commit():
    print("Select a commit to reset to.")
    subprocess.call("git log --oneline --all -n 10", shell=True)
    commits = subprocess.getoutput("git log --oneline --all -n 10 | cut -c -7").splitlines()
    if not commits:
        return
    else:
        options = commits + ["Cancel"]
        for i, commit in enumerate(options):
            print(f"{i+1}. {commit}")
        while True:
            try:
                choice = int(input("Choose an option: ")) - 1
                commit = options[choice]
                if choice == len(commits):
                    break
                elif choice >= 0 and choice < len(commits):
                    print(f"Selected {commit}")
                    prompt_reset(commit)
                    break
                else:
                    print("Invalid choice")
            except (ValueError, IndexError):
                print("Invalid choice")

def prompt_reset(commit):
    options = ["Mixed", "Soft", "Hard", "Cancel"]
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")
    while True:
        try:
            choice = int(input("Choose an option: ")) - 1
            opt = options[choice]
            if opt == "Mixed":
                subprocess.call(f"git reset --mixed {commit}", shell=True)
                break
            elif opt == "Soft":
                subprocess.call(f"git reset --soft {commit}", shell=True)
                break
            elif opt == "Hard":
                print(f"Hard reset to commit {commit}? ALL CHANGES WILL BE DISCARDED!")
                hard_reset_options = ["Yes", "No"]
                for i, hard_opt in enumerate(hard_reset_options):
                    print(f"{i+1}. {hard_opt}")
                while True:
                    try:
                        reset_choice = int(input("Choose an option: ")) - 1
                        hard_opt = hard_reset_options[reset_choice]
                        if hard_ == "Yes":
                            subprocess.call(f"git reset --hard {commit}", shell=True)
                            break
                        elif hard_opt == "No":
                            break
                        else:
                            print("Invalid choice.")
                    except (ValueError, IndexError):
                        print("Invalid choice.")
                break
            elif opt == "Cancel":
                break
            else:
                print("Invalid choice")
        except (ValueError, IndexError):
            print("Invalid choice")

if __name__ == "__main__":
    main()
