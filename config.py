# Python modules
import os
import configparser
from datetime import datetime
# My modules
import app_utils as app

class Config:
    name = "gitwriting.ini"
    parser = configparser.ConfigParser()

    def read(self, quiet=False):
        try:
            with open(self.name, 'r', encoding="utf-8") as file:
                self.parser.read(self.name)
        except (Exception, FileNotFoundError) as e:
            if not quiet:
                app.print_error(f"Error while reading config file. {e}")
            raise
    def get_value(self, section, option):
        try:
            return self.parser.get(section, option)
        except Exception as e:
            app.print_error(f"Failed to retrieve ['{section}', '{option}'] from '{self.name}'. {e}")
            app.print_info(f"Please verify that '{self.name}' is setup correctly.")

    def set_value(self, section, option, value):
        try:
            self.parser.set(section, option, value)
            self.save(f"Set ['{section}', '{option}'] = '{value}'")
        except Exception as e:
            app.print_error(f"Failed to set ['{section}', '{option}'] = '{value}' in '{self.name}'. {e}")

    def save(self, message):
        try:
            with open(self.name, "w", encoding="utf-8") as newfile:
                self.parser.write(newfile)
            app.print_success(message)
        except Exception as e:
            app.print_error(f"Failed to save to config file '{newfile}': {e}")

    def show(self):
        try:     
            for section in self.parser.sections():
                print()
                print(f"[{section}]")
                for key, value in self.parser.items(section):
                    print(f"{key} = {value}")
        except Exception as e:
            app.print_error(f"Failed to display config file. {e}")

class AppConfig(Config):
    def generate(self):
        """Generate a new config file if it doesn't exist already"""
        try:
            if app.platform_is_windows():
                self.parser['APPS'] = {'editor': 'notepad.exe', 'browser': 'default'}
            elif app.platform_is_unix():
                self.parser['APPS'] = {'editor': 'nano', 'browser': 'default'}
            self.parser['DAILY_NOTES'] = {'status': 'off', 'path': 'daily'}
            self.parser['FLAGS'] = {'hidden_files': 'off'}
            self.save(f"A new config file '{self.name}' was generated with these defaults, based on your system.")
        except Exception as e:
            app.print_error(f"Error while generating config file. {e}")
            raise

    def get_today_note_path(self):
        """Returns a file path based on the current date, ordered by each year and month (Default: DAILY_NOTES_ROOT/YEAR/YEAR-MONTH/YEAR-MONTH-DAY.md)"""
        root = self.get_daily_notes_root_path()
        now = datetime.now().strftime("%F")
        # ['YEAR', 'MONTH', 'DAY']
        date_arr = now.split("-")
        year_month = f"{date_arr[0]}-{date_arr[1]}"
        note_filename = f"{date_arr[0]}-{date_arr[1]}-{date_arr[2]}.md"
        full_note_path = os.path.join(root, date_arr[0], year_month, note_filename)
        return full_note_path

    def is_present(self):
        try:
            self.read(quiet=True)
            return True
        except (FileNotFoundError, Exception):
            return False

    def is_daily_notes_enabled(self):
        status = self.get_daily_notes_status()
        return bool(status == "on")

    def is_hidden_files_enabled(self):
        status = self.get_hidden_files_status()
        return bool(status == "on")

    def get_app(self, app_type):
        return self.get_value('APPS', app_type)

    def get_daily_notes_status(self):
        return self.get_value('DAILY_NOTES', 'status')

    def get_daily_notes_root_path(self):
        return self.get_value('DAILY_NOTES', 'path')

    def get_hidden_files_status(self):
        return self.get_value('FLAGS', 'hidden_files')

    def set_app(self, app_type, new_app):
        self.set_value('APPS', app_type, new_app)

    def set_daily_notes_status(self, new_status):
        self.set_value('DAILY_NOTES', 'status', new_status)
        
    def set_daily_notes_path(self, new_path):
        self.set_value('DAILY_NOTES', 'path', new_path)

    def set_hidden_files(self, new_status):
        self.set_value('FLAGS', 'hidden_files', new_status)
        
    def show_app_not_found_error(self, name):
        app.print_error(f"App '{name}' not found.")
        app.print_info("Ensure that the app's name is defined correctly in '{self.name}' and installed systemwide.\n", new_line=False)

    def show_config_read_error(self):
        app.print_error(f"Failed to read expected config file '{self.name}'. Functionality will be limited until this is resolved.") 
        app.print_info("Please create and place `{self.name}' in your Git repo's root directory with the following structure.")
        app.print_info("Visit the 'Help' menu or https://github.com/tmscott88/GitWriting/blob/main/README.md for further instructions.")

    def show_config_template(self):
        """View a working sample config file"""
        print(f"""
            File: {self.name}

            [APPS]
            editor = {app.get_system_app("editor")}
            browser = {app.get_system_app("browser")}

            [DAILY_NOTES]
            status = off
            path = daily

            [FLAGS]
            hidden_files = off
        """)

    def factory_reset(self):
        try:
            if os.path.exists(self.name):
                os.remove(self.name)
                app.print_success(f"Deleted config file '{self.name}'")
            else:
                app.print_info(f"{self.name} not found.")
            app.print_warning("GitWriting must be restarted in order to continue.")
            app.prompt_exit()
        except Exception as e:
            app.print_error(f"Error while performing reset: {e}")
            app.prompt_exit()
