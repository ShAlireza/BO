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
        namespace = self.flat_data.get('namespace')
        module = self.flat_data.get('module')

        filename = f'{self.backup_path}/{namespace}-{module}-{datetime.now().isoformat()}'
        mysql = subprocess.Popen(
            ['mysqldump', '-h', f'{host}', '-P', f'{port}', '--protocol=tcp',
             '-u',
             f'{username}', f'-p{password}', '--all-databases'],

            stdout=subprocess.PIPE
        )

        minio = subprocess.Popen(
            [MINIO_CLIENT, 'pipe', f'{filename}'],
            stdin=mysql.stdout,
            universal_newlines=True,
        )
        stdout, stderr = minio.communicate()

        return_code = minio.poll()
        if return_code != 0:
            print(stdout, stderr)
        else:
            print(f'backup {module} successfully completed: {host}:{port}')

    def validate(self):
        pass

    def restore(self):
        pass
