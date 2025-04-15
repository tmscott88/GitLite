"""Manage the "recent files" file operations"""
import os
import json
import appdirs
import app_utils as app
import file_utils

def read():
    """Tries to read the history file"""
    path = os.path.join(
        appdirs.user_config_dir(appname=app.APP_NAME, appauthor=False), "history.ini")
    try:
        # Read JSON file
        with open(path, 'r', encoding="utf-8") as f:
            data = json.load(f)
        # Remove files that no longer exist
        old_len = len(data)
        for d in data:
            if not os.path.exists(file_utils.get_standard_path(d)):
                data.remove(d)
        # If files have been deleted, update data file
        if old_len > len(data):
            save(data)
        data.reverse()
        return data
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

def update(fpath):
    """Updates the file history if applicable"""
    data = read()
    if not data:
        save([fpath])
    else:
        # Keep n files max in the history file rotation
        if len(data) in range(0, 9):
            # If the file is already in history, move it to the end (latest)
            if fpath in data:
                dup_index = data.index(fpath)
                if dup_index < len(data):
                    data.append(data.pop(dup_index))
            else:
                data.append(fpath)
            save(data)
            return
        # If the array is full Remove first (oldest) entry from data, append latest and save
        del data[0]
        if fpath in data:
            data.append(data.pop(data.index(fpath)))
        else:
            data.append(fpath)
        save(data)
