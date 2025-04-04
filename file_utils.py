import os

def convert_to_unix_path(fpath):
    """Replaces the current system's default path seperators with the standard Unix forward slash"""
    return os.path.join(get_current_dir(), fpath).replace(os.set, '/')

def create_new_file(new_path):
    """Returns True if a new file is created or already exists, False if not created."""
    # print(f"\nReceived path {new_path}.")
    converted_path = convert_to_unix_path(new_path)
    if not is_existing_file(new_path) and not is_existing_directory(new_path):
        try:
            # Only make new directory/directories if the file path forms a directory.
            if os.path.dirname(new_path) != "":
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
            # print(f"\nos.path.dirname: {os.path.dirname(new_path)}")
            f = open(new_path, 'w')
            # print(f"\nCreated file {f}.")
        except Exception as e:
            print(f"\nCould not create file '{new_path}'. {e}")
    elif not is_existing_file(new_path) and is_existing_directory(new_path):
        print(f"\nA folder '{new_path}' already exists in this directory. Please create a different file name or directory.")

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
        print(f"\nA file '{new_path}' already exists in this directory. Please create a different directory name.")
    # TODO move this to interactive class
    # else:
    #     set_daily_notes_path(new_path)

def is_existing_file(path):
    return bool(os.path.isfile(path))
    
def is_existing_directory(dir):
    return bool(os.path.isdir(dir))