"""Manage the "recent files" file operations"""
import json
import app_utils as app
import file_utils

def read(reverse_for_display=False):
    """Tries to read the history file"""
    _path = app.get_user_config_resource_path("history.json")
    try:
        # Read JSON file
        with open(_path, 'r', encoding="utf-8") as f:
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
        app.print_error(f"Error while decoding file history from '{_path}'.")
    return None

def save(data, message=""):
    """Writes and saves a value to the history file using json.dump()"""
    _path = app.get_user_config_resource_path("history.json")
    try:
        # Read JSON file
        with open(_path, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        if message != "":
            app.print_success(message)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        app.print_error(f"Error while saving file history to '{_path}'. {e}")

def add(fpath):
    """Updates the file history with the specified path (if applicable)"""
    _data = read(reverse_for_display=False)
    if not _data:
        # Initialize history as JSON array
        save([fpath])
    else:
        if fpath in _data:
            dupe_index = _data.index(fpath)
            # If pending duplicate is already at the end of the list, ignore
            if dupe_index < len(_data):
                _data.append(_data.pop(dupe_index))
        else:
            # Delete the first (oldest) entry if adding a new, unique entry
            if len(_data) not in range(0, 10):
                del _data[0]
            _data.append(fpath)
        save(_data)
