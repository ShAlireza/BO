import subprocess
import os
from datetime import datetime

from bo_shared.modules.interface import BaseModule
from minio import Minio

from config import MINIO_CLIENT


# Todo
#  1. change os.system to subprocess.Popen
#  2. ...

class MySqlModule(BaseModule):

    def backup(self):
        print(f'backing up with data {self.flat_data}')
        host = self.flat_data.get('host')
        port = self.flat_data.get('port')
        username = self.flat_data.get('username')
        password = self.flat_data.get('password')
        label = self.flat_data.get('label')
        module = self.flat_data.get('module')

        path = self.create_necessary_bucket_minio(
            label=label,
            module=module
        )

        filename = f'{path}/{label}-{module}-{datetime.now().isoformat()}'
        return_code = os.system(
            f'mysqldump -h {host} -P {port} --protocol=tcp -u {username} '
            f'-p{password} --all-databases | {MINIO_CLIENT} pipe {filename}'
        )

        if return_code != 0:
            print(f'backup failed with return code: {return_code}')
        else:
            print(f'backup {module} successful: {host}:{port}')

    def validate(self):
        pass

    def restore(self):
        pass
