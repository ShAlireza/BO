import os

SECRET_KEY = os.getenv('SECRET_KEY')
MANAGER_HOST = os.getenv('MANAGER_HOST')
MANAGER_PORT = os.getenv('MANAGER_PORT')
LOGIN_PATH = '/api/module/login'

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
NAME = 'mysql'
MINIO_CLIENT = './mc'

# Comma separated list of valid credential names for this module services
VALID_CREDENTIAL_NAMES = 'username,password'

# These settings will be overwritten by cluster manager, so don't change them
RABBITMQ_HOST = None
RABBITMQ_PORT = None
RABBITMQ_QUEUE = None
MINIO_ADDRESS = None
MINIO_ACCESS_KEY = None
MINIO_SECRET_KEY = None
