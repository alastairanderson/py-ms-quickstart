from services.core.ConfigService import ConfigService

class NotificationService:
    
    def __init__(self, config_service):
        self._config_service = config_service
        self.__read_config()


    def __read_config(self):
        pass
