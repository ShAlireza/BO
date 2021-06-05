from bo_shared.modules.interface import BaseModule
from minio import Minio

mysql_dump = f'/usr/bin/mysqldump -u root'


class MySqlModule(BaseModule):

    def backup(self):
        print(f'backing up with data {self.data}')
        pass

    def validate(self):
        pass

    def restore(self):
        pass

# def main():
#     client = Minio(
#         "http://172.16.18.242:9000",
#         access_key="minio",
#         secret_key="minio123",
#     )
#     client.make_bucket()
