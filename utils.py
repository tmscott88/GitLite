import os
import sys
from commands import Command

__version = "0.8.4"

def __get_platform():
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

# TODO test this a lot
def new_file_converted(fpath):
    return os.path.join(get_current_dir(), fpath).replace(os.set, '/')

def prompt_exit():
    print("\nPress any key to exit...")
    k = readchar.readchar()
    sys.exit()

def print_splash():
    print(f"\n[GitWriting {__version}]")
    print("Author: Tom Scott (tmscott88)")
    print("https://github.com/tmscott88/GitWriting")

def print_system():
    print(f"Platform: {__get_platform()}")
    print(f"Python: {sys.version[:7]}")

# def print_options(options, title):
#     print(f"\n[{title}]")
#     for i, opt in enumerate(options):
#         print(f"{i+1}. {opt}")

def create_new_file(new_path):
    """Returns True if a new file is created or already exists, False if not created."""
    if not is_existing_file(new_path) and not is_existing_directory(new_path):
        try:
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            f = open(new_path, 'w')
            print(f"\nCreated file {new_path}.")
        except subprocess.CalledProcessError as e:
            print(f"\nCould not create file '{new_path}'. {e}")

def create_new_directory(new_path):
    """Returns True if a new directory is created, False if not created."""
    # if path doesn't exist, create the directory
    if not is_existing_directory(new_path) and not is_existing_file(new_path):
        try:
            # TODO test path normalization
            os.makedirs(new_path, exist_ok=True)
            return False
            # TODO move this to interactive class
            # if is_existing_directory(new_path):
            #     return True
            #     set_daily_notes_path(new_path)   
            # else:
            #     print(f"\nPath creation failed. Keep current path.")
            #     return False
        except Exception as e:
            print(f"\nCould not create directory '{new_path}'. {e}")
            return False
    # if directory doesn't exist but conflicting file exists
    elif not is_existing_directory(new_path) and is_existing_file(new_path):
        print(f"\nA file '{new_path}' already exists in this directory.")
    # TODO move this to interactive class
    # else:
    #     set_daily_notes_path(new_path)

def is_existing_file(path):
    return bool(os.path.isfile(path))
    
def is_existing_directory(dir):
    return bool(os.path.isdir(dir))