import yaml
import requests
from pathlib import Path
import zipfile

from fastapi import FastAPI


class ManagerConfigFileNotFound(Exception):
    pass


class LoginFailed(Exception):
    pass


try:
    import config
except ImportError:
    raise ManagerConfigFileNotFound('config.py not found.')


class ModuleApp(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager_config_file = 'config.py'
        self.secret_key = config.secret_key
        self.manager_host = config.manager_host
        self.manager_port = config.manager_port
        self.register_path = config.register_path
        self.token = None

    def login(self):
        response = requests.get(
            url=f'http://{self.manager_host}:{self.manager_port}'
                f'{self.register_path}'
        )

        if response.status_code != 200:
            raise LoginFailed('login on manager failed, check you configs.')

        data = response.json()
        self.token = data.get('token').get('key')
        config.KAFKA_HOST = data.get('kafka_host')
        config.KAFKA_PORT = data.get('kafka_port')


def create_module_app():
    app = ModuleApp()
    app.login()

    return app
