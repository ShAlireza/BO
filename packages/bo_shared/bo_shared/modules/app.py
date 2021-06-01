import requests

from fastapi import FastAPI


class ModuleException(Exception):
    pass


class ManagerConfigFileNotFound(ModuleException):
    pass


class LoginFailed(ModuleException):
    pass


try:
    import config
except ImportError:
    raise ManagerConfigFileNotFound('config.py not found.')


class ModuleApp(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secret_key = config.SECRET_KEY
        self.manager_host = config.MANAGER_HOST
        self.manager_port = config.MANAGER_PORT
        self.login_path = config.LOGIN_PATH
        self.host = config.HOST
        self.port = config.PORT
        self.name = config.NAME
        self.token = None

    def login(self):
        response = requests.post(
            url=f'http://{self.manager_host}:{self.manager_port}'
                f'{self.login_path}',
            json={
                'secret_key': self.secret_key,
                'name': self.name,
                'instance': {
                    'host': self.host,
                    'port': self.port
                }
            }
        )

        if response.status_code != 200:
            raise LoginFailed(f'login on manager failed, check you configs. '
                              f'(manager status_code: {response.status_code})')

        data = response.json()

        self.token = data.get('token').get('key')
        config.KAFKA_HOST = data.get('kafka_host')
        config.KAFKA_PORT = data.get('kafka_port')
        config.KAFKA_TOPIC = data.get('kafka_topic')

        assert config.KAFKA_HOST is not None
        assert config.KAFKA_PORT is not None
        assert config.KAFKA_TOPIC is not None


def create_module_app():
    app = ModuleApp()
    app.login()

    @app.get("/heart")
    def heart():
        pass

    return app
