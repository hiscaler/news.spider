# -*- encode: utf-8 -*-
import configparser
import os

import paramiko
import sys

"""FTP 文件同步"""


class Sync(object):
    _config = {
        'ip': None,
        'port': 21,
        'username': None,
        'password': None
    }

    _count = 0

    _remote_dir = None

    _local_dir = None

    def __init__(self, config, remote_dir, local_dir):
        for key in config:
            if key in self._config:
                self._config[key] = config[key]

        self._remote_dir = remote_dir
        self._local_dir = local_dir

    def open(self):
        pass

    def get_files(self, current_directory):
        pass

    def download(self):
        pass

    def upload(self):
        pass

    def close(self):
        pass


class SyncFtp(Sync):
    _transport = None
    _ftp = None

    def open(self):
        try:
            if self._transport is None:
                self._transport = paramiko.Transport((self._config['ip'], self._config['port']))

            self._transport.connect(username=self._config['username'], password=self._config['password'])

            if self._ftp is None:
                self._ftp = paramiko.SFTP.from_transport(self._transport)

        except BaseException as e:
            self.close()
            print(str(e))

    def get_files(self, current_directory):
        files = []
        self._ftp.chdir(current_directory)

        for remote_dir in self._ftp.listdir(current_directory):
            if os.path.isdir(remote_dir):
                files.extend(self.get_files(remote_dir))
            else:
                files.append(current_directory + '/' + remote_dir)

        return files

    def download(self, current_directory):
        files = self.get_files(current_directory)
        if files:
            for file in files:
                local_path = file.replace(self._remote_dir, self._local_dir)
                if not os.path.exists(os.path.dirname(local_path)):
                    os.mkdir(os.path.dirname(local_path))

                if not os.path.exists(local_path):
                    self._count += 1
                    print("%s: Download %s file..." % (self._count, file))
                    self._ftp.get(file, localpath=local_path)
                else:
                    print("Ignore %s file..." % file)

    def close(self):
        if self._transport is not None:
            self._transport.close()

        if self._ftp is not None:
            self._ftp.close()


if __name__ == '__main__':
    cfg = configparser.ConfigParser()
    cfg.read('conf')
    if 'ftp' in cfg:
        ftp_config = cfg['ftp']
    else:
        raise BaseException

    config = {
        'ip': str(ftp_config['ip']),
        'port': int(ftp_config['port']),
        'username': str(ftp_config['username']),
        'password': str(ftp_config['password'])
    }
    remote_dir = str(ftp_config['remote_dir'])
    local_dir = str(ftp_config['local_dir'])

    try:
        sftp = SyncFtp(config, remote_dir=remote_dir, local_dir=local_dir)
        sftp.open()
        print(remote_dir)
        dirs = sftp.get_files(remote_dir)
        for dir in dirs:
            sftp.download(dir)


    finally:
        sftp.close()
