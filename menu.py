class Menu:
    def __init__(self, title):
        self.options = {}
        self.title = title

    def add_option(self, key, description, action):
        self.options[key] = (description, action)  

    def show(self, post_action=None):
        """Display the menu and handle user choice."""
        while True:
            print(f"\n[{self.title}]:")
            options = self.options.items()
            for key, (desc, _) in options:
                print(f"{key}: {desc}")
            try:
                choice = int(input("Select an option: "))
                if choice not in self.options:
                    raise ValueError()
                self.options[choice][1]()
            except (ValueError, IndexError):
                print("\nInvalid input.")
            if post_action is not None:
                post_action()