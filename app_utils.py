# Python modules
import os
import sys
from readchar import readkey, key
# My modules
from commands import Command

__version = "0.8.5"
project_url = "https://github.com/tmscott88/GitWriting" 

def convert_to_unix_path(fpath):
    """Replaces the current system's default path seperators with the standard Unix forward slash"""
    return fpath.strip().replace(os.sep, '/')

def get_current_dir():
    """Returns the directory that this app is running in as a Unix-formatted path"""
    current = os.path.dirname(os.path.abspath(sys.argv[0]))
    return convert_to_unix_path(current)
            
def get_system_app(app_type):
    match(app_type):
        case "browser":
            if platform_is_windows():
                return "explorer.exe"
            elif platform_is_unix():
                print_question(f"Unix system browser support coming soon.")
            else:
                print_warning(f"Platform not supported.")
        case "editor":
            if platform_is_windows():
                return "notepad.exe"
            elif platform_is_unix():
                editor = os.getenv('EDITOR')
                if not editor:
                    return "nano"
                else:
                    return editor
            else:
                print_warning(f"Platform not supported.")
        case _:
            print_error(f"App type '{app_type}' is not supported.")

def is_valid_repo():
    """Check if the app is placed at the top level of a git repo"""
    cmd = Command()
    try:
        git_root = cmd.get_output("git rev-parse --show-toplevel")[0]
        script_dir = get_current_dir()
        # print(f"\n(DEBUG) Git Root: {git_root}")
        # print(f"(DEBUG) Script Dir: {script_dir}")
        return bool(git_root == script_dir)
    except Exception as e:   
        return False

def platform_is_windows():
    return os.name == "nt"

def platform_is_unix():
    return os.name == "posix"

# def is_running_in_windows_terminal():
#     """Returns True if "WT_SESSION" is found as an environment variable. The Windows Terminal sets a specific environment variable, WT_SESSION, when it's running."""
#     return platform_is_windows() and "WT_SESSION" in os.environ

def prompt_exit():
    print("\nPress any key to exit...")
    k = readkey()
    sys.exit()

def prompt_continue(any_key=False):
    if any_key:
        print("\nPress any key to continue...")
        k = readkey()
        return
    else:
        while True:
            print("\nContinue? (Y/n): ")
            k = readkey()
            if k == "y" or k == "Y":
                return True
            elif k == "n" or k == "N":
                return False
            else:
                print_error("Invalid option.")
                continue


def print_version():
    print(f"GitWriting {__version}")

def print_author():
    print("Author: Tom Scott (tmscott88)")
    print(project_url)

def print_system():
    if platform_is_windows():
        print("Platform: Windows")
    elif platform_is_unix:
        print("Platform: Unix")
    else:
        print("Platform: Other")
    print(f"Python: {sys.version[:7]}")

def show_splash():
    print()
    print_version()
    print_author()

def show_about():
    print()
    print_version()
    print_author()
    print_system()
    prompt_continue(any_key=True)

# symbols = {
#     "error": "\u274C",
#     "success": "\u2705"
#     "warning ": "\u26A0"
#     "info": "\u2139"
# }
def print_success(message, new_line=True):
    """Prints a message prepended with a newline and a green checkbox."""
    if new_line:
        print(f"\n\u2705 {message}")
    else:
        print(f"\u2705 {message}")


def print_warning(message, new_line=True):
    """Prints a message prepended with a newline and a "warning" triangle."""
    if new_line:
        print(f"\n\u26A0 {message}")
    else:
        print(f"\u26A0 {message}")

def print_error(message, new_line=True):
    """Prints a message prepended with an optional newline and a red "cancel" circle."""
    print(f"\u274C {message}")
    pass

def print_info(message, new_line=True):
    """Prints a message prepended with a newline and an "info" mark."""
    if new_line:
        print(f"\n\u2139 {message}")
    else:
        print(f"\u2139 {message}")

def print_question(message, new_line=True):
    """Prints a message with an optional newline and a question mark."""
    if new_line:
        print(f"\n\u003F {message}")
    else:
        print(f"\u003F {message}")