"""App utilities go here"""
import os
import sys
from readchar import readkey

VERSION = "0.8.6"
PROJECT_URL = "https://github.com/tmscott88/GitWriting" 

def get_expected_config_path():
    """Returns the expected config path. By default, will point to the working directory"""
    return os.path.join(os.getcwd(), "gitwriting.ini")

def get_runtime_directory(convert=True):
    """Returns the directory of the current script. Converts to standard path format by default. On Windows, will return in Windows path format if set False."""
    runtime_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    if convert:
        return runtime_dir.strip().replace(os.sep, '/')
    return runtime_dir

def change_working_directory(new_directory):
    """Change the working directory using os.chdir()."""
    try:
        os.chdir(new_directory)
    except OSError as e:
        print_error(f"Could not change working directory to '{new_directory}'. {e}")
            
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

def get_resource_path(relative_path):
    """Returns the absolute path to a resource (if the resource exists in the app data), works for dev and for PyInstaller. Resources must be added when building the app, e.g. with PyInstaller (--add-data ...)"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    except AttributeError:
        print_error(f"Could not retrieve an app resource path for {relative_path}.")
        print_warning(f"This feature is unavailable when running the app from source. Please build the app using PyInstaller or download the latest release from: {PROJECT_URL}.")
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
    print(f"GitWriting {VERSION}")

def print_author():
    print("Author: Tom Scott (tmscott88)")
    print(PROJECT_URL)

def print_system():
    if platform_is_windows():
        print("Platform: Windows")
    elif platform_is_unix():
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

def show_app_not_found_error(name):
    print_error(f"App '{name}104 not found.")
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