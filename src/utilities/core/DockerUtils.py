import docker

# # Useful Links
# # https://docker-py.readthedocs.io/en/stable/
# # https://github.com/docker/docker-py

class DockerUtils:

#region public methods
    @staticmethod
    def is_container_running(id: str):
        try:
            container = DockerUtils.__get_container(id)
            return container.status == "running"
        except docker.errors.NotFound:
            return False


    @staticmethod
    def restart_container(id: str):
        container = DockerUtils.__get_container(id)
        print(f"Container {id} status: {container.status}")
        print(f"Restarting container {id}...")
        container.restart()
        print(f"Container {id} status: {container.status}")


    @staticmethod
    def start_container(id: str):
        container = DockerUtils.__get_container(id)
        print(f"Container {id} status: {container.status}")
        container.start()
        container = DockerUtils.__get_container(id)
        print(f"Container {id} status: {container.status}")


    @staticmethod
    def stop_container(id: str):
        container = DockerUtils.__get_container(id)
        print(f"Container {id} status: {container.status}")
        container.stop()
        container = DockerUtils.__get_container(id)
        print(f"Container {id} status: {container.status}")
#endregion

#region private methods
    @staticmethod
    def __get_container(id: str):
        client = docker.from_env()
        return client.containers.get(id)
#endregion

#region sandbox
# container_id = "deploy_wordpress_1"             # or the CONTAINER ID of '24a'
# DockerUtils.restart_container(container_id)
#endregion
