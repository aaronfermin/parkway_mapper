import json
import os
from pathlib import Path


class FileHelper:

    @staticmethod
    def file_exists(path):
        file = Path(path)
        return file.is_file()

    @staticmethod
    def load_json_file(path):
        with open(path) as file:
            contents = json.loads(file.read())
        return contents

    @staticmethod
    def save_json_file(path, data):
        with open(path, 'w') as file:
            json.dump(data, file)

    @staticmethod
    def move_file(from_path, to_path):
        # this is pretty extra to have in its own method, but just to avoid importing os in another file for 1 line
        os.rename(from_path, to_path)
