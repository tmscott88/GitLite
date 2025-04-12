"""Contains a model for an interactive Menu object"""
from readchar import readkey
import app_utils as app

class Menu:
    """The interactive, base Menu object"""
    def __init__(self, title):
        self.options = {}
        self.title = title

    def add_option(self, key, description, action):
        """Adds an actionable option to the Menu object"""
        self.options[key] = (description, action)

    def show(self, post_action=None):
        """Display the menu and handle user choice."""
        while True:
            print(f"\n[{self.title}]:")
            options = self.options.items()
            for key, (desc, _) in options:
                print(f"{key}: {desc}")
            try:
                while True:
                    print("Select an option: ")
                    k = int(readkey())
                    print(f"Selected: {k}")
                    if k not in self.options:
                        raise ValueError
                    self.options[k][1]()
                    break
            except (ValueError, IndexError):
                app.clear()
                print("\nInvalid input.")
            if post_action is not None:
                post_action()
