import requests
import subprocess

from fastapi import FastAPI


class ModuleException(Exception):
    pass


class ManagerConfigFileNotFound(ModuleException):
    pass


class LoginFailed(ModuleException):
    pass


class MinioClientNotFound(ModuleException):
    pass


class MinioSetStorageFailed(ModuleException):
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
        self.valid_credential_names = config.VALID_CREDENTIAL_NAMES
        self.token = None

    def login(self):
        response = requests.post(
            url=f'http://{self.manager_host}:{self.manager_port}'
                f'{self.login_path}',
            json={
                'secret_key': self.secret_key,
                'module': {
                    'name': self.name,
                    'valid_credential_names': self.valid_credential_names
                },
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
        config.RABBITMQ_HOST = data.get('rabbitmq_host')
        config.RABBITMQ_PORT = data.get('rabbitmq_port')
        config.RABBITMQ_QUEUE = data.get('rabbitmq_queue')
        config.MINIO_ADDRESS = data.get('minio_address')
        config.MINIO_ACCESS_KEY = data.get('minio_access_key')
        config.MINIO_SECRET_KEY = data.get('minio_secret_key')

        assert config.RABBITMQ_HOST is not None
        assert config.RABBITMQ_PORT is not None
        assert config.RABBITMQ_QUEUE is not None
        assert config.MINIO_ADDRESS is not None
        assert config.MINIO_ACCESS_KEY is not None
        assert config.MINIO_SECRET_KEY is not None


def create_module_app():
    app = ModuleApp()
    app.login()

    try:
        subprocess.Popen(
            ['./mc', '--help'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        config.MINIO_CLIENT = './mc'
    except FileNotFoundError:
        try:
            subprocess.Popen(
                ['mc', '--help'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            config.MINIO_CLIENT = 'mc'
        except FileNotFoundError:
            raise MinioClientNotFound('minio client not found.')

    process = subprocess.run(
        [config.MINIO_CLIENT, 'alias', 'set', 'storage',
         f'http://{config.MINIO_ADDRESS}',
         f'{config.MINIO_ACCESS_KEY}',
         f'{config.MINIO_SECRET_KEY}']
    )

    if process.returncode != 0:
        raise MinioSetStorageFailed('failed to set set cloud storage.')

    @app.get("/heart")
    def heart():
        pass

    return app
