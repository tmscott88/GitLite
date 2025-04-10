"""The config handler module, using configparser"""
# Python modules
import os
import configparser
from datetime import datetime
# My modules
import app_utils as app
import file_utils

class Config:
    """The base config class"""
    parser = configparser.ConfigParser()

    def __init__(self, path, quiet=False):
        self.path = path
        self.quiet = quiet

    def read(self):
        """Tries to read the config file using configparser"""
        try:
            with open(self.path, 'r', encoding="utf-8") as f:
                self.parser.read_file(f)
        except FileNotFoundError:
            if not self.quiet:
                app.print_warning(f"Could not find a valid config file in '{os.getcwd()}'.")
            raise
        except configparser.Error as e:
            if not self.quiet:
                app.print_error(f"Error while reading config file. {e}")
            raise

    def get_value(self, section, option):
        """Reads a value from the config file using configparser"""
        try:
            return self.parser.get(section, option)
        except ValueError:
            app.print_error(f"Failed to retrieve ['{section}', '{option}'] from '{self.path}'. '{option}' is not a valid boolean.")
        except configparser.Error as e:
            app.print_error(f"Failed to retrieve ['{section}', '{option}'] from '{self.path}'. {e}")
            app.print_info(f"Please verify that '{self.path}' is setup correctly.")
        return None

    def get_bool(self, section, option):
        """Similar to get_value, except using ConfigParser's boolean coercing"""
        try:
            return self.parser.getboolean(section, option)
        except ValueError:
            app.print_error(f"Failed to retrieve ['{section}', '{option}'] from '{self.path}'. '{option}' is not a valid boolean.")
        except configparser.Error as e:
            app.print_error(f"Failed to retrieve ['{section}', '{option}'] from '{self.path}'. {e}")
            app.print_info(f"Please verify that '{self.path}' is setup correctly.")
        return None

    def set_value(self, section, option, value):
        """Updates a value in the config file using configparser"""
        try:
            self.parser.set(section, option, value)
            if self.quiet:
                self.save()
            else:
                self.save(f"Set ['{section}', '{option}'] = '{value}'")
        except (configparser.NoSectionError, TypeError) as e:
            app.print_error(f"Failed to set ['{section}', '{option}'] = '{value}' in '{self.path}'. {e}")

    def save(self, message=""):
        """Writes and saves a value to the config file using configparser"""
        try:
            with open(self.path, "w", encoding="utf-8") as newfile:
                self.parser.write(newfile)
            if message != "":
                app.print_success(message)
        except FileNotFoundError:
            app.print_error(f"Could not find a valid config file '{newfile}'")
        except configparser.Error as e:
            app.print_error(f"Failed to save to config file '{newfile}': {e}")

    def show(self):
        """Displays the config file, section by section"""
        try:
            for section in self.parser.sections():
                print()
                print(f"[{section}]")
                for key, value in self.parser.items(section):
                    print(f"{key} = {value}")
        except configparser.NoSectionError as e:
            app.print_error(f"Failed to display config file. {e}")

