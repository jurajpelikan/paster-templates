"""
This script provide fabric interface for update virtualenv
dependencies, generating/updating configuration files.
"""
import os
from string import Template # pylint: disable-msg=W0402
from fabric.api import local

def get_project_name():
    """
    Return project name determined from path.
    """

    return get_project_root().split('/')[-1]

def get_project_root():
    """
    Return project root determined from path.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def update_env():
    """
    This command updates python packages.
    """
    project_root = get_project_root()
    pip = os.path.join(project_root, 'env', 'bin', 'pip')
    requirements = os.path.join(project_root, 'config', 'pip_requirements.txt')
    local("%s install -r %s" % (pip, requirements))

def apache_conf(hostname=None, user=None, group=None):
    """
    This updates/create apache configuration.
    """
    options = {}

    if hostname:
        options['hostname'] = hostname
    else:
        options['hostname'] = get_project_name()

    if user:
        options['user'] = user
    else:
        options['user'] = os.environ.get('USER')

    if group:
        options['group'] = group
    else:
        options['group'] = os.environ.get('USER')

    options['project_root'] = get_project_root()
    options['config_path'] = os.path.join(options['project_root'], 'config')

    _file = open(os.path.join(options['config_path'], 'apache-conf.template'))
    template = Template(_file.read())
    _file.close()

    _file = open(
        os.path.join(options['config_path'], "%s.conf" % options['hostname']), 'w')
    print >> _file, template.substitute(options)
    _file.close()


def supervisor_celery_conf(hostname=None, user=None, group=None, workers=2):
    """
    This updates/create apache configuration.
    """
    options = {}

    if hostname:
        options['hostname'] = hostname
    else:
        options['hostname'] = get_project_name()

    if user:
        options['user'] = user
    else:
        options['user'] = os.environ.get('USER')

    if group:
        options['group'] = group
    else:
        options['group'] = os.environ.get('USER')

    options['workers'] = workers
    options['project_root'] = get_project_root()
    options['django_project_root'] = os.path.join(options['project_root'], 'project')
    options['config_path'] = os.path.join(options['project_root'], 'config')
    options['python'] = os.path.join(options['project_root'], 'env', 'bin', 'python')
    options['manage'] = os.path.join(options['project_root'], 'project', 'manage.py')
    options['log'] = os.path.join(options['project_root'], 'logs')
    
    _file = open(os.path.join(
        options['config_path'], 'supervisor-celery.conf.template'))
    template = Template(_file.read())
    _file.close()

    _file = open(
        os.path.join(
            options['config_path'],
            "%s-supervisor-celery.conf" % options['hostname']),
        'w')
    print >> _file, template.substitute(options)
    _file.close()

