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

        # hosting
        self.hosting_port = None

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

            # os.environ['PORT']
            self.hosting_port = os.environ['HOSTING_PORT'] if 'HOSTING_PORT' in os.environ else config_data["hosting"]["port"]


        except KeyError as ke:
            print(f"There was an issue retrieving {ke.args[0]}")
        except Exception as ex:
            print("There was an issue opening " + self.config_file)
        finally:
            data_file.close()
#endregion


#region public methods
    def update_config(self, key, value):
        with open(self.config_file, "r") as jsonFile:
            data = json.load(jsonFile)

        if "." in key:
            keys = key.split(".")
            
            if len(keys) == 2:
                data[keys[0]][keys[1]] = value
            elif len(keys) == 3:
                data[keys[0]][keys[1]][keys[2]] = value
            elif len(keys) == 4:
                data[keys[0]][keys[1]][keys[2]][keys[3]] = value
            elif len(keys) == 5:
                data[keys[0]][keys[1]][keys[2]][keys[3]][keys[4]] = value
        else:
            data[key] = value

        with open(self.config_file, "w") as jsonFile:
            json.dump(data, jsonFile, sort_keys=True, indent=4)

        self.__read_config()
#endregion
