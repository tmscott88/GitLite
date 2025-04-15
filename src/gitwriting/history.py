"""Manage the "recent files" file operations"""
import os
import json
import appdirs
import app_utils as app
import file_utils

def read(reverse_for_display=False):
    """Tries to read the history file"""
    path = os.path.join(
        appdirs.user_config_dir(appname=app.APP_NAME, appauthor=False), "history.ini")
    try:
        # Read JSON file
        with open(path, 'r', encoding="utf-8") as f:
            data = json.load(f)
        # Remove files that no longer exist
        parsed_data = [d for d in data if file_utils.is_file(d)]
        # If files have been deleted, update data file
        if len(data) > len(parsed_data):
            save(parsed_data)
        if reverse_for_display:
            parsed_data.reverse()
        return parsed_data
    except FileNotFoundError:
        # Create empty JSON file since this isn't a file the user needs to interact with
        save([])
    except json.JSONDecodeError:
        app.print_error(f"Error while decoding file history from '{path}'.")
    return None

def save(data, message=""):
    """Writes and saves a value to the history file using json.dump()"""
    path = os.path.join(
        appdirs.user_config_dir(appname=app.APP_NAME, appauthor=False), "history.ini")
    try:
        # Read JSON file
        with open(path, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        if message != "":
            app.print_success(message)
    except json.JSONDecodeError:
        app.print_error(f"Error while saving file history to '{path}'.")

def add(fpath):
    """Updates the file history with the specified path (if applicable)"""
    data = read(reverse_for_display=False)
    if not data:
        # Initialize history as JSON array
        save([fpath])
    else:
        if fpath in data:
            dupe_index = data.index(fpath)
            # If pending duplicate is already at the end of the list, ignore
            if dupe_index < len(data):
                data.append(data.pop(dupe_index))
        else:
            # Delete the first (oldest) entry if adding a new, unique entry
            if len(data) not in range(0, 10):
                del data[0]
            data.append(fpath)
        save(data)
