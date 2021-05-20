import os

PYTHONPATH = os.getenv('PYTHONPATH')
API_SERVER_USER = os.getenv('API_SERVER_USER')
SCHEDULER_HOST = os.getenv('SCHEDULER_HOST')
SCHEDULER_OPENAPI_URL = os.getenv('SCHEDULER_OPENAPI_URL')

EXTERNAL_OPENAPI_URLS = (
    'http://localhost:8000/openapi.json',
    # Other urls maybe added in future
)

# SCHEDULER_
