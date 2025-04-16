"""App utilities go here"""
import os
import sys
import time
from readchar import readkey
import appdirs

APP_NAME = "GitWriting"
VERSION = "0.8.8"
PROJECT_URL = "https://github.com/tmscott88/GitWriting"

def clear(delay=0):
    """Clears the console. Recommended for ue when """
    if platform_is_windows():
        os.system('cls')
    elif platform_is_unix():
        os.system('clear')
    time.sleep(delay)

def change_working_directory(new_directory):
    """Change the working directory using os.chdir()."""
    try:
        os.chdir(new_directory)
    except OSError as e:
        print_error(f"Could not change working directory to '{new_directory}'. {e}")
        raise

def get_system_app(app_type):
    """Based on the current platform, returns the default app for the provided app type"""
    match(app_type):
        case "browser":
            return "default"
        case "editor":
            if platform_is_windows():
                return "notepad.exe"
            if platform_is_unix():
                editor = os.getenv('EDITOR')
                if not editor:
                    return "nano"
                return editor
            print_warning("Platform not supported.")
        case _:
            print_error(f"App type '{app_type}' is not supported.")

def get_user_config_resource_path(fname):
    """Returns the absolute path to a resource (if the resource exists in the user config directory)"""
    return os.path.join(
        appdirs.user_config_dir(appname=APP_NAME, appauthor=False), fname)

def get_python_resource_path(relative_path):
    """Returns the absolute path to a resource (if the resource exists in the app data)
        Works for dev and for PyInstaller.
        Resources must be added when building the app, e.g. with PyInstaller (--add-data ...)"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    except AttributeError:
        print_error(f"Could not find an app resource path for '{relative_path}'.")
        print_warning(f"This feature is unavailable when running {APP_NAME} from source.")
        print_warning(f"Please build the app using PyInstaller (See README) or download the latest release from: {PROJECT_URL}.")
    return None

def platform_is_windows():
    """Using os.name, returns True if 'nt'."""
    return os.name == "nt"

def platform_is_unix():
    """Using os.name, returns True if 'posix'."""
    return os.name == "posix"

def prompt_exit():
    """Prompts to exit the app."""
    print("\nPress any key to exit...")
    readkey()
    sys.exit()

def prompt_continue(any_key=False):
    """Use this prompt to confirm whether to continue with a process or not."""
    if any_key:
        print("\nPress any key to continue...")
        k = readkey()
        return None
    while True:
        print("\nContinue? (Y/n): ")
        k = readkey()
        if k in ('y', 'Y'):
            return True
        if k in ('n', 'N'):
            return False
        print_error("Invalid option.")
        continue

def print_version():
    """Helper function to print the app version"""
    print(f"{APP_NAME} {VERSION}")

def print_author():
    """Helper function to print the app author and project URL"""
    print("Author: Tom Scott (tmscott88)")
    print(PROJECT_URL)

def print_system():
    """Prints the current platform"""
    if platform_is_windows():
        print("Platform: Windows")
    elif platform_is_unix():
        print("Platform: Unix")
    else:
        print("Platform: Other")
    print(f"Python: {sys.version[:7]}")

def show_splash(verbose=False):
    """Prints the app version and author. If verbose=True, prints the system information as well."""
    print()
    print_version()
    print_author()
    if verbose:
        print_system()

def show_app_not_found_error(name):
    """Prints an error that the specified app was not found"""
    print_error(f"App '{name}' not found.")
    print_warning("Ensure that the app's name is defined correctly and installed systemwide.\n", new_line=False)

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
    if new_line:
        print(f"\n\u274C {message}")
    else:
        print(f"\u274C {message}")

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
