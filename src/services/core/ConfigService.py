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

        # notifications
        self.email_notifications_enabled = None
        self.email_username = None
        self.email_password = None
        self.email_server = None
        self.email_port = None
        self.email_to_notify = None
        
        self.slack_notifications_enabled = None
        self.slack_token = None
        self.slack_account = None
        self.slack_username = None

        # self.notifications_last_sent = None
        self.batch_minutes = None
        self.message_file_locked = False
        self.message_file = None


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

            # Port that the Flask API is available on
            # os.environ['PORT']
            self.hosting_port = os.environ['HOSTING_PORT'] if 'HOSTING_PORT' in os.environ else config_data["hosting"]["port"]

            # notifications
            self.email_notifications_enabled = config_data["notifications"]["email"]["enabled"]
            self.email_username = os.environ[self.service_name + '__EMAIL_USERNAME']
            self.email_password = os.environ[self.service_name + '__EMAIL_PASSWORD']
            self.email_server = os.environ[self.service_name + '__EMAIL_SERVER']
            self.email_port = int(os.environ[self.service_name + '__EMAIL_PORT'])
            self.email_to_notify = os.environ[self.service_name + '__EMAIL']

            self.slack_notifications_enabled = config_data["notifications"]["slack"]["enabled"]
            self.slack_token = os.environ[self.service_name + '__SLACK_TOKEN']
            self.slack_account = os.environ[self.service_name + '__SLACK_ACCOUNT']
            self.slack_username = os.environ[self.service_name + '__SLACK_USERNAME']

            self.batch_minutes = int(config_data["notifications"]["batch_minutes"])
            self.message_file_locked = config_data["notifications"]["message_file_locked"]
            
            # self.message_file = self.root_folder + '/logs/news/ft/notifications.log'



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
