import os

SECRET_KEY = "-qBLt7PhmITXYXFQG+>U>r?*=+Pq<Ne$su=jQqWux7k!jRx$lP#3*Pr63+wyYi3O"
MANAGER_HOST = 'localhost'
MANAGER_PORT = '9000'
LOGIN_PATH = '/api/module/login'
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
NAME = 'mysql'
VALID_CREDENTIAL_NAMES = 'username,password'
RABBITMQ_HOST = None
RABBITMQ_PORT = None
RABBITMQ_QUEUE = None
