class Menu:
    def __init__(self, title):
        self.options = {}
        self.title = title

    def add_option(self, key, description, action):
        self.options[key] = (description, action)

    def show(self):
        """Display the menu and handle user choice."""
        while True:
            print(f"\n[{self.title}]:")
            options = self.options.items()
            for key, (desc, _) in options:
                print(f"{key}: {desc}")
            try:
                choice = int(input("Select an option: "))
                if choice not in self.options.keys():
                    raise ValueError()
                else:
                    self.options[choice][1]()
            except (ValueError, IndexError):
                print("\nInvalid input.")