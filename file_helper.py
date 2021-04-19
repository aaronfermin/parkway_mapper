import os
import json

class FileHelper():

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
