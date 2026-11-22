import os
import json

class JsonProcessor:
    """
    A class to perform operations on JSON files.
    """

    def read_json(self, file_path):
        """
        Reads a JSON file from the specified path.

        Parameters:
        - file_path (str): Path to the JSON file.

        Returns:
        - dict: The parsed JSON data if successful.
        - int: 0 if the file does not exist.
        - int: -1 if an error occurs during reading.
        """
        if not os.path.exists(file_path):
            return 0  # File does not exist
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            return -1  # Error occurred during reading

    def write_json(self, data, file_path):
        """
        Writes the given JSON data to a file at the specified path.

        Parameters:
        - data (dict): The JSON data to write.
        - file_path (str): Path to the output JSON file.

        Returns:
        - int: 1 if the write was successful.
        - int: -1 if an error occurs during writing.
        """
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f)
            return 1
        except Exception as e:
            return -1  # Error occurred during writing

    def process_json(self, file_path, remove_key):
        """
        Reads a JSON file, removes the specified key, and writes the modified data back.

        Parameters:
        - file_path (str): Path to the JSON file.
        - remove_key (str): Key to be removed from the JSON data.

        Returns:
        - int: 1 if the operation was successful.
        - int: 0 if the file does not exist or the key is not found.
        - int: -1 if an error occurs during reading or writing.
        """
        # Check if the file exists
        if not os.path.exists(file_path):
            return 0  # File does not exist

        # Read the JSON data
        data = self.read_json(file_path)
        if data == -1:
            return -1  # Error reading the file

        # Check if the key exists
        if remove_key not in data:
            return 0  # Key not found

        # Remove the key
        del data[remove_key]

        # Write the modified data back to the file
        if self.write_json(data, file_path) == 1:
            return 1  # Success
        else:
            return -1  # Error writing the file


processor = JsonProcessor()

# Example JSON content:
# {"name": "Alice", "age": 30, "city": "New York"}

# Remove the 'city' key
result = processor.process_json("data.json", "city")

if result == 1:
    print("Key removed successfully.")
elif result == 0:
    print("Key not found or file not found.")
else:
    print("An error occurred during processing.")
