#!/usr/bin/python3
"""Define the tasks to_pack deploy web_static"""

from fabric.api import *
from datetime import datetime
from os import path

n = datetime.now()
env.hosts = ['35.243.155.96', '54.227.102.243']


def do_pack():
    """Generate a .tgz archive from the contents of the web_static."""

    data = (n.year, n.month, n.day, n.hour, n.minute, n.second)
    file_name = 'versions/web_static_{}{}{}{}{}{}.tgz'.format(*data)
    local('mkdir -p versions')
    command = local("tar -cvzf " + file_name + " ./web_static/")
    if command.succeeded:
        return file_name
    return None


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


def deploy():
    """Run pack and deploy the web_statics"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


def do_clean(number=0):
    """Delete out-of-date archives"""

    n = int(number)
    keep_one = 'ls -t | tail -n +2 | xargs rm -rfv'
    keep_n = 'ls -t | tail -n +{} | xargs rm -rfv'

    with lcd('versions'):
        if n == 0 or n == 1:
            local(keep_one)
        else:
            local(keep_n.format(n + 1))

    with cd('/data/web_static/releases/'):
        if n == 0 or n == 1:
            run(keep_one)
        else:
            run(keep_n.format(n + 1))
