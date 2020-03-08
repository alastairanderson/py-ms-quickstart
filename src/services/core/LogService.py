import logging
import logging.config
import loggly.handlers
import requests     # TODO: Remove this when we add Tor
import yaml
from services.core.ConfigService import ConfigService
from utilities.core.DateUtils import DateUtils
from utilities.core.JsonUtils import JsonUtils
from utilities.core.OsUtils import OsUtils


class LogService:

#region initialiser
    def __init__(self, config_service):
        self._config = config_service
        log_config = yaml.load(open(self._config.logging_config_file))
        log_config.setdefault('version', 1)

        if self._config.build_config == "dev":
            log_config["handlers"]["dev_bulk_file"]["filename"] = log_config["handlers"]["dev_bulk_file"]["filename"].format(root_logs_folder=config_service.root_logs_folder)
            log_config["handlers"].pop("prod_bulk_file", None)
            log_config["handlers"].pop("prod_https", None)
            log_config["loggers"].pop("prod_bulk_logger", None)
            log_config["loggers"].pop("prod_https_logger", None)
            log_config["root"]["handlers"].remove("prod_bulk_file")
            log_config["root"]["handlers"].remove("prod_https")
            logging.config.dictConfig(log_config)
            self._logger = logging.getLogger('dev_bulk_logger')
            self._logger.setLevel(logging.DEBUG)

        elif self._config.build_config == "prod" and self._config.logging_bulk_enabled:
            log_config["handlers"]["prod_bulk_file"]["filename"] = log_config["handlers"]["prod_bulk_file"]["filename"].format(root_logs_folder=config_service.root_logs_folder)
            log_config["handlers"].pop("dev_bulk_file", None)
            log_config["handlers"].pop("prod_https", None)
            log_config["loggers"].pop("dev_bulk_logger", None)
            log_config["loggers"].pop("prod_https_logger", None)
            log_config["root"]["handlers"].remove("dev_bulk_file")
            log_config["root"]["handlers"].remove("prod_https")
            logging.config.dictConfig(log_config)
            self._logger = logging.getLogger('prod_bulk_logger')
            self._logger.setLevel(logging.INFO)

        elif self._config.build_config == "prod" and not self._config.logging_bulk_enabled:

            # Currently having this issue with logging to loggly
            # https://stackoverflow.com/questions/53641763/strange-error-traceback-in-loggly-python-recursionerror-maximum-recursion-dep

            log_config["handlers"]["prod_https"]["url"] = log_config["handlers"]["prod_https"]["url"].format(url=config_service.logging_endpoint)
            log_config["handlers"].pop("dev_bulk_file", None)
            log_config["handlers"].pop("prod_bulk_file", None)
            log_config["loggers"].pop("dev_bulk_logger", None)
            log_config["loggers"].pop("prod_bulk_logger", None)
            log_config["root"]["handlers"].remove("dev_bulk_file")
            log_config["root"]["handlers"].remove("prod_bulk_file")
            logging.config.dictConfig(log_config)
            self._logger = logging.getLogger('prod_https_logger')
            self._logger.setLevel(logging.INFO)

        else:
            raise Exception("No logger found")

        self._next_bulk_send_datetime = self.__calculate_next_bulk_send()
#endregion

#region public methods
    def send_bulk(self):
        # TODO: Update this to use the Tor client when we have it ported
        if self._next_bulk_send_datetime < DateUtils.get_current_date_time():
            bulk_file_content = OsUtils.read_lines_from_file(self._config.logging_bulk_log_file)
            bulk_http_content = ""

            for line in bulk_file_content:
                if not bulk_http_content:
                    bulk_http_content = line
                else:
                    bulk_http_content = bulk_http_content + '\n' + line

            r = requests.post(self._config.logging_bulk_endpoint, data=bulk_http_content, headers={'content-type': 'application/json'})

            if r.status_code == 200:
                OsUtils.delete_file(self._config.logging_bulk_log_file)

            self._next_bulk_send_datetime = self.__calculate_next_bulk_send()


    def get_logger(self):
        return self._logger
#endregion

#region private methods
    def __calculate_next_bulk_send(self):
        return DateUtils.add_timedelta_to_date(DateUtils.get_current_date_time(), seconds=int(self._config.logging_bulk_send_interval_in_seconds))
#endregion
