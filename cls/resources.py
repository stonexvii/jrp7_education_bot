import os
from .reader import Reader


class Resource:
    PATH = 'resources'
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.images = {}
        self.messages = {}
        self.prompts: dict[str, str] = {}

    async def load(self):
        for res_dir in os.listdir(self.PATH):
            if not res_dir.startswith('__'):
                current_path = os.path.join(self.PATH, res_dir)
                files = {}
                for file in os.listdir(current_path):
                    reader = Reader(os.path.join(current_path, file))
                    data = await reader.load()
                    files[file.split('.')[0]] = data
                self.__setattr__(res_dir, files)

    def create_buttons(self):
        buttons = {}
        for button, text in self.prompts.items():
            if button.startswith('talk_'):
                buttons[button] = text.split(', ', 1)[0][5:]
        return buttons