class AppConfig(Config):
    """Perform app-specific operations to the base config file"""
    def __init__(self, path, quiet=False):
        super().__init__(path, quiet=False)
        self.path = path
        self.quiet = quiet

    def generate(self):
        """Generate a new config file if it doesn't exist already"""
        try:
            if app.platform_is_windows():
                self.parser['PATHS'] = {
                    'editor': 'notepad.exe', 
                    'browser': 'default', 
                    'daily_notes': 'daily'}
            elif app.platform_is_unix():
                self.parser['PATHS'] = {
                    'editor': 'nano', 
                    'browser': 'default', 
                    'daily_notes': 'daily'}
            self.parser['FLAGS'] = {
                'browser_hidden_files': 'off', 
                'browser_readonly_mode': 'off', 
                'daily_notes': 'off'}
            self.save(f"A new config file '{self.path}' was generated with these defaults.")
        except (FileNotFoundError, configparser.Error) as e:
            app.print_error(f"Could not generate '{self.path}' config file. {e}")
            raise

    def is_in_current_dir(self):
        """Returns True if the config file is saved in the working directory"""
        try:
            self.read()
            return bool(file_utils.get_path_head(self.path) == os.getcwd())
        except FileNotFoundError:
            return False

    def get_today_note_path(self):
        """Returns a file path based on the current date, 
            ordered by each year and month 
            (Default: DAILY_NOTES_ROOT/YEAR/YEAR-MONTH/YEAR-MONTH-DAY.md)
        """
        root = self.get_daily_notes_root_path()
        now = datetime.now().strftime("%F")
        # ['YEAR', 'MONTH', 'DAY']
        date_arr = now.split("-")
        year_month = f"{date_arr[0]}-{date_arr[1]}"
        note_filename = f"{date_arr[0]}-{date_arr[1]}-{date_arr[2]}.md"
        full_note_path = os.path.join(root, date_arr[0], year_month, note_filename)
        return full_note_path

    def is_daily_notes_enabled(self):
        """Returns whether the default browser should display hidden files"""
        return bool(self.get_daily_notes_status())

    def is_browser_hidden_files_enabled(self):
        """Returns whether the default browser should display hidden files"""
        return bool(self.get_browser_hidden_files_status())

    def is_browser_readonly_mode_enabled(self):
        """Returns whether the default browser should be in read-only mode"""
        return bool(self.get_browser_readonly_mode_status())

    def get_app(self, app_type):
        """Returns the specified app as defined in the config file"""
        return self.get_value('PATHS', app_type)

    def get_daily_notes_root_path(self):
        """Returns the Daily Notes root path as defined in the config file"""
        return self.get_value('PATHS', 'daily_notes')

    def get_daily_notes_status(self):
        """Returns the Daily Notes flag in the config file"""
        return self.get_bool('FLAGS', 'daily_notes')

    def get_browser_hidden_files_status(self):
        """Returns the default browser's hidden files visibility flag in the config file"""
        return self.get_bool('FLAGS', 'browser_hidden_files')

    def get_browser_readonly_mode_status(self):
        """Returns the default browser's readonly mode flag in the config file"""
        return self.get_bool('FLAGS', 'browser_readonly_mode')

    def set_app(self, app_type, new_app):
        """Updates the specified app by app type in the config file"""
        self.set_value('PATHS', app_type, new_app)

    def set_daily_notes_status(self, new_status):
        """Enables or disables Daily Notes in the config file"""
        self.set_value('FLAGS', 'daily_notes', new_status)

    def set_daily_notes_path(self, new_path):
        """Sets the daily notes root path in the config file"""
        self.set_value('PATHS', 'daily_notes', new_path)

    def set_browser_hidden_files(self, new_status):
        """Sets the browser hidden files visiblity flag in the config file"""
        self.set_value('FLAGS', 'browser_hidden_files', new_status)

    def set_browser_readonly_mode(self, new_status):
        """Sets the browser readonly mode flag in the config file"""
        self.set_value('FLAGS', 'browser_readonly_mode', new_status)

    def show_config_template(self):
        """View a working sample config file"""
        print(f"""
            File: {self.path}

            [PATHS]
            editor = {app.get_system_app("editor")}
            browser = {app.get_system_app("browser")}
            daily_notes = daily

            [FLAGS]
            daily_notes = off
            browser_hidden_files = off
            browser_readonly_mode = off
        """)

    def factory_reset(self):
        """Deletes the existing config file, returning the app to its default state"""
        try:
            if os.path.exists(self.path):
                os.remove(self.path)
                app.print_success(f"Deleted config file '{self.path}'")
            else:
                app.print_info(f"{self.path} not found.")
            app.print_warning("GitWriting must be restarted in order to continue.")
            app.prompt_exit()
        except (OSError, FileNotFoundError) as e:
            app.print_error(f"Could not perform factory reset: {e}")
            app.prompt_exit()
