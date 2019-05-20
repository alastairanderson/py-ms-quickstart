import json
import os

class ConfigService:

#region initialiser
    def __init__(self, config_file_path):
        self.config_file = config_file_path

        # metadata
        self.service_name = None
        self.version = None
        self.build_config = None

        self.__read_config()
#endregion

#region private methods
    def __read_config(self):
        try:
            with open(self.config_file) as data_file:
                config_data = json.load(data_file)
            
            # metadata
            self.service_name = config_data["about"]["service"]
            self.version = config_data["about"]["version"]
            self.build_config = config_data["about"]["build_config"]

        except KeyError as ke:
            print(f"There was an issue retrieving {ke.args[0]}")
        except Exception as ex:
            print("There was an issue opening " + self.config_file)
        finally:
            data_file.close()
#endregion
