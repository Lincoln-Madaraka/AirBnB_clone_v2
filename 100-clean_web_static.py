#!/usr/bin/python3
'''Fabric script that creates and distributes an archive to web servers'''
from datetime import datetime
from fabric.api import *
from os.path import isdir, exists


env.hosts = ['100.25.19.62', '100.26.174.180']


def do_pack():
    """archive from the contents of the web_static folder of
    AirBnB Clone repo"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception:
        return None


def do_deploy(archive_path):
    '''deploy an archive to web server'''
    if exists(archive_path) is False:
        return False
    filename = archive_path.split('/')[-1]
    filename_wex = filename.split('.')[0]
    path = '/data/web_static/releases/'
    if put(archive_path, '/tmp/').failed is True:
        return False
    if run('mkdir -p {}{}/'.format(
            path, filename_wex)).failed is True:
        return False
    if run('tar -xzf /tmp/{} -C {}{}/'.format(
            filename, path, filename_wex)).failed is True:
        return False
    if run('rm  /tmp/{}'.format(filename)).failed is True:
        return False
    if run('mv {0}{1}/web_static/* {0}{1}/'.format(
                    path, filename_wex)).failed is True:
        return False
    if run('rm -rf {}{}/web_static'.format(
            path, filename_wex)).failed is True:
        return False
    if run('rm -rf /data/web_static/current').failed is True:
        return False
    if run('ln -s {}{}/ /data/web_static/current'.
            format(path, filename_wex)).failed is True:
        return False
    return True


def deploy():
    '''creates and distributes an archive to web servers'''
    if env.host == env.hosts[0]:
        file = do_pack()
        env.file = file
    if env.file is None:
        return False
    return do_deploy(env.file)


def do_clean(number=0):
    '''deletes out-of-date archives'''
    path = '/data/web_static/releases/'
    keep = local('ls versions', capture=True)
    if type(number) == str:
        number = eval(number)
    if number == 0:
        number = 1
    files = sorted(keep.split(), reverse=True)
    to_keep = files[:number]
    to_delete = [x for x in files if x not in to_keep]
    for file in to_delete:
        local('rm -r versions/{}'.format(file))
    remote = run('ls {}'.format(path))
    remote = sorted(remote.split(), reverse=True)
    remote = [x for x in remote if 'web_static' in x]
    remote_toKeep = remote[:number]
    remote_toDelete = [x for x in remote if x not in remote_toKeep]
    for file in remote_toDelete:
        run('rm -rf {}{}'.format(path, file))
