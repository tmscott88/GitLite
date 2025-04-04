class Menu:
    def __init__(self, title):
        self.options = {}
        self.title = title

    def add_option(self, key, description, action, post_action=None):
        self.options[key] = (description, action, post_action)  

    def show(self):
        """Display the menu and handle user choice."""
        while True:
            print(f"\n[{self.title}]:")
            options = self.options.items()
            for key, (desc, _, _) in options:
                print(f"{key}: {desc}")
            try:
                choice = int(input("Select an option: "))
                if choice not in self.options.keys():
                    raise ValueError()
                else:
                    self.options[choice][1]()
                    if self.options[choice][2] != None:
                        post_action()
            except (ValueError, IndexError):
                print("\nInvalid input.")