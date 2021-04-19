import os
import json
from pathlib import Path

class FileHelper():

    def file_exists(path):
        file = Path(path)
        return file.is_file()

    def load_json_file(path):
        file = open(path, 'r')
        contents = json.loads(file.readline())
        file.close()
        return contents

    def save_json_file(path, data):
        with open(path, 'w') as file:
            json.dump(data, file)

    def move_file(from_path, to_path):
        os.rename(from_path, to_path)
