
import json
import os


class JSONProcessor:
    """
    This is a class to process JSON file, including reading and
    writing JSON files, as well as processing JSON data by
    removing a specified key from the JSON object.
    """

    def read_json(self, file_path):
        """
        Read a JSON file and return the data.
        Return 0 if the file does not exist.
        Return -1 if an error occurs.
        """
        if not os.path.exists(file_path):
            return 0

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except (OSError, ValueError, TypeError):
            return -1

    def write_json(self, data, file_path):
        """
        Write data to a JSON file.
        Return 1 if successful, otherwise -1.
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            return 1
        except (OSError, ValueError, TypeError):
            return -1

    def process_json(self, file_path, remove_key):
        """
        Remove a specified key from a JSON file.
        Return 1 if successfully removed and saved.
        Return 0 if the file or key does not exist.
        """
        if not os.path.exists(file_path):
            return 0

        data = self.read_json(file_path)

        if not isinstance(data, dict):
            return 0

        if remove_key not in data:
            return 0

        del data[remove_key]

        return self.write_json(data, file_path)
