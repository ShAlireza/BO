import os

SECRET_KEY = "MoyIgPkLQu-yxh@1VM1JMyWD#bV3BR!gXON2eD=dJHyh3vP86Szn3zrO-<6_-t6Z"
MANAGER_HOST = 'localhost'
MANAGER_PORT = '8000'
LOGIN_PATH = '/api/module/login'
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
NAME = 'mysql'
KAFKA_HOST = None
KAFKA_PORT = None
KAFKA_TOPIC = None
