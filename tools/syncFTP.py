# -*- encode: utf-8 -*-
import configparser
import os

import paramiko
import sys

"""同步 FTP 图片"""
cfg = configparser.ConfigParser()
cfg.read('conf')
if 'sftp' in cfg:
    sftp = cfg['sftp']
else:
    raise BaseException

ip = str(sftp['ip'])
port = int(sftp['port'])
username = str(sftp['username'])
password = str(sftp['password'])
image_dir = '../'
remote_dir_path = str(sftp['remote_dir_path'])


class SFTP(object):
    transport = None
    ftp = None
    ip = None
    port = None
    username = None
    password = None

    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def open(self):
        try:
            if self.transport is None:
                self.transport = paramiko.Transport((self.ip, self.port))

            if self.ftp is None:
                self.ftp = paramiko.SFTP.from_transport(self.transport)

        except BaseException as e:
            self.close()
            print(str(e))

    def get_files(self, current_directory):
        files = []
        self.ftp.chdir(current_directory)

        for remote_dir in self.listdir(current_directory):
            if os.path.isdir(remote_dir):
                files.extend(self.get_files(remote_dir))
            else:
                files.append(current_directory + '/' + remote_dir)

        return files

    def close(self):
        if self.transport is not None:
            self.transport.close()

        if self.ftp is not None:
            self.ftp.close()


try:
    sftp = SFTP(ip, port, username, password)
    sftp.open()
    print(sftp.ftp)
    sys.exit()
    print(remote_dir_path)
    files = sftp.get_files(remote_dir_path)
    print(files)
finally:
    sftp.close()

sys.exit()