import os
import configparser
import app_utils

class Config:
    name = "gitwriting.ini"
    parser = configparser.ConfigParser()

    def generate(self):
        """Generate a new config file if it doesn't exist already"""
        match(app_utils.get_platform()):
            case "Unix":
                self.parser['APPS'] = {'editor': 'nano', 'browser': ''}
            case "Windows":
                # TODO dtermine how to best handle windows defaults: Stay in CLI, open GUI apps?
                self.parser['APPS'] = {'editor': 'notepad.exe', 'browser': ''}
        self.parser['DAILY_NOTES'] = {'status': 'off', 'path': ''}
        # self.parser['MISC'] = {'commit_limit': '""'}
        self.save(f"* A new config file was generated for you: '{self.name}'.")

    def read(self):
        try:
            with open(self.name, 'r', encoding="utf-8") as file:
                self.parser.read(self.name)
        except (Exception, FileNotFoundError) as e:
            # print(f"Error reading config file. {e}")
            # self.show_config_read_error()
            raise
    
    def get_value(self, section, option):
        try:
            return self.parser.get(section, option)
        except Exception as e:
            print(f"\nCould not retrieve ['{section}', '{option}'] from '{self.name}'. {e}")
            print(f"\nPlease verify that '{self.name}' is setup correctly.")

    def set_value(self, section, option, value):
        try:
            self.parser.set(section, option, value)
            self.save(f"Set ['{section}', '{option}'] = '{value}'")
        except Exception as e:
            print(f"\nCould not set ['{section}', '{option}'] = '{value}' in '{self.name}'. {e}")

    def save(self, message):
        try:
            with open(self.name, "w", encoding="utf-8") as newfile:
                self.parser.write(newfile)
            print(f"\n{message}")
            # self.show()
        except Exception as e:
            print(f"\nCould not save to config file '{newfile}': {e}")

    def show(self):
        try:     
            # print(f"\n> {self.name}")
            for section in self.parser.sections():
                print()
                print(f"[{section}]")
                for key, value in self.parser.items(section):
                    print(f"{key} = {value}")
        except Exception as e:
            print(f"\nCould not display config file. {e}")

class AppConfig(Config):
    def is_present(self):
        try:
            self.read()
            return True
        except (FileNotFoundError, Exception):
            return False

    def get_app(self, app_type):
        return self.get_value('APPS', app_type)

    # def get_commit_limit(self):
    #     return self.get_value('MISC', 'commit_limit')

    def get_daily_notes_status(self):
        return self.get_valuet('DAILY_NOTES', 'status')

    def get_daily_notes_path(self):
        return self.get_value('DAILY_NOTES', 'path')

    def set_app(self, app_type, new_app):
        self.set_value('APPS', app_type, new_app)

    # def set_commit_limit(self):
    #     self.set_value('MISC', 'commit_limit', new_limit)

    def set_daily_notes_status(self, new_status):
        self.set_value('DAILY_NOTES', 'status', new_status)
        
    def set_daily_notes_path(self):
        self.set_value('DAILY_NOTES', 'path', new_path)
        
    def show_app_not_found_error(self, name):
        print(f"\nApp '{name}' not found, or '{name}' just crashed. This may be due to a missing reference/installation, or perhaps something is wrong with {name}'s configuration.") 
        print(f"\nEnsure that the app's reference name is defined correctly in '{self.name}' and installed systemwide.") 
        print(f"\nConsult {name}'s documentation and/or forums for more information.")
        print(f"\nIf '{name}' works fine outside of GitWriting, and you are still experiencing issues here, please open an issue at:")
        print("\nhttps://github.com/tmscott88/GitWriting/issues")

    def show_config_read_error(self):
        print(f"\n! Could not read expected config file '{self.name}'. Functionality will be limited until this is resolved.") 
        print(f"! Please create and place `{self.name}' in your Git repo's root directory with the following structure.")
        print(f"? Visit the 'Help' menu or https://github.com/tmscott88/GitWriting/blob/main/README.md for further instructions.")
    
    # def print_config_corrupt_error():
    #     print(f"\nWarning: Config file '{self.name}' has corrupt or missing properties. Functionality will be limited until this is resolved.") 
    #     # print(f"\nPlease create and place `{self.name}' in your Git repo's root directory.")
    #     print(f"\nSee the included README or visit https://github.com/tmscott88/GitWriting/blob/main/README.md for further instructions.")

    # def has_valid_sections():
    #     for section in self.parser.sections():
    #         # TODO: check if section is within valid "Sections" enum
    #         for key, value in self.parser.items(section):
    #             # TODO: check if key, value matches expected format? Key match is most important
    #             print(f"{key} = {value}")