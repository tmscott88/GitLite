import configparser
import utils

class Config:
    config = "config.ini"
    parser = configparser.ConfigParser()

    def read(self):
        try:
            with open(self.config, 'r', encoding="utf-8") as file:
                self.parser.read(self.config)
        except (Exception, FileNotFoundError) as e:
            print(f"\nCould not read config file {self.config}: {e}")
    
    def get_value(self, section, option):
        try:
            return self.parser.get(section, option)
        except Exception as e:
            print(f"\nCould not retrieve ['{section}', '{option}'] from '{self.config}'. {e}")
            print(f"\nPlease verify that '{self.config}' is setup correctly.")

    def set_value(self, section, option, value):
        try:
            self.parser.set(section, option, value)
            self.save(f"Set ['{section}', '{option}'] = '{value}'")
        except Exception as e:
            print(f"\nCould not set ['{section}', '{option}'] = '{value}' in '{self.config}'. {e}")

    def save(self, message):
        try:
            with open(self.config, "w", encoding="utf-8") as newfile:
                self.parser.write(newfile)
            print(f"\n{message}")
            self.show()
        except Exception as e:
            print(f"\nCould not save to config file '{newfile}': {e}")

    def show(self):
        for section in self.parser.sections():
            print()
            print(f"[{section}]")
            for key, value in self.parser.items(section):
                print(f"{key} = {value}")

class AppConfig(Config):
    def get_app(self, app_type):
        return self.get_value('APPS', app_type)

    def get_commit_limit(self):
        return self.get_value('MISC', 'commit_limit')

    def get_daily_notes_status(self):
        return self.get_valuet('DAILY_NOTES', 'status')

    def get_daily_notes_path(self):
        return self.get_value('DAILY_NOTES', 'path')

    def set_app(self, app_type, new_app):
        self.set_value('APPS', app_type, new_app)

    def set_commit_limit(self):
        self.set_value('MISC', 'commit_limit', new_limit)

    def set_daily_notes_status(self, new_status):
        self.set_value('DAILY_NOTES', 'status', new_status)
        
    def set_daily_notes_path(self):
        self.set_value('DAILY_NOTES', 'path', new_path)
        
    def print_app_error(self, name):
        print(f"\nApp '{name}' not found, or '{name}' just crashed. This may be due to a missing reference/installation, or perhaps something is wrong with {name}'s configuration.") 
        print(f"\nEnsure that the app's reference name is defined correctly in '{self.config}' and installed systemwide.") 
        print(f"\nConsult {name}'s documentation and/or forums for more information.")
        print(f"\nIf '{name}' works fine outside of GitWriting, and you are still experiencing issues here, please open an issue at:")
        print("\nhttps://github.com/tmscott88/GitWriting/issues")

    def print_config_not_found_error():
        print(f"\nWarning: Config file '{self.config}' not found. Functionality will be limited until this is resolved.") 
        print(f"\nPlease create and place `{self.config}' in your Git repo's root directory.")
        print(f"\nSee the included README or visit https://github.com/tmscott88/GitWriting/blob/main/README.md for further instructions.")

    # def print_config_corrupt_error():
    #     print(f"\nWarning: Config file '{self.config}' has corrupt or missing properties. Functionality will be limited until this is resolved.") 
    #     # print(f"\nPlease create and place `{self.config}' in your Git repo's root directory.")
    #     print(f"\nSee the included README or visit https://github.com/tmscott88/GitWriting/blob/main/README.md for further instructions.")

    # def has_valid_sections():
    #     for section in self.parser.sections():
    #         # TODO: check if section is within valid "Sections" enum
    #         for key, value in self.parser.items(section):
    #             # TODO: check if key, value matches expected format? Key match is most important
    #             print(f"{key} = {value}")