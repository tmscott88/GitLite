"""Contains various file management functions"""
import os
import app_utils as app

def get_standard_path(path):
    """(For Windows) Converts the specified path to a standardized path format 
        with forward slashes instead of backward slashes."""
    return path.strip().replace(os.sep, '/')

def get_absolute_path(rel_path):
    """Returns the absolute path of a relative path, starting at the working directory"""
    return os.path.abspath(rel_path)

def get_entries_in_directory(path, include_hidden=False):
    """(Python 3.5+) Return a list of DirEntry object names,
        each corresponding to the entries in the specified directory."""
    results = []
    try:
        if not os.access(path, os.R_OK):
            raise PermissionError
        for entry in os.scandir(path):
            if not include_hidden:
                if not entry.name.startswith('.'):
                    results.append(entry.name)
            else:
                results.append(entry.name)
    except PermissionError:
        return None
    return results

def get_folders_in_directory(path, include_hidden=False):
    """Return an list of names corresponding to the folder entries in the specified directory.
        (DIRECTORIES ONLY)"""
    results = []
    try:
        if not os.access(path, os.R_OK):
            raise PermissionError
        for entry in os.scandir(path):
            if not include_hidden:
                if not entry.name.startswith('.') and entry.is_dir():
                    results.append(entry.name)
            else:
                if entry.is_dir():
                    results.append(entry.name)
    except PermissionError:
        return None
    return results

def get_path_head(path):
    """Returns one directory higher than the specified path."""
    return os.path.split(path)[0]

def get_path_tail(path):
    """Returns the last part of the path"""
    return os.path.split(path)[1]

def create_new_file(new_path):
    """Creates a new file if needed."""
    if not is_file(new_path) and not is_directory(new_path):
        try:
            # Only make new directory/directories if the file path forms a directory.
            if os.path.dirname(new_path) != "":
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
            with open(new_path, 'w', encoding="utf-8"):
                app.clear()
                app.print_success(f"Created file '{new_path}'")
        except OSError as e:
            app.print_error(f"Failed to create file '{new_path}'. {e}")
    elif not is_file(new_path) and is_directory(new_path):
        app.print_error(f"A folder '{new_path}' already exists in this directory. "
            "Please create a different file name or directory.")

def create_new_directory(new_path):
    """Creates a new directory (and any intermediate directories denoted by the path seperator)."""
    if not is_directory(new_path) and not is_file(new_path):
        try:
            os.makedirs(new_path, exist_ok=True)
            app.print_success(f"Created new directory '{new_path}'")
        # Shouldn't reach this since exist_ok=True but keep it just in case
        except FileExistsError as e:
            app.print_error(f"Failed to create directory '{new_path}'. {e}")
    elif not is_directory(new_path) and is_file(new_path):
        app.print_error(f"A file '{new_path}' already exists in this directory. "
            "Please create a different directory name.")
        raise FileExistsError

def is_file(path):
    """Returns whether the specified path exists and is a file"""
    return bool(os.path.isfile(path))

def is_directory(path):
    """Returns whether the specified path exists is a directory"""
    return bool(os.path.isdir(path))
