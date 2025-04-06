import os
import sys
import app_utils as app

def create_new_file(new_path):
    """Creates a new file if needed."""
    if not is_existing_file(new_path) and not is_existing_directory(new_path):
        try:
            # Only make new directory/directories if the file path forms a directory.
            if os.path.dirname(new_path) != "":
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
            # print(f"\nos.path.dirname: {os.path.dirname(new_path)}")
            f = open(new_path, 'w')
            app.print_success(f"Created file '{new_path}'")
        except Exception as e:
            app.print_error(f"Failed to create file '{new_path}'. {e}")
    elif not is_existing_file(new_path) and is_existing_directory(new_path):
        app.print_error(f"A folder '{new_path}' already exists in this directory. Please create a different file name or directory.")

def create_new_directory(new_path):
    """Creates a new directory (and any intermediate directories denoted by the path seperator) if needed."""
    if not is_existing_directory(new_path) and not is_existing_file(new_path):
        try:
            # TODO test path normalization
            os.makedirs(new_path, exist_ok=True)
            app.print_success(f"Created new directory '{new_path}'")
        except Exception as e:
            app.print_error(f"Failed to create directory '{new_path}'. {e}")
    elif not is_existing_directory(new_path) and is_existing_file(new_path):
        app.print_error(f"A file '{new_path}' already exists in this directory. Please create a different directory name.")
        raise FileExistsError

def is_existing_file(path):
    return bool(os.path.isfile(path))
    
def is_existing_directory(dir):
    return bool(os.path.isdir(dir))