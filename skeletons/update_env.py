#!/usr/bin/env python
# -*- mode: python -*-
"""
This script is used to create/update virtualenv, installed packages and for
generating/updating apache configuration.
"""

import os
import subprocess
from optparse import OptionParser
from string import Template # pylint: disable-msg=W0402

def get_project_name():
    """
    Return project name determined from path.
    """
    return os.path.abspath(__file__).split('/')[-4]

def get_project_root():
    """
    Return project root determined from path.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def parse_command_line():
    """
    Examines command line options and does preliminary checking.
    """
    project_name = get_project_name()

    parser = OptionParser("update_env [options]")
    parser.add_option(
        "--server_name",
        action="store",
        dest="server_name",
        default=project_name,
        help="Apache conf: ServerName; Default: %s" % project_name)

    parser.add_option(
        "--user",
        action="store",
        dest="user",
        default=os.environ.get('USER'),
        help="Apache conf: WSGI process user; Default: %s." % os.environ.get('USER'))

    parser.add_option(
        "--group",
        action="store",
        dest="group",
        default=os.environ.get('USER'),
        help="Apache conf: WSGI process user; Default: %s." % os.environ.get('USER'))

    return parser.parse_args()


def update_apache_conf(options, project_root, project_name):
    """
    This updates/create apache configuration.
    """
    options['project_root'] = project_root
    options['server_name'] = project_name
    if not options.get('user', None):
        options['user'] = os.environ.get('USER')
    if not options.get('group', None):
        options['group'] = os.environ.get('USER')

    config_path = os.path.join(project_root, 'config')
    _file = open(os.path.join(config_path, 'apache-conf.template'))
    template = Template(_file.read())
    _file.close()

    _file = open(os.path.join(config_path, "%s.conf" % project_name), 'w')
    print >> _file, template.substitute(options)
    _file.close()



def update_installed_packages(project_root):
    """
    This updates/installs installed packages in virtualenv from pip_requirements.txt
    """
    _bin = os.path.join(project_root, "env", "bin")
    _python = os.path.join(_bin , "python")
    _easy_install = os.path.join(_bin , "easy_install")
    _pip = os.path.join(_bin , "pip")

    subprocess.call([_easy_install, "pip"])
    subprocess.call([_pip, "install", "-r",
                     os.path.join(project_root, "config", "pip_requirements.txt")])

def update_virtualenv(project_root):
    """
    This updates/create virtualenv 
    """
    subprocess.call([
        "virtualenv", "--no-site-packages",
        os.path.join(project_root, "env")
        ])


def update_all(options, project_root=None, project_name=None, create_env=True):
    """
    This updates all.
    """
    if not project_root:
        project_root = get_project_root()
    if not project_name:
        project_name = get_project_name()

    if create_env:
        update_virtualenv(project_root)
    update_apache_conf(options, project_root, project_name)
    update_installed_packages(project_root)
    
def main():
    """
    Called from command line.
    """
    options, args = parse_command_line() # pylint: disable-msg=W0612
    update_all(options.__dict__, create_env=False)
    
if __name__ == '__main__':
    main()
    
