import subprocess
import sys
from datetime import datetime

# GLOBAL VARIABLES

DEFAULT_EDITOR = "micro"  # micro automatically creates subfolders if they don't exist in the specified path.
DEFAULT_BROWSER = "glow"
DAILY_NOTES_PATH = "DIARY"  # Default format: DAILY_NOTES_PATH/YYYY-MM/YYYY-MM-DD.md

FALLBACK_EDITOR = "nano"
FALLBACK_BROWSER = "rucola"

def main():
    # Handle options
    while len(sys.argv) > 1:
        option = sys.argv[1]
        if option in ("-h", "--help", "-H"):
            print("Usage: ./start.sh [OPTION]")
            print("Options: [-h | --help | -H] [-v | --version | -V]")
        elif option in ("-v", "--version", "-V"):
            print("GitLite 0.8.0")
            print("Author: Tom Scott (tmscott88)")
            print(f"Commit Hash: {subprocess.getoutput('git log --oneline -n 1 | cut -c -7')}")
            print(f"Compiled: {subprocess.getoutput('git show -s --format=\"%cD\" | cut -d \"-\" -f 1')}")
        else:
            print(f"Unknown Option: {option}")
            print("Usage: ./start.sh [-OPTION]")
            print("Options: [-h | --help | -H] [-v | --version | -V]")
        sys.exit(1)
        sys.argv.pop(1)

    # Post-options flow
    print_stashes()
    print_changes()
    prompt_main()

# HELPER FUNCTIONS

def get_script_changes():
    script_status = subprocess.getoutput("git status start.sh --short")
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
        subprocess.call("git status --short", shell=True)
        print("-------------")

def print_stashes():
    if get_stashes():
        print("\n---Stashes---")
        subprocess.call("git stash list", shell=True)
        print("-------------")

def prompt_main():
    options = ["Start", "Fetch", "Log", "Diff", "Pull", "Push", "Stage", "Commit", "Stash", "Revert", "Discard", "Reset", "Quit"]
    while True:
        print("\nChoose an option:")
        for i, opt in enumerate(options):
            print(f"{i+1}. {opt}")
        try:
            choice = int(input()) - 1
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
                prompt_stage()
            else:
                prompt_commit()
        elif opt == "Stash":
            script_status = subprocess.getoutput("git status start.sh --short")
            if not (get_changes() or get_stashes()):
                print("\nNo changes to stash. No stashes to apply. Cannot proceed.")
            elif get_changes() and not get_stashes():
                print("\nNo stashes found. Create a stash?")
                prompt_stash_full()
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
        print("\nChoose an option:")
        for i, opt in enumerate(options):
            print(f"{i+1}. {opt}")
        try:
            choice = int(input()) - 1
            opt = options[choice]
        except (ValueError, IndexError):
            print("Invalid choice")
            continue

        if opt == "New":
            try:
                subprocess.call(DEFAULT_EDITOR, shell=True)
            except:
                subprocess.call(FALLBACK_EDITOR, shell=True)
        elif opt == "Resume":
            prompt_resume()
        elif opt == "Browse":
            try:
                subprocess.call(DEFAULT_BROWSER, shell=True)
            except:
                subprocess.call(FALLBACK_BROWSER, shell=True)
        elif opt == "Daily-Note":
            path = f"{DAILY_NOTES_PATH}/{datetime.now().strftime('%Y-%m')}/{datetime.now().strftime('%F')}.md"
            try:
                subprocess.call(f"{DEFAULT_EDITOR} {path}", shell=True)
            except:
                subprocess.call(f"{FALLBACK_EDITOR} {path}", shell=True)
        elif opt == "Cancel":
            break
        else:
            print("Invalid choice")

def prompt_resume():
    files = subprocess.getoutput("git status -s | cut -c4-").splitlines()
    if not files:
        return
    else:
        options = files + ["Cancel"]
        print("\nChoose an option:")
        for i, file in enumerate(options):
            print(f"{i+1}. {file}")
        while True:
            try:
                choice = int(input()) - 1
                file = options[choice]
                if choice == len(files):
                    break
                elif choice >= 0 and choice < len(files):
                    try:
                        subprocess.call(f"{DEFAULT_EDITOR} {file}", shell=True)
                    except:
                        subprocess.call(f"{FALLBACK_EDITOR} {file}", shell=True)
                    break
                else:
                    print("Invalid choice")
            except (ValueError, IndexError):
                print("Invalid choice")

