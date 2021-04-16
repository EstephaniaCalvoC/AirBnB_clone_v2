#!/usr/bin/python3
"""Define the task do_deploy to fabric (fab) command"""

from fabric.api import *
from os import path

env.hosts = ['35.243.155.96', '54.227.102.243']


def do_deploy(archive_path):
    """Distribute an archive to your web servers"""

    if not path.exists(archive_path):
        print("path no existe")
        return False

    put_file = put(archive_path, "/tmp/")
    if put_file.failed:
        return False

    file_name = archive_path[len("versions/"): -1 * len(".tgz")]
    dest_folder = '/data/web_static/releases/'
    create_folder = run('mkdir -p ' + dest_folder + file_name + '/')
    if create_folder.failed:
        return False

    unpack_command_1 = 'tar -xzf /tmp/' + file_name + '.tgz'
    unpack_command_2 = ' -C /data/web_static/releases/' + file_name + '/'
    unpack = run(unpack_command_1 + unpack_command_2)
    if unpack.failed:
        return False

    del_archive = run('rm /tmp/' + file_name + '.tgz')
    if del_archive.failed:
        return False

    move = run('mv /data/web_static/releases/' +
               file_name +
               '/web_static/* /data/web_static/releases/' +
               file_name +
               '/')
    if move.failed:
        return False

    del_folder = run('rm -rf /data/web_static/releases/' +
                     file_name +
                     '/web_static')
    if del_folder.failed:
        return False

    del_slink = run('rm -rf /data/web_static/current')
    if del_slink.failed:
        return False

    create_slink = run('ln -sf /data/web_static/releases/' +
                       file_name + '/' + ' /data/web_static/current')
    if create_slink.failed:
        return False

    return True
