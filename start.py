import configparser  
import subprocess
import sys
from datetime import datetime
from profile import Profile

config_file = "config.ini"

def main():
    # Initialize config file and read values
    parser = configparser.ConfigParser()
    parser.read(config_file)

    browser = parser.get('DEFAULT', 'browser')
    editor = parser.get('DEFAULT', 'editor')
    daily_notes_path = parser.get('DEFAULT', 'daily_notes_path') # Default format: daily_notes_path/YYYY-MM/YYYY-MM-DD.md
    version = parser.get('PROGRAM', 'version')

    # profile.py
    profile = Profile(browser, editor, daily_notes_path)

    welcome = f"GitLite {version}"
    parser_desc = "App settings are specified in 'config.ini'"
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
            print(f'Browser: {browser}')
            print(f'Editor: {editor}')
            print(f'Daily Notes Path: {daily_notes_path}')
        elif option in ("-v", "--version", "-V"):
            print(welcome)
        else:
            print(f"Unknown Option: {option}")
            print(usage_desc)
            print(options_desc)
        sys.exit(1)
        sys.argv.pop(1)

    # Post-options flow
    print("-------------------")
    print(f"GitLite {version}")
    print(f"Browser: {profile._browser}")
    print(f"Editor: {profile._editor}")
    print(f"Daily Notes Path: {profile._daily_notes_path}")
    print("-------------------")
        
    print_stashes()
    print_changes()
    prompt_main()

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

def print_changes():
    if get_changes():
        print("\n---Changes---")
        run_git_command("status", "-s -u")
        print("-------------")

def print_stashes():
    if get_stashes():
        print("\n---Stashes---")
        run_git_command("stash", "list")
        print("-------------")

def open_editor(fpath):
    editor = parser.get('DEFAULT', 'editor')
    try:
        subprocess.run(f"{editor} {fpath}", shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"Verify that the editor is defined correctly in 'config.ini' and is added to PATH.")

def open_browser():
    browser = parser.get('DEFAULT', 'browser')
    try:
        subprocess.run(browser, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"Verify that the browser is defined correctly in 'config.ini' and is added to PATH.")
    
def run_git_command(operation, args):
    try:
        subprocess.run(f"git {operation} {args}", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Could not run Git operation. {e}")    

def prompt_main():
    options = ["Start", "Fetch", "Log", "Diff", "Pull", "Push", "Stage", "Commit", "Stash", "Revert", "Discard", "Reset", "Settings", "Quit"]
    while True:
        for i, opt in enumerate(options):
            print(f"{i+1}. {opt}")
        try:
            choice = int(input("Choose an option: ")) - 1
            if choice < 1:
                raise ValueError()
            opt = options[choice]
            if opt == "Start":
                prompt_start()
            elif opt == "Fetch":
                run_git_command("fetch", "origin")
                run_git_command("status", "-b")
            elif opt == "Log":
                prompt_log()
            elif opt == "Diff":
                if not subprocess.getoutput("git diff"):
                    print("\nNo tracked changes to analyze.")
                else:
                    run_git_command("diff", "origin")
            elif opt == "Pull":
                run_git_command("pull", "origin")
            elif opt == "Push":
                run_git_command("push", "origin")
            elif opt == "Stage":
                prompt_stage()
            elif opt == "Commit":
                if not get_staged_changes():
                    print("\nNo changes staged for commit. Please stage changes before committing.")
                else:
                    prompt_commit()
            elif opt == "Stash":
                # If this script has uncommitted changes, 
                if not file_is_committed(__file__):
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
                run_git_command("checkout", "-p")
            elif opt == "Discard":
                if not subprocess.getoutput("git ls-files --others --exclude-standard"):
                    print("\nNo untracked changes to discard.")
                else:
                    run_git_command("clean", "-i -d")
            elif opt == "Reset":
                prompt_select_commit()
            elif opt == "Settings":
                prompt_settings()
            elif opt == "Quit":
                sys.exit(1)  
        except (ValueError, IndexError):
            print("Invalid choice.")
            continue
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
            open_editor("")
        elif opt == "Resume":
            prompt_resume()
        elif opt == "Browse":
            open_browser()
        elif opt == "Daily-Note":
            path = f"{daily_notes_path}/{datetime.now().strftime('%Y-%m')}/{datetime.now().strftime('%F')}.md"
            open_editor(path)
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
                    open_editor(file)
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
                run_git_command("log", "--name-status --all")
                break
            elif opt == "Simple":
                run_git_command("log", "--oneline --all")
                break
            elif opt == "Verbose":
                run_git_command("log", "--oneline -p")
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
        run_git_command("commit", "-m '{message}'")
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
        if opt == "Stage-All":
            run_git_command("add", "-A")
            print("\nStaged all changes.")
        elif opt == "Unstage-All":
            run_git_command("restore", "--staged .")
            print("\nUnstaged all changes.")
        elif opt == "Stage-Interactive":
            run_git_command("add", "-i")
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
                    run_git_command("stash push", "-u -m '{message}'")
                else:
                    print("\nCanceled stash.")
                break
            elif opt == "Stash Staged":
                message = input("Enter stash message (or pass empty message to cancel): ")
                if message:
                    run_git_command("stash push", "--staged -m '{message}'")
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
                                run_git_command("stash apply", stash)
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
                                run_git_command("stash pop", stashes_trim[stash_choice])
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
                                            run_git_command("stash drop", stashes_trim[stash_choice])
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
    subprocess.run("git log --oneline --all -n 10", shell=True)
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
                run_git_command(f"reset --mixed", commit)
                break
            elif opt == "Soft":
                run_git_command(f"reset --soft", commit)
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
                        if hard_opt == "Yes":
                            run_git_command("reset --hard", commit)
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

def prompt_settings():
    options = ["Browser", "Editor", "Daily Notes", "Cancel"]
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")
    while True:
        try:
            choice = int(input("Choose an option: ")) - 1
            opt = options[choice]
            if opt == "Browser":
                current_browser = parser.get('DEFAULT', 'browser')
                new_browser = input("Set new default browser (or pass empty message to continue): ")
                if new_browser:
                    parser.set('DEFAULT', 'browser', new_browser)
                    with open(config_file, 'w') as newfile:
                        parser.write(newfile)
                    # test if setting is valid. if not, re-prompt
                else:
                    print(f"Browser kept as {current_browser}")
                break
            elif opt == "Editor":
                current_editor = parser.get('DEFAULT', 'editor')
                new_editor = input("Set new default editor (or pass empty message to continue): ")
                if new_editor:
                    parser.set('DEFAULT', 'browser', new_editor)
                    with open(config_file, 'w') as newfile:
                        parser.write(newfile)
                    # test if setting is valid. if not, re-prompt
                else:
                    print(f"Editor kept as {current_editor}")
                break
            elif opt == "Daily Notes":
                current_path = parser.get('DEFAULT', 'daily_notes_path')
                new_path = input("Set new default daily notes path (or pass empty message to continue): ")
                if new_path:
                    parser.set('DEFAULT', 'daily_notes_path', new_path)
                    with open(config_file, 'w') as newfile:
                        parser.write(newfile)
                    # test if setting is valid. if not, re-prompt
                else:
                    print(f"Daily notes path kept as {current_path}")  
                break
            elif opt == "Cancel":
                break
            else:
                print("Invalid choice")
        except (ValueError, IndexError):
            print("Invalid choice")

if __name__ == "__main__":

    main()