def prompt_log():
    options = ["Standard", "Simple", "Verbose", "Cancel"]
    print("\nChoose an option:")
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")
    while True:
        try:
            choice = int(input()) - 1
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
    print("\nChoose an option:")
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")
    while True:
        try:
            choice = int(input()) - 1
            opt = options[choice]
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
        except (ValueError, IndexError):
            print("Invalid choice")

def prompt_stash_create():
    print("\nNOTE: Patch mode does not include untracked files.")
    options = ["All", "Patch", "No"]
    print("\nChoose an option:")
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")
    while True:
        try:
            choice = int(input()) - 1
            opt = options[choice]
            if opt == "All":
                message = input("Enter stash message (or pass empty message to cancel): ")
                if message:
                    subprocess.call(f"git stash push -u -m '{message}'", shell=True)
                else:
                    print("\nCanceled stash.")
                break
            elif opt == "Patch":
                subprocess.call("git stash -p", shell=True)
                break
            elif opt == "No":
                break
            else:
                print("Invalid choice.")
        except (ValueError, IndexError):
            print("Invalid choice")

def prompt_stash_full():
    stashes = subprocess.getoutput("git stash list").splitlines()
    stashes_trim = [x.split(":")[0] for x in stashes]
    print_stashes()
    options = ["Create", "Apply", "Pop", "Drop", "Cancel"]
    print("\nChoose an option:")
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")
    while True:
        try:
            choice = int(input()) - 1
            opt = options[choice]
            if opt == "Create":
                if not get_changes():
                    print("There are no changes to stash.")
                else:
                    prompt_stash_create()
                break
            elif opt == "Apply":
                if not get_stashes():
                    print("There are no stashes in this repository.")
                else:
                    print("Note: This will apply the stored copy of the stash and preserve it in the local tree.")
                    print("\nChoose an option:")
                    for i, stash in enumerate(stashes_trim + ["Cancel"]):
                        print(f"{i+1}. {stash}")
                    while True:
                        try:
                            stash_choice = int(input()) - 1
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
            elif opt == "Pop":
                if not get_stashes():
                    print("There are no stashes in this repository.")
                else:
                    print("Note: This will apply the stored copy of the selected stash and remove it from the local tree.")
                    print("\nChoose an option:")
                    for i, stash in enumerate(stashes_trim + ["Cancel"]):
                        print(f"{i+1}. {stash}")
                    while True:
                        try:
                            stash_choice = int(input()) - 1
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
            elif opt == "Drop":
                if not get_stashes():
                    print("There are no stashes in this repository.")
                else:
                    print("Note: This will drop the stored copy of the selected stash.")
                    print("\nChoose an option:")
                    for i, stash in enumerate(stashes_trim + ["Cancel"]):
                        print(f"{i+1}. {stash}")
                    while True:
                        try:
                            stash_choice = int(input()) - 1
                            if stash_choice == len(stashes_trim):
                                break
                            elif stash_choice >= 0 and stash_choice < len(stashes_trim):
                                print(f"Drop stash {stashes_trim[stash_choice]}? THIS STASH WILL BE DISCARDED!")
                                drop_confirm_options = ["Yes", "No"]
                                print("\nChoose an option:")
                                for i, opt in enumerate(drop_confirm_options):
                                    print(f"{i+1}. {opt}")
                                while True:
                                    try:
                                        drop_choice = int(input()) - 1
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
        print("\nChoose an option:")
        for i, commit in enumerate(options):
            print(f"{i+1}. {commit}")
        while True:
            try:
                choice = int(input()) - 1
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
    print("\nChoose an option:")
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")
    while True:
        try:
            choice = int(input()) - 1
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
                print("\nChoose an option:")
                for i, hard_opt in enumerate(hard_reset_options):
                    print(f"{i+1}. {hard_opt}")
                while True:
                    try:
                        reset_choice = int(input()) - 1
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