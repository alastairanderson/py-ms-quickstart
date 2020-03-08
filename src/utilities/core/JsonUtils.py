import json
import os


class JsonUtils:
    
    @staticmethod
    def save_to_file(file_path, json_data):
        """Saves JSON to a file"""
        try:
            with open(file_path, "w") as json_file:
                json.dump(json_data, json_file, sort_keys=True, indent=4)
        except Exception as ex:
            print("There was an issue saving to " + file_path)
        finally:
            json_file.close()


    @staticmethod
    def load_from_file(file_path):
        result = None

        try:
            with open(file_path, "r") as json_file:
                result = json.load(json_file)
        except Exception as ex:
            print("There was an issue loading from " + file_path)
        finally:
            json_file.close()

        return result