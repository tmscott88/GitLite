import os
import sys
from commands import Command

__version = "0.8.4"
project_url = "https://github.com/tmscott88/GitWriting" 

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

def get_system_app(app_type):
    match(app_type):
        case "browser":
            print(f"\nSystem browser support coming soon.")
            pass
        case "editor":
            match(get_platform()):
                case "Unix":
                    editor = os.getenv('EDITOR')
                    if not editor:
                        return nano
                    else:
                        return editor
                case "Windows":
                    print(f"\nWindows system editor support coming soon.")
                    # TODO add default Windows editor
                    # return "Notepad" or maybe search for nano and route there
            pass
        case _:
            print("\nSystem")

def prompt_exit():
    print("\nPress any key to exit...")
    k = readchar.readchar()
    sys.exit()

def print_version():
    print(f"GitWriting {__version}")

def print_author():
    print("Author: Tom Scott (tmscott88)")
    print(project_url)

def print_system():
    print(f"Platform: {get_platform()}")
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

def show_config_template():
    """Uses the `less` command to view a working config.ini example"""
    cmd = Command()
    print("""
        File: config.ini

        [APPS]
        editor = micro
        browser = glow

        [DAILY_NOTES]
        status = on
        path = DAILY
    """)

# def print_options(options, title):
#     print(f"\n[{title}]")
#     for i, opt in enumerate(options):
#         print(f"{i+1}. {opt}")