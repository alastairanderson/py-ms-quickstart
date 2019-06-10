from services.core.ConfigService import ConfigService

class NotificationService:
    
#region initialiser
    def __init__(self, config_service, email_service, slack_service):
        self._config_service = config_service
        self._email_service = email_service
        self._slack_service = slack_service
        self.__read_config()
#endregion

#region public methods
    def send(self):
        pass

    
    def send_bulk(self):
        pass
#endregion

#region private methods
    def __read_config(self):
        pass


    def __lock_message_file(self):
        self._config_service.update_config("notifications.message_file_locked", True)


    def __unlock_message_file(self):
        self._config_service.update_config("notifications.message_file_locked", False)
#endregion
