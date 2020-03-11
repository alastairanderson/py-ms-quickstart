import random
from random import randint
import requests
from urllib.parse import urljoin
import zlib
from utilities.core.DockerUtils import DockerUtils
from utilities.core.OsUtils import OsUtils
from utilities.core.TimeUtils import TimeUtils

# This relies on https://hub.docker.com/r/peterdavehello/tor-socks-proxy/ running

class HttpService:

#region initialisers
    def __init__(
        self,
        config_service,
        log_service
    ):
        self._config = config_service
        self.req_i = 0        # No of requests that have been made since last ip change
        self.n_requests = 25  # No of requests before rotating the ip address
        self._logger = log_service.get_logger()
        self._logger.info(f"Initial IP address: {self.get_ip_address()}")
        self._user_agent_strings_file = self._config.root_config_folder + "/common/user-agent-strings.txt"
        self._logger.info(f"User agent strings: {self._user_agent_strings_file}")
#endregion

#region public methods
    user_agent_strings = []

    def select_random_user_agent(self):
        if len(self.user_agent_strings) == 0:
            with open(self._user_agent_strings_file, "r") as file:
                for line in file:
                    self.user_agent_strings.append(line.replace("\n", ""))

        random.shuffle(self.user_agent_strings)

        random_index = randint(0, len(self.user_agent_strings)-1)
        return self.user_agent_strings[random_index]


    def get(self, url, headers=None, timeout=None):
        """Attempts an HTTP get and returns the response and/or an error message"""
        if not headers:
            headers = {}

        # Always set the agent string (?)
        # headers['user-agent'] = TorHttpUtils.select_random_user_agent()

        total_retry_attempt = 5
        attempts = 0
        last_error_message = None

        while attempts < total_retry_attempt:
            try:
                response = requests.get(url, headers=headers, timeout=timeout, 
                    proxies=dict(http=self._config.env_tor_socks_proxy))

                # response = requests.get(url, headers=headers, timeout=timeout)

                self.__update_count()

                if response:
                    if response.status_code == 200:
                        TimeUtils.sleep_for_random_time_period(3,6)
                        return response, None       # the happy path, return data with no error
                    else:
                        print("Status code for {0} was {1}".format(url, response.status_code))
                        print("Rotating IP address...")
                        self.__rotate_ip_address()
                        attempts = attempts + 1
                        TimeUtils.sleep_for_random_time_period(3,6)
                else:
                    if response.status_code == 404:
                        return response, "404 Page not found"
                    else:
                        last_error_message = "No data response"
                        attempts = attempts + 1
            
            except requests.exceptions.TooManyRedirects as tmrex:
                last_error_message = f"Too many redirects have occurred for {url}: " + str(tmrex)
                print(f"Too many redirects have occurred for {url} on attempt {attempts}")
                attempts = attempts + 1
                TimeUtils.sleep_for_random_time_period(3,6)
            except requests.exceptions.Timeout as tmex:
                last_error_message = f"A timeout has occurred for {url}: " + str(tmex)
                print(f"A timeout has occurred for {url} on attempt {attempts}")
                attempts = attempts + 1
                TimeUtils.sleep_for_random_time_period(3,6)
            except requests.exceptions.ConnectionError as ce:
                last_error_message = f"Connection refused for {url}: " + str(ce)
                print(f"Connection refused for {url} on attempt {attempts}")
                attempts = attempts + 1
                TimeUtils.sleep_for_random_time_period(3,6)

        return response, last_error_message


    def download(self, url, file_path, headers=None, timeout=None):
        try:
            response, error_msg = self.get(url, headers, timeout)

            if response:
                if response.status_code == 200:
                    OsUtils.write_to_file_in_binary_mode(file_path, response.content)
                    return None
                else:
                    return f"Status code {response.status_code} received for {url}"
            else:
                return error_msg

        except Exception as ex:
            print(ex)
            raise ex


    def join_root_url_and_relative_url_path(self, root_url, relative_url):
        if root_url.rfind('/') != len(root_url):
            root_url = root_url + '/'
        return urljoin(root_url, relative_url)


    def check_url_exists(self, url, headers=None):
        response = self.__get_head(url, headers=headers)
        return response.status_code == 200


    def get_ip_address(self):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en-GB,en;q=0.5",
            "connection": "keep-alive",
            "dnt": "1",
            "host": "ipinfo.io",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0"
        }

        response, _ = self.get("http://ipinfo.io/ip", headers=headers, timeout=300)
        return response.content.decode("utf-8").strip()  
#endregion

#region private methods
    def __get_head(self, url, headers=None):
        response = requests.head(url, headers=headers)
        return response


    def __update_count(self):
        self.req_i += 1
        if self.req_i > self.n_requests:
            self.req_i = 0
            self.__rotate_ip_address()


    def __rotate_ip_address(self):
        self._logger.info(f"Restarting docker proxy to rotate IP...")
        DockerUtils.restart_container(self._config.tor_container_id)
        self._logger.info(f"New IP address: {self.get_ip_address()}")
#endregion
