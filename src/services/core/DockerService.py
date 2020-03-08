import docker

# # Useful Links
# # https://docker-py.readthedocs.io/en/stable/
# # https://github.com/docker/docker-py

class DockerService:

#region initialisers
    def __init__(self, config_service, log_service):
        self._config = config_service
        self._logger = log_service.get_logger()
#endregion

#region public methods
    def is_container_running(self, id: str):
        try:
            container = self.__get_container(id)
            return container.status == "running"
        except docker.errors.NotFound:
            return False


    def restart_container(self, id: str):
        container = self.__get_container(id)
        print(f"Container {id} status: {container.status}")
        print(f"Restarting container {id}...")
        container.restart()
        print(f"Container {id} status: {container.status}")


    def start_container(self, id: str):
        container = self.__get_container(id)
        print(f"Container {id} status: {container.status}")
        container.start()
        container = self.__get_container(id)
        print(f"Container {id} status: {container.status}")


    def stop_container(self, id: str):
        container = self.__get_container(id)
        print(f"Container {id} status: {container.status}")
        container.stop()
        container = self.__get_container(id)
        print(f"Container {id} status: {container.status}")
#endregion

#region private methods
    def __get_container(self, id: str):
        client = docker.from_env()
        return client.containers.get(id)
#endregion

