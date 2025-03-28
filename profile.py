class Profile:
    def __init__(self, browser, editor, daily_notes_path):
        self._browser = browser
        self._editor = editor
        self._daily_notes_path = daily_notes_path

    def get_browser(self):
        return self._browser

    def get_editor(self):
        return self._editor

    def get_daily_notes_path(self):
        return self._daily_notes_path

    def set_browser(self, value):
        self._browser = value

    def set_editor(self, value):
        self._editor = value

    def set_daily_notes_path(self, value):
        self._daily_notes_path = value
