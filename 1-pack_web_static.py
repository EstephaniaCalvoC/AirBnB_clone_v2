#!/usr/bin/python3
"""Define the task to_pack to fabric (fab) command"""

from fabric.api import run, local, sudo
from datetime import datetime

n = datetime.now()


def do_pack():
    """Generate a .tgz archive from the contents of the web_static."""

    data = (n.year, n.month, n.day, n.hour, n.minute, n.second)
    file_name = 'versions/web_static_{}{}{}{}{}{}.tgz'.format(*data)
    local('mkdir -p versions')
    command = local("tar -cvzf " + file_name + " ./web_static/")
    if command.succeeded:
        return file_name
    return None
